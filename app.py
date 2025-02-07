import pygame
import random
import sys
import math
import numpy as np
from settings import *
from helpers import *

# These are the animation scenes for the show


def scene_1(screen):
    # Black screen
    screen.fill((0, 0, 0))


def scene_2(screen):
    # TV Static
    amplitude = random.randint(10, 30)
    step = random.randint(5, 40)
    num_lines = random.randint(17, 56)
    baseline_y_positions = [random.randint(
        0, HEIGHT) for _ in range(num_lines)]

    screen.fill((0, 0, 0))
    for base_y in baseline_y_positions:
        points = generate_static_line_points(base_y, amplitude, step, WIDTH)
        pygame.draw.lines(screen, (100, 100, 100), False, points, 1)


def scene_3(screen):
    # TV Static with moving blue circle

    # Random parameters for TV static effect
    amplitude = random.randint(10, 30)
    step = random.randint(5, 40)
    num_lines = random.randint(17, 56)
    baseline_y_positions = [random.randint(
        0, HEIGHT) for _ in range(num_lines)]

    screen.fill((0, 0, 0))
    # Define the circle's radius (almost full height)
    radius = int(HEIGHT * 0.45)

    # Initialize the circle's x-position if not already done.
    # It starts off-screen to the right.
    if not hasattr(scene_3, "circle_x"):
        scene_3.circle_x = WIDTH + radius

    # Define a speed (pixels per frame) and update the circle's position.
    speed = 20
    scene_3.circle_x -= speed

    # If the circle has completely moved off the left side, reset it to the right.
    if scene_3.circle_x < -radius:
        scene_3.circle_x = WIDTH + radius

    # Use the updated x-position to define the circle's center.
    center = (scene_3.circle_x, HEIGHT // 2)

    # Draw the blue circle in the background.
    pygame.draw.circle(screen, (0, 0, 80), center, radius)

    # Draw the TV static lines on top of the circle.
    for base_y in baseline_y_positions:
        points = generate_static_line_points(base_y, amplitude, step, WIDTH)
        pygame.draw.lines(screen, (100, 100, 100), False, points, 1)


def scene_4(screen):
    half_screen_scene(screen, "left", False)


def scene_5(screen):
    half_screen_scene(screen, "right", False)


def scene_6(screen):
    half_screen_scene(screen, "left", True)


def scene_7(screen):
    half_screen_scene(screen, "right", True)


def scene_8(screen):
    """Game of Life simulation: 10x10 pixel gray squares on a gray background."""
    # Fill the background with gray.
    screen.fill((0, 0, 0))

    # Define cell and grid size.
    cell_size = 10
    grid_width = WIDTH // cell_size
    grid_height = HEIGHT // cell_size

    # Initialize the grid on the first call.
    if not hasattr(scene_8, "grid"):
        # Create a grid with a 20% chance for a cell to be alive.
        scene_8.grid = [
            [1 if random.random() < 0.1 else 0 for _ in range(grid_width)]
            for _ in range(grid_height)
        ]

    # Draw live cells as 10x10 pixel rectangles.
    live_color = (200, 200, 200)  # Color for live cells (gray)
    for y in range(grid_height):
        for x in range(grid_width):
            if scene_8.grid[y][x]:
                rect = pygame.Rect(x * cell_size, y *
                                   cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, live_color, rect)

    # Compute the next generation of the grid using Conway's Game of Life rules.
    new_grid = [[0] * grid_width for _ in range(grid_height)]
    for y in range(grid_height):
        for x in range(grid_width):
            live_neighbors = 0
            # Check the 8 neighbors.
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue  # Skip the cell itself.
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < grid_width and 0 <= ny < grid_height:
                        live_neighbors += scene_8.grid[ny][nx]
            # Apply Conway's rules:
            if scene_8.grid[y][x] == 1:
                # Any live cell with fewer than two or more than three live neighbors dies.
                if live_neighbors < 2 or live_neighbors > 3:
                    new_grid[y][x] = 0
                else:
                    new_grid[y][x] = 1
            else:
                # Any dead cell with exactly three live neighbors becomes alive.
                if live_neighbors == 3:
                    new_grid[y][x] = 1
                else:
                    new_grid[y][x] = 0

    # Update the grid for the next frame.
    scene_8.grid = new_grid


def scene_9(screen):
    # Cracked screen effect: a broken projector look with glitch-colored vertical stripes.
    screen.fill((0, 0, 0))

    # Initialize persistent state on first call.
    if not hasattr(scene_9, "initialized"):
        # Random band width between 200 and 400 pixels.
        scene_9.band_width = random.randint(200, 400)
        # Center the band horizontally with an additional random offset.
        scene_9.left_bound = (WIDTH - scene_9.band_width) // 2 + random.randint(
            -800, 800
        )
        scene_9.right_bound = scene_9.left_bound + scene_9.band_width
        # Decide on the total number of glitch stripes to generate.
        scene_9.total_stripes = random.randint(30, 70)
        # List to store each stripe as (x_coordinate, color).
        scene_9.stripes = []
        scene_9.initialized = True

    # List of glitch colors.
    glitch_colors = [
        (57, 255, 20),  # Neon green
        (255, 20, 147),  # Neon pink
        (255, 255, 255),  # White
        (0, 0, 139),  # Deep blue
    ]

    # Each frame, if we haven't reached the total count, add a random number (between 1 and 10) of new stripes.
    num_to_add = random.randint(1, 10)
    stripes_added = 0
    while len(scene_9.stripes) < scene_9.total_stripes and stripes_added < num_to_add:
        # Use a Gaussian to bias x positions toward the center of the band.
        x_offset = int(random.gauss(
            scene_9.band_width / 2, scene_9.band_width / 6))
        # Clamp x_offset to valid values within the band.
        x_offset = max(0, min(scene_9.band_width - 1, x_offset))
        # Translate to a screen x-coordinate.
        x_coord = scene_9.left_bound + x_offset
        # Choose a random color from the glitch palette.
        color = random.choice(glitch_colors)
        scene_9.stripes.append((x_coord, color))
        stripes_added += 1

    # Draw all stripes as thin vertical lines.
    for x_coord, color in scene_9.stripes:
        pygame.draw.line(screen, color, (x_coord, 0), (x_coord, HEIGHT), 1)


def scene_q(screen):
    screen.fill((0, 0, 0))

    # On the very first call after Q is pressed, generate the bitmap and initial state.
    if not hasattr(scene_q, "initialized"):
        # Random dimensions for the bitmap.
        rect_width = random.randint(400, 1200)
        rect_height = random.randint(50, 250)

        # Create a new surface for the bitmap.
        bitmap = pygame.Surface((rect_width, rect_height))

        # Choose a random gradient direction.
        # Options: "top_to_bottom", "bottom_to_top", "left_to_right", "right_to_left",
        # "diagonal_tl_br" (top-left to bottom-right), "diagonal_tr_bl" (top-right to bottom-left)
        directions = [
            "top_to_bottom",
            "bottom_to_top",
            "left_to_right",
            "right_to_left",
            "diagonal_tl_br",
            "diagonal_tr_bl",
        ]
        direction = random.choice(directions)

        # Choose start and end grayscale values.
        start_value = random.randint(0, 100)
        end_value = random.randint(155, 255)

        # Fill the bitmap pixel-by-pixel with a gradient plus noise.
        for y in range(rect_height):
            for x in range(rect_width):
                # Compute the gradient fraction t based on the chosen direction.
                if direction == "top_to_bottom":
                    t = y / (rect_height - 1) if rect_height > 1 else 0
                elif direction == "bottom_to_top":
                    t = 1 - y / (rect_height - 1) if rect_height > 1 else 0
                elif direction == "left_to_right":
                    t = x / (rect_width - 1) if rect_width > 1 else 0
                elif direction == "right_to_left":
                    t = 1 - x / (rect_width - 1) if rect_width > 1 else 0
                elif direction == "diagonal_tl_br":
                    t = (
                        ((x / (rect_width - 1)) + (y / (rect_height - 1))) / 2
                        if rect_width > 1 and rect_height > 1
                        else 0
                    )
                elif direction == "diagonal_tr_bl":
                    t = (
                        (
                            ((rect_width - 1 - x) / (rect_width - 1))
                            + (y / (rect_height - 1))
                        )
                        / 2
                        if rect_width > 1 and rect_height > 1
                        else 0
                    )
                else:
                    t = 0

                # Interpolate between start_value and end_value.
                base_value = int(start_value + t * (end_value - start_value))
                # Add random noise.
                noise = random.randint(-20, 20)
                pixel_value = max(0, min(255, base_value + noise))
                # Set the pixel (using a grayscale color).
                bitmap.set_at((x, y), (pixel_value, pixel_value, pixel_value))

        # Choose a random starting position on the screen.
        pos_x = random.randint(50, 1400)
        pos_y = random.randint(50, 700)

        # Store persistent state.
        scene_q.bitmap = bitmap
        scene_q.start_pos = (pos_x, pos_y)
        # The list of copies starts with the first (original) position.
        scene_q.copies = [scene_q.start_pos]
        # How many total copies will be drawn (including the first one)?
        scene_q.target_copies = random.randint(5, 15)
        # Time stamp for when the last copy was added.
        scene_q.last_copy_time = pygame.time.get_ticks()
        scene_q.initialized = True

    # Blit all copies (each copy remains drawn).
    for pos in scene_q.copies:
        screen.blit(scene_q.bitmap, pos)

    # Check if we need to add another copy.
    current_time = pygame.time.get_ticks()
    if len(scene_q.copies) < scene_q.target_copies:
        # If 100ms have passed since the last copy was added, add another.
        if current_time - scene_q.last_copy_time >= 100:
            # The new copy is drawn 30 pixels to the right and 30 pixels down from the last copy.
            last_x, last_y = scene_q.copies[-1]
            new_pos = (last_x + 30, last_y + 30)
            scene_q.copies.append(new_pos)
            scene_q.last_copy_time = current_time




def scene_w(screen):
    """Fills the screen with a grid of 30x30 pixel letters.
    Initially, every cell shows ".", and on each frame there is a chance for a cell
    to change to a glitch character. Once a cell changes, it remains that way.
    Additionally, a pulsating ripple effect is applied:
      - The ripple center is fixed at the grid’s center.
      - A global offset vector oscillates from 0 to 100 px in a pulsating, breathing motion.
        When the pulsation returns to 0, the direction is changed.
      - Each cell’s drawn offset is the global offset multiplied by a factor that
        decreases with its Chebyshev distance from the center (using 40 as the maximum distance).
    Every 1500 frames, the grid resets to white dots.
    """
    # Fill background black.
    screen.fill((0, 0, 0))
    cell_size = 30

    # Initialize persistent state in a dictionary.
    if not hasattr(scene_w, "state"):
        scene_w.state = {}
        cols = WIDTH // cell_size
        rows = HEIGHT // cell_size
        # Create the grid: each cell is a dict with 'letter' and 'color'
        scene_w.state["grid"] = [
            [{'letter': ".", 'color': (255, 255, 255)} for _ in range(cols)]
            for _ in range(rows)
        ]
        scene_w.state["font"] = pygame.font.SysFont("BarCode", cell_size, bold=True)
        scene_w.state["cell_size"] = cell_size
        scene_w.state["cols"] = cols
        scene_w.state["rows"] = rows
        # Fixed ripple center at the grid's center.
        scene_w.state["ripple_center"] = (cols / 2.0, rows / 2.0)
        # Fixed pulsation direction (angle in radians); will change each time the pulsation returns to 0.
        scene_w.state["pulsate_angle"] = random.uniform(0, 2 * math.pi)
        # Flag to prevent multiple changes per cycle.
        scene_w.state["angle_changed"] = False
        # Frame counter to trigger periodic resets.
        scene_w.state["frame_counter"] = 0

    state = scene_w.state
    grid = state["grid"]
    cols = state["cols"]
    rows = state["rows"]
    font = state["font"]

    # Increment frame counter; every 1500 frames, reset the grid.
    state["frame_counter"] += 1
    if state["frame_counter"] >= 1500:
        for r in range(rows):
            for c in range(cols):
                grid[r][c]['letter'] = "."
                grid[r][c]['color'] = (255, 255, 255)
        state["frame_counter"] = 0

    # With 90% probability per frame, update one random cell (only those that are still ".")
    if random.random() < 0.9:
        default_cells = [(r, c) for r in range(rows) for c in range(cols)
                         if grid[r][c]['letter'] == "."]
        if default_cells:
            r, c = random.choice(default_cells)
            glitch_chars = [";", "!", ":", "\"", "^", "(", ")", "$", "%", "#", ".", ".", ".", "."]
            new_letter = random.choice(glitch_chars)
            glitch_colors = [
                (57, 255, 20),    # Neon green
                (255, 20, 147),   # Neon pink
                (255, 255, 255),  # White
                (0, 0, 139)       # Deep blue
            ]
            if random.random() < 0.3:
                new_color = random.choice(glitch_colors)
            else:
                new_color = (255, 255, 255)
            grid[r][c]['letter'] = new_letter
            grid[r][c]['color'] = new_color

    # --- Pulsating Ripple Effect ---
    # The ripple center remains fixed at the grid center.
    ripple_center = state["ripple_center"]

    # Compute a pulsating magnitude that oscillates smoothly from 0 to 100 px (period = 3 seconds).
    t = pygame.time.get_ticks() / 1000.0
    period = 3.0
    pulsate_magnitude = ((math.sin(2 * math.pi * t / period) + 1) / 2) * 100

    # When the magnitude is near 0, update the pulsation angle (once per cycle).
    if pulsate_magnitude < 5 and not state["angle_changed"]:
        state["pulsate_angle"] = random.uniform(0, 2 * math.pi)
        state["angle_changed"] = True
    elif pulsate_magnitude >= 5:
        state["angle_changed"] = False

    pulsate_angle = state["pulsate_angle"]
    global_offset_x = math.cos(pulsate_angle) * pulsate_magnitude
    global_offset_y = math.sin(pulsate_angle) * pulsate_magnitude

    # Define a scaling function: cells at distance 0 get full offset; those farther away get reduced.
    def scale_for_distance(d):
        return max(0, 1 - (d / 40.0))

    # --- Draw the Grid with the Pulsating Ripple Offset ---
    for r in range(rows):
        for c in range(cols):
            cell = grid[r][c]
            orig_x = c * cell_size
            orig_y = r * cell_size
            # Chebyshev distance from the center.
            d = max(abs(c - ripple_center[0]), abs(r - ripple_center[1]))
            scale = scale_for_distance(d)
            offset_x = global_offset_x * scale
            offset_y = global_offset_y * scale
            final_x = orig_x + offset_x
            final_y = orig_y + offset_y
            letter_surface = font.render(cell['letter'], True, cell['color'])
            screen.blit(letter_surface, (final_x, final_y))

def scene_e(screen):
    """Generates an evolving Mandelbrot view that continuously zooms and drifts.
    Colors are mapped using a blue-to-black gradient with a nonlinear (sqrt) scaling,
    emphasizing the fractal’s boundary details.
    """
    screen.fill((0, 0, 0))
    
    # Use a low resolution for speed.
    res_factor = 4
    img_width = WIDTH // res_factor
    img_height = HEIGHT // res_factor

    # Initialize persistent state if needed.
    if not hasattr(scene_e, "state"):
        state = {}
        # Pick a random starting center from a region known to contain fractal detail.
        state["center"] = (random.uniform(-2.0, 1.0), random.uniform(-1.0, 1.0))
        state["zoom"] = random.uniform(1, 50)  # Starting zoom factor.
        state["max_iter"] = 50               # Increased iteration count for more detail.
        scene_e.state = state
    state = scene_e.state

    # Update the zoom factor slowly.
    zoom_factor = 1.050  # 0.5% increase per frame.
    state["zoom"] *= zoom_factor

    # Drift the center slightly each frame for evolving visuals.
    cx, cy = state["center"]
    cx += random.uniform(-0.002, 0.002)
    cy += random.uniform(-0.002, 0.002)
    state["center"] = (-0.74364, 0.13183)

    # Compute the view rectangle in the complex plane.
    view_width = 3.5 / state["zoom"]
    view_height = view_width * (img_height / img_width)
    center_x, center_y = state["center"]
    x_min = center_x - view_width / 2
    x_max = center_x + view_width / 2
    y_min = center_y - view_height / 2
    y_max = center_y + view_height / 2

    # Create coordinate arrays.
    xs = np.linspace(x_min, x_max, img_width)
    ys = np.linspace(y_min, y_max, img_height)
    X, Y = np.meshgrid(xs, ys)
    C = X + 1j * Y
    Z = np.zeros(C.shape, dtype=complex)
    max_iter = state["max_iter"]
    iters = np.zeros(C.shape, dtype=int)
    mask = np.full(C.shape, True, dtype=bool)

    # Mandelbrot iteration loop.
    for i in range(max_iter):
        Z[mask] = Z[mask] * Z[mask] + C[mask]
        mask_new = np.abs(Z) <= 2.0
        escaped = mask & (~mask_new)
        iters[escaped] = i
        mask = mask_new
    iters[mask] = max_iter

    # Color mapping: Use a blue-to-black gradient with sqrt scaling.
    # Points that never escape (n == max_iter) are black.
    # Otherwise, we compute f = n/max_iter, then blue = 255*(1 - sqrt(f)).
    def mandelbrot_color(n):
        if n == max_iter:
            return (0, 0, 0)
        else:
            f = n / max_iter
            blue_value = int(255 * (1 - math.sqrt(f)))
            return (0, 0, blue_value)

    # Build an image array.
    img = np.empty((img_height, img_width, 3), dtype=np.uint8)
    for i in range(img_height):
        for j in range(img_width):
            img[i, j] = mandelbrot_color(iters[i, j])

    # Create a Pygame surface from the image array.
    # Note: Transpose because Pygame expects (width, height, channels).
    mandelbrot_surface = pygame.surfarray.make_surface(np.transpose(img, (1, 0, 2)))
    # Scale the low-resolution image to the full display size.
    mandelbrot_surface = pygame.transform.scale(mandelbrot_surface, (WIDTH, HEIGHT))
    screen.blit(mandelbrot_surface, (0, 0))



def scene_r(screen):
    """Placeholder: Fill screen with a blueish tint."""
    screen.fill((50, 50, 100))


def scene_t(screen):
    """Placeholder: Fill screen with a warm color."""
    screen.fill((150, 150, 0))


def scene_z(screen):
    """Placeholder: Fill screen with a purple tone."""
    screen.fill((150, 0, 150))


def scene_u(screen):
    """Placeholder: Fill screen with a teal tone."""
    screen.fill((0, 150, 150))


def scene_i(screen):
    """Placeholder: Fill screen with a soft green tone."""
    screen.fill((100, 200, 100))


def scene_o(screen):
    """Placeholder: Fill screen with a pinkish tone."""
    screen.fill((200, 100, 200))


def main():
    # Initialize pygame stuff
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    pygame.display.set_caption("Pygame App - Scene Animations")
    clock = pygame.time.Clock()

    # Map keys to scene functions.
    scene_map = {
        pygame.K_1: scene_1,
        pygame.K_2: scene_2,
        pygame.K_3: scene_3,
        pygame.K_4: scene_4,
        pygame.K_5: scene_5,
        pygame.K_6: scene_6,
        pygame.K_7: scene_7,
        pygame.K_8: scene_8,
        pygame.K_9: scene_9,
        pygame.K_q: scene_q,
        pygame.K_w: scene_w,
        pygame.K_e: scene_e,
        pygame.K_r: scene_r,
        pygame.K_t: scene_t,
        pygame.K_z: scene_z,
        pygame.K_u: scene_u,
        pygame.K_i: scene_i,
        pygame.K_o: scene_o,
    }

    # Start with scene_1 (TV static lines)
    current_scene = scene_1

    # Define a helper dictionary for resetting persistent state.
    # Each key maps to a tuple: (scene_function, [list of attribute names to delete]).
    reset_map = {
        pygame.K_9: (
            scene_9,
            [
                "initialized",
                "band_width",
                "left_bound",
                "right_bound",
                "total_stripes",
                "stripes",
            ],
        ),
        pygame.K_8: (scene_8, ["grid"]),
        pygame.K_q: (
            scene_q,
            [
                "initialized",
                "bitmap",
                "start_pos",
                "copies",
                "target_copies",
                "last_copy_time",
            ],
        ),
    }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key in scene_map:
                    current_scene = scene_map[event.key]

                    # If the pressed key requires resetting persistent state, do so.
                    if event.key in reset_map:
                        scene_func, attr_list = reset_map[event.key]
                        for attr in attr_list:
                            if hasattr(scene_func, attr):
                                delattr(scene_func, attr)

        # Render the current scene.
        current_scene(screen)

        pygame.display.flip()
        clock.tick(20)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
