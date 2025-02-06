import pygame
import random
from settings import *


def generate_static_line_points(base_y, amplitude, step, width):
    """
    Generates a list of points along a horizontal line with random vertical offsets.

    Parameters:
        base_y (int): The baseline y-coordinate of the line.
        amplitude (int): The maximum vertical deviation from the baseline.
        step (int): The horizontal distance between consecutive points.
        width (int): The total width of the screen.

    Returns:
        List[Tuple[int, int]]: A list of (x, y) points.
    """
    points = []
    for x in range(0, width + step, step):
        offset = random.randint(-amplitude, amplitude)
        y = base_y + offset
        points.append((x, y))
    return points


def half_screen_scene(screen, side, bluedot):
    screen.fill((0, 0, 0))

    # --- 1. Create a random curve ---
    # Parameters for the curve – you can tweak these ranges for more/less variation.
    curve_amplitude = random.randint(20, 100)
    curve_step = random.randint(20, 50)
    curve_base_y = random.randint(HEIGHT // 4, 3 * HEIGHT // 4)

    # Use our helper to generate a set of points spanning the width.
    curve_points = generate_static_line_points(
        curve_base_y, curve_amplitude, curve_step, WIDTH
    )

    # Draw the curve in gray (100, 100, 100). Increase line width for visibility.
    curve_color = (125, 125, 125)
    pygame.draw.lines(screen, curve_color, False, curve_points, random.randint(2, 5))

    # Compute an average x value from the curve as a rough boundary.
    avg_curve_x = sum(p[0] for p in curve_points) / len(curve_points)

    # --- 3. Fill with a noisy gradient ---
    # Gradient settings: We start near 100 and gradually increase toward 150.
    base_value = 50
    target_value = 75
    noise_range = 60  # Maximum offset in either direction

    if side == "left":
        # For the left side, fill from x=0 to the boundary (avg_curve_x).
        # t goes from 1 at x=0 (more intense) down to 0 at x=avg_curve_x.
        for x in range(0, int(avg_curve_x) + 1):
            t = (avg_curve_x - x) / avg_curve_x  # t = 1 at left edge, 0 at boundary
            value = int(base_value + t * (target_value - base_value))
            # Add noise and clamp between 0 and 255.
            noise = random.randint(-noise_range, noise_range)
            color_val = max(0, min(255, value + noise))
            color = (color_val, color_val, color_val)
            pygame.draw.line(screen, color, (x, 0), (x, HEIGHT))
    else:
        # For the right side, fill from the boundary to the right edge.
        # t goes from 0 at x=avg_curve_x (at the curve) to 1 at x=WIDTH.
        for x in range(int(avg_curve_x), WIDTH):
            t = (x - avg_curve_x) / (WIDTH - avg_curve_x)
            value = int(base_value + t * (target_value - base_value))
            noise = random.randint(-noise_range, noise_range)
            color_val = max(0, min(255, value + noise))
            color = (color_val, color_val, color_val)
            pygame.draw.line(screen, color, (x, 0), (x, HEIGHT))
    
    if bluedot:
        pygame.draw.circle(screen, (0, 0, 80), (800, 450), 300)
