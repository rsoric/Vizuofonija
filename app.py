import pygame
import random
import sys
import math
import numpy as np
from settings import *
from helpers import *

# These are the animation scenes for the show


def scene_1(screen):
    import pygame
    # Fill the screen with black.
    screen.fill((0, 0, 0))
    
    # Load the logo with transparency preserved.
    logo = pygame.image.load("logo.png").convert_alpha()
    
    # Scale the logo to 500x500 pixels.
    logo_scaled = pygame.transform.smoothscale(logo, (500, 500))
    
    # Calculate the position to center the logo.
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    pos_x = (screen_width - 500) // 2
    pos_y = (screen_height - 500) // 2
    
    # Blit the scaled logo to the screen.
    screen.blit(logo_scaled, (pos_x, pos_y))



def scene_2(screen):
    # TV Static
    amplitude = random.randint(10, 30)
    step = random.randint(5, 40)
    num_lines = random.randint(17, 56)
    baseline_y_positions = [random.randint(0, HEIGHT) for _ in range(num_lines)]

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
    baseline_y_positions = [random.randint(0, HEIGHT) for _ in range(num_lines)]

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
    """
    Scene 4: Consolidated scene that randomly selects a configuration.

    On its first call (or after a reset), it randomly selects:
      - A side: "left" or "right"
      - A flag: False or True

    Then it calls half_screen_scene(screen, side, flag) with the chosen configuration.
    """
    import random

    # Create a persistent configuration so that the choice remains constant
    # until the scene is reset.
    if not hasattr(scene_4, "config"):
        side = random.choice(["left", "right"])
        flag = random.choice([False, True])
        scene_4.config = (side, flag)

    # Call the half_screen_scene with the randomly chosen parameters.
    half_screen_scene(screen, scene_4.config[0], scene_4.config[1])


def scene_5(screen):
    """
    Scene 5: Displays 25 random swirls on a black background.

    Each swirl:
      - Is drawn as a spiral using a gradient of line thickness (thick at the start, thin at the end).
      - Has a random position on the screen.
      - Twists at its own random speed and with its own twist multiplier.
      - Has a 20% chance of being drawn in deep blue, otherwise in a gray tone.
      - Has a random rotation (0 to 360 degrees) that rotates the entire swirl.
      - Disappears when its twist (angle) exceeds a random threshold.

    When a swirl disappears, a new one is immediately created at a random position.
    """
    import math, random, pygame

    # --- Helper: Create a new swirl ---
    def new_swirl(width, height):
        # A swirl is a dictionary with:
        #   "x", "y": its fixed center (randomly chosen within the screen),
        #   "angle": current twist (starts at 0),
        #   "speed": twist speed (radians per frame),
        #   "twist_factor": multiplier that affects how sharply it twists,
        #   "threshold": twist threshold (when reached, the swirl is removed),
        #   "color": the swirl's color (20% chance deep blue, else gray),
        #   "rotation": a fixed rotation offset (0 to 2π radians) applied to the spiral.
        color = (0, 0, 139) if random.random() < 0.2 else (100, 100, 100)
        return {
            "x": random.uniform(0, width),
            "y": random.uniform(0, height),
            "angle": 0,
            "speed": random.uniform(0.05, 0.6),  # Twist speed.
            "twist_factor": random.uniform(1.0, 5.0),  # Affects twisting sharpness.
            "threshold": random.uniform(
                4 * math.pi, 6 * math.pi
            ),  # Increased threshold.
            "color": color,
            "rotation": random.uniform(
                0, 2 * math.pi
            ),  # Random rotation (0 to 360 degrees).
        }

    # Clear the screen.
    screen.fill((0, 0, 0))
    width = screen.get_width()
    height = screen.get_height()

    # Initialize persistent swirls list on the first call.
    if not hasattr(scene_5, "swirls"):
        scene_5.swirls = [new_swirl(width, height) for _ in range(25)]

    # Update and draw each swirl.
    for swirl in scene_5.swirls:
        # Update the twist angle.
        swirl["angle"] += swirl["speed"]

        # Build the spiral as a list of points.
        points = []
        steps = 150  # Number of sample points along the spiral.
        scale = 10  # Scale factor for the spiral's size.
        for i in range(steps):
            # t is affected by the swirl's twist_factor.
            t = swirl["angle"] * swirl["twist_factor"] * i / (steps - 1)
            r = scale * t  # The spiral's radius grows with t.
            # Add the swirl's fixed rotation offset to t.
            x = swirl["x"] + r * math.cos(t + swirl["rotation"])
            y = swirl["y"] + r * math.sin(t + swirl["rotation"])
            points.append((int(x), int(y)))

        # Draw the spiral segment by segment with a gradient thickness.
        max_seg_thickness = 10  # Maximum (thick) line thickness at the start.
        min_seg_thickness = 1  # Minimum (thin) line thickness at the end.
        for i in range(len(points) - 1):
            # Linearly interpolate thickness from max_seg_thickness to min_seg_thickness.
            seg_thickness = int(
                max_seg_thickness
                - (max_seg_thickness - min_seg_thickness) * i / (len(points) - 2)
            )
            pygame.draw.line(
                screen, swirl["color"], points[i], points[i + 1], seg_thickness
            )

    # Remove swirls that have twisted past their threshold.
    scene_5.swirls = [
        swirl for swirl in scene_5.swirls if swirl["angle"] <= swirl["threshold"]
    ]

    # If any swirl has disappeared, add new ones to maintain (currently) 10 swirls.
    while len(scene_5.swirls) < 10:
        scene_5.swirls.append(new_swirl(width, height))


def scene_6(screen):
    """
    Scene 6:
      - Displays a small white dot in the center of a black screen that slowly grows.
      - After a random interval between 3 and 10 seconds, triggers a strobe effect:
           • Two quick white flashes, or (with 30% chance) a double strobe (four flashes).
      - After the strobe sequence finishes, the scene resets and starts a new cycle.
    """
    import pygame, random, math

    # Use pygame.time.get_ticks() to measure time (in milliseconds).
    current_time = pygame.time.get_ticks()

    # If no persistent state exists, initialize for the "growing" phase.
    if not hasattr(scene_6, "phase"):
        scene_6.phase = "growing"
        scene_6.phase_start = current_time
        scene_6.target_interval = random.randint(
            500, 8000
        )  # between 3 and 10 seconds (ms)
        scene_6.base_radius = 1  # starting radius in pixels
        scene_6.growth_rate = 0.009  # pixels per millisecond

    if scene_6.phase == "growing":
        # Growing phase: Increase the dot's radius over time.
        elapsed = current_time - scene_6.phase_start
        radius = scene_6.base_radius + scene_6.growth_rate * elapsed

        # Clear the screen and draw the growing white dot at the center.
        screen.fill((0, 0, 0))
        center = (screen.get_width() // 2, screen.get_height() // 2)
        pygame.draw.circle(screen, (255, 255, 255), center, int(radius))

        # Once the target interval has elapsed, switch to the strobe phase.
        if elapsed >= scene_6.target_interval:
            scene_6.phase = "strobe"
            scene_6.phase_start = current_time
            # Decide on strobe parameters:
            # With 30% chance, do a "double strobe" (4 flashes); otherwise, 2 flashes.
            scene_6.num_flashes = 4 if random.random() < 0.3 else 2
            scene_6.flash_duration = 80  # duration of each flash in ms
            scene_6.gap_duration = 80  # gap between flashes in ms
            scene_6.total_strobe = (
                scene_6.num_flashes * scene_6.flash_duration
                + (scene_6.num_flashes - 1) * scene_6.gap_duration
            )

    elif scene_6.phase == "strobe":
        # Strobe phase: Determine if we are in a flash "on" period.
        elapsed_strobe = current_time - scene_6.phase_start
        flash_on = False
        for i in range(scene_6.num_flashes):
            flash_start = i * (scene_6.flash_duration + scene_6.gap_duration)
            flash_end = flash_start + scene_6.flash_duration
            if flash_start <= elapsed_strobe < flash_end:
                flash_on = True
                break

        # Fill the screen white during a flash; otherwise, black.
        screen.fill((200, 200, 200) if flash_on else (0, 0, 0))

        # Once the strobe sequence is complete, reset the scene for a new cycle.
        if elapsed_strobe >= scene_6.total_strobe:
            # Delete persistent attributes so that on the next frame, a new cycle is initialized.
            for attr in [
                "phase",
                "phase_start",
                "target_interval",
                "base_radius",
                "growth_rate",
                "num_flashes",
                "flash_duration",
                "gap_duration",
                "total_strobe",
            ]:
                if hasattr(scene_6, attr):
                    delattr(scene_6, attr)


def scene_7(screen):
    """
    Scene 7: Randomized Kaleidoscope with Glitch Effects and Dynamic Horizontal Scan Lines

    - A base pattern of deep blue random lines is generated on a black surface.
      This base pattern is updated only every few frames (skipping 1–6 frames randomly).
    - A kaleidoscopic effect is created by rotating the base pattern into a random number
      of sectors (between 6 and 12), with a slight random rotation and positional offset to
      produce a glitchy effect.
    - Overlaid on the pattern are dark gray horizontal scan lines. Every 10–25 frames the
      number of evenly distributed scan lines is randomly reselected between 18 and 25.
    """
    import pygame, random, math

    # Clear the screen.
    screen.fill((0, 0, 0))
    width = screen.get_width()
    height = screen.get_height()

    # --- Update the Base Pattern (Random Lines) with Frame Skipping ---
    # Initialize persistent variables if not already present.
    if not hasattr(scene_7, "skip_counter"):
        scene_7.skip_counter = 0
        scene_7.base = None  # The base pattern surface.
    if scene_7.skip_counter <= 0:
        # Generate a new base pattern.
        base = pygame.Surface((width, height))
        base.fill((0, 0, 0))
        num_lines = random.randint(50, 150)
        for _ in range(num_lines):
            start = (random.randint(0, width), random.randint(0, height))
            end = (random.randint(0, width), random.randint(0, height))
            thickness = random.randint(1, 5)
            pygame.draw.line(base, (0, 0, 139), start, end, thickness)
        scene_7.base = base
        # Set skip_counter to a random value between 1 and 6 frames.
        scene_7.skip_counter = random.randint(1, 6)
    else:
        scene_7.skip_counter -= 1
        base = scene_7.base

    # --- Create the Kaleidoscope Effect ---
    # Choose a random number of sectors between 6 and 12.
    n = random.randint(6, 12)
    wedge_angle = 360 / n  # Full circle division.

    # Create a surface with per-pixel alpha for the kaleidoscope.
    kaleido = pygame.Surface((width, height), pygame.SRCALPHA)
    center = (width // 2, height // 2)
    for i in range(n):
        # Base rotation for the sector.
        base_angle = i * wedge_angle
        # Add a slight random glitch rotation offset (in degrees).
        glitch_offset = random.uniform(-2, 2)
        angle = base_angle + glitch_offset

        # Rotate the base pattern.
        rotated = pygame.transform.rotate(base, angle)
        # Get its rect, centered at the screen center.
        rect = rotated.get_rect(center=center)
        # Add a small random positional glitch.
        pos_glitch = (random.randint(-5, 5), random.randint(-5, 5))
        rect.x += pos_glitch[0]
        rect.y += pos_glitch[1]

        # Blit the rotated (glitched) sector onto the kaleidoscope surface.
        kaleido.blit(rotated, rect)

    # Blit the kaleidoscope pattern onto the screen.
    screen.blit(kaleido, (0, 0))

    # --- Update and Draw the Horizontal Scan Lines ---
    # Persistent scan line parameters.
    if not hasattr(scene_7, "scan_line_timer"):
        scene_7.scan_line_timer = 0
        scene_7.scan_line_interval = random.randint(10, 25)  # Frames between updates.
        scene_7.scan_line_count = random.randint(18, 25)  # Number of scan lines.
    scene_7.scan_line_timer += 1
    if scene_7.scan_line_timer >= scene_7.scan_line_interval:
        scene_7.scan_line_timer = 0
        scene_7.scan_line_interval = random.randint(10, 25)
        scene_7.scan_line_count = random.randint(18, 25)
    # Draw horizontal scan lines using a dark gray color.
    for i in range(scene_7.scan_line_count):
        # Evenly space the lines vertically.
        y = int((i + 0.5) * height / scene_7.scan_line_count)
        pygame.draw.line(screen, (40, 40, 40), (0, y), (width, y), 1)


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
            [1 if random.random() < 0.3 else 0 for _ in range(grid_width)]
            for _ in range(grid_height)
        ]

    # Draw live cells as 10x10 pixel rectangles.
    live_color = (200, 200, 200)  # Color for live cells (gray)
    for y in range(grid_height):
        for x in range(grid_width):
            if scene_8.grid[y][x]:
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
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
        x_offset = int(random.gauss(scene_9.band_width / 2, scene_9.band_width / 6))
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
    import random, math, pygame

    # Clear the screen.
    screen.fill((0, 0, 0))
    current_time = pygame.time.get_ticks()
    width = screen.get_width()
    height = screen.get_height()

    # --- Helper: Create a new gradient group ---
    def new_group():
        # Random dimensions for the bitmap.
        rect_width = random.randint(400, 1200)
        rect_height = random.randint(50, 250)

        # Create a new surface for the bitmap.
        bitmap = pygame.Surface((rect_width, rect_height))

        # Decide on color mode: 10% chance for blue mode.
        blue_mode = True if random.random() < 0.1 else False

        # Choose a random gradient direction.
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

                base_value = int(start_value + t * (end_value - start_value))
                noise = random.randint(-20, 20)
                pixel_value = max(0, min(255, base_value + noise))
                if blue_mode:
                    # In blue mode, use blue channel only.
                    bitmap.set_at((x, y), (0, 0, pixel_value))
                else:
                    # Otherwise, use a grayscale value.
                    bitmap.set_at((x, y), (pixel_value, pixel_value, pixel_value))

        # Choose a random starting position on the screen.
        pos_x = random.randint(10, 1000)
        pos_y = random.randint(10, 700)

        # Build the group dictionary.
        group = {
            "bitmap": bitmap,
            "start_pos": (pos_x, pos_y),
            "copies": [(pos_x, pos_y)],  # Start with the original position.
            "target_copies": random.randint(5, 15),  # Total copies for this gradient.
            "last_copy_time": current_time,
        }
        return group

    # Initialize the persistent list of groups if not already present.
    if not hasattr(scene_q, "groups"):
        scene_q.groups = [new_group()]

    # Draw all groups: for each group, blit its bitmap at each stored copy position.
    for group in scene_q.groups:
        for pos in group["copies"]:
            screen.blit(group["bitmap"], pos)

    # Update the most-recent (last) group if it hasn't reached its target copies.
    last_group = scene_q.groups[-1]
    if len(last_group["copies"]) < last_group["target_copies"]:
        if current_time - last_group["last_copy_time"] >= 100:
            last_x, last_y = last_group["copies"][-1]
            new_pos = (last_x + 30, last_y + 30)
            last_group["copies"].append(new_pos)
            last_group["last_copy_time"] = current_time
    else:
        # The last group is finished.
        # If we have fewer than 15 groups, simply add a new group.
        if len(scene_q.groups) < 15:
            scene_q.groups.append(new_group())
        else:
            # Otherwise, remove the oldest group (index 0) and add a new one.
            scene_q.groups.pop(0)
            scene_q.groups.append(new_group())

    # --- Reset the whole scene when 'q' is pressed ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        # Delete the persistent groups so the scene reinitializes.
        if hasattr(scene_q, "groups"):
            del scene_q.groups
        # Clear the screen.
        screen.fill((0, 0, 0))


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
            [{"letter": ".", "color": (255, 255, 255)} for _ in range(cols)]
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
                grid[r][c]["letter"] = "."
                grid[r][c]["color"] = (255, 255, 255)
        state["frame_counter"] = 0

    # With 90% probability per frame, update one random cell (only those that are still ".")
    if random.random() < 0.9:
        default_cells = [
            (r, c)
            for r in range(rows)
            for c in range(cols)
            if grid[r][c]["letter"] == "."
        ]
        if default_cells:
            r, c = random.choice(default_cells)
            glitch_chars = [
                ";",
                "!",
                ":",
                '"',
                "^",
                "(",
                ")",
                "$",
                "%",
                "#",
                ".",
                ".",
                ".",
                ".",
            ]
            new_letter = random.choice(glitch_chars)
            glitch_colors = [
                (57, 255, 20),  # Neon green
                (255, 20, 147),  # Neon pink
                (255, 255, 255),  # White
                (0, 0, 139),  # Deep blue
            ]
            if random.random() < 0.3:
                new_color = random.choice(glitch_colors)
            else:
                new_color = (255, 255, 255)
            grid[r][c]["letter"] = new_letter
            grid[r][c]["color"] = new_color

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
            letter_surface = font.render(cell["letter"], True, cell["color"])
            screen.blit(letter_surface, (final_x, final_y))


def scene_e(screen):
    """
    Scene E: Draws a set of parallel white wavy lines on a black background,
    with a cyclic highlight effect that changes the line thickness.

    On initialization (or after a reset), this scene randomly determines:
      - A rotation angle (theta) for the lines.
      - A constant spacing (between 40 and 100 pixels) for all lines.
      - A constant base thickness (between 1 and 3 pixels) for all lines.
      - A common wave deformation defined by:
            amplitude (60 to 120 pixels),
            frequency (10 to 15 complete cycles along the line),
            and a phase offset (between 1 and 3π radians).

    At render time, the scene cycles a "highlight" along the lines. For example,
    if the highlighted line is index 20, then:
      - Line 20 is drawn with a maximum thickness (e.g. 12 pixels).
      - Lines 19 and 21 are drawn with slightly less thickness.
      - Lines 18 and 22 are drawn with even less thickness,
        continuing outwards until 10 lines away, which revert to the base thickness.
    This highlight index is updated each frame so that the effect cycles.
    """
    import math, random, pygame
    import numpy as np

    width = screen.get_width()
    height = screen.get_height()

    # Reinitialize configuration if attributes are missing (first run or after reset).
    if not hasattr(scene_e, "lines"):
        # Choose a random angle between 0 and pi (0 to 180 degrees).
        theta = random.uniform(0, math.pi)
        # u: unit vector perpendicular to the lines.
        u = (math.cos(theta), math.sin(theta))
        # v: unit vector parallel to the lines.
        v = (-math.sin(theta), math.cos(theta))

        # Determine the range of offsets (d values) needed to cover the screen.
        # Each line is defined by: x*cos(theta) + y*sin(theta) = d.
        corners = [(0, 0), (width, 0), (0, height), (width, height)]
        d_values = [corner[0] * u[0] + corner[1] * u[1] for corner in corners]
        d_min = min(d_values)
        d_max = max(d_values)

        # Add a margin to ensure full coverage.
        margin = 100
        d_start = d_min - margin
        d_end = d_max + margin

        # Choose constant spacing and base thickness for all lines.
        spacing = random.uniform(40, 100)  # Spacing in pixels.
        base_thickness = random.randint(1, 3)  # Base thickness in pixels.

        # Generate the list of line offsets.
        lines = []
        d = d_start
        while d < d_end:
            lines.append((d, base_thickness))
            d += spacing

        # Set wave parameters: amplitude, frequency, and phase.
        wave_amp = random.uniform(60, 120)  # Amplitude in pixels.
        wave_freq = random.uniform(10, 15)  # Number of complete cycles along the line.
        wave_phase = random.uniform(1, 3 * math.pi)  # Phase shift in radians.

        # Store the configuration persistently.
        scene_e.lines = lines
        scene_e.theta = theta
        scene_e.u = u
        scene_e.v = v
        scene_e.wave_amp = wave_amp
        scene_e.wave_freq = wave_freq
        scene_e.wave_phase = wave_phase
        # Initialize the highlight index.
        scene_e.highlight_index = 0

    # Clear the screen.
    screen.fill((0, 0, 0))

    # Compute a diagonal length that guarantees coverage across the screen.
    diag = math.sqrt(width * width + height * height)

    # Number of sample points for drawing each curve.
    sample_count = 400

    # Parameters for the thickness cycling.
    highlight_range = 10  # Number of lines on each side to affect.
    max_thickness = 12  # Maximum thickness for the highlighted line.

    # Draw each wavy line.
    # We use enumerate() so we have an index for each line.
    for i, (d, base_thickness) in enumerate(scene_e.lines):
        # Compute dynamic thickness based on distance from the highlighted line.
        distance = abs(i - scene_e.highlight_index)
        if distance > highlight_range:
            dynamic_thickness = base_thickness
        else:
            # Linear interpolation: when distance == 0, thickness is max_thickness;
            # when distance == highlight_range, thickness reverts to base_thickness.
            dynamic_thickness = base_thickness + (max_thickness - base_thickness) * (
                1 - distance / highlight_range
            )

        # Build the wavy line as a polyline.
        t_values = np.linspace(-diag, diag, sample_count)
        points = []
        for t in t_values:
            # Compute the sine wave offset.
            offset = scene_e.wave_amp * math.sin(
                2 * math.pi * scene_e.wave_freq * ((t + diag) / (2 * diag))
                + scene_e.wave_phase
            )
            # Total offset along the u direction.
            total_offset = d + offset
            # Compute the point coordinates.
            x = total_offset * scene_e.u[0] + t * scene_e.v[0]
            y = total_offset * scene_e.u[1] + t * scene_e.v[1]
            points.append((int(x), int(y)))
        # Draw the wavy line with the computed dynamic thickness.
        pygame.draw.lines(
            screen, (255, 255, 255), False, points, int(dynamic_thickness)
        )

    # Update the highlight index so that the effect cycles.
    scene_e.highlight_index = (scene_e.highlight_index + 1) % len(scene_e.lines)


def scene_r(screen):
    """
    Scene R: Evolving Spirograph Visualization

    This visualization generates a spirograph (a type of hypotrochoid) with random parameters,
    drawn using 200 sample points. The spirograph is centered on the screen and evolves over time.
    When its internal evolution parameter reaches a randomly chosen threshold, the spirograph is discarded
    and a new one is generated. The drawing is rendered using a random line thickness (1 to 5) and either
    dark blue or white color.
    """
    import math, random, pygame

    # Clear the screen (black background).
    screen.fill((0, 0, 0))
    width = screen.get_width()
    height = screen.get_height()

    # Initialize spirograph parameters if not already done.
    if not hasattr(scene_r, "spiro"):
        # Center the spirograph.
        center = (width // 2, height // 2)
        # Choose random parameters for the spirograph.
        R = random.uniform(100, 600)  # Big circle radius.
        r = random.uniform(10, R - 10)  # Small circle radius (ensure r < R).
        l = random.uniform(30, r)  # Pen offset from the center of the small circle.
        thickness = random.randint(1, 3)  # Line thickness.
        color = random.choice(
            [(0, 0, 189), (255, 255, 255)]
        )  # Either dark blue or white.
        dt = random.uniform(0.4, 0.6)  # Time increment per frame.
        # Evolution threshold: when the spirograph has evolved beyond this value, it will be replaced.
        evolution_threshold = random.uniform(38 * math.pi, 42 * math.pi)

        # Store all parameters in a persistent dictionary.
        scene_r.spiro = {
            "center": center,
            "R": R,
            "r": r,
            "l": l,
            "thickness": thickness,
            "color": color,
            "current_t": 0.0,  # Current evolution parameter.
            "dt": dt,
            "evolution_threshold": evolution_threshold,
        }

    # Retrieve current spirograph parameters.
    spiro = scene_r.spiro
    # Increase the evolution parameter.
    spiro["current_t"] += spiro["dt"]

    # If the spirograph has evolved beyond its threshold, reinitialize.
    if spiro["current_t"] >= spiro["evolution_threshold"]:
        del scene_r.spiro  # Remove the current parameters.
        return  # On the next frame, new parameters will be generated.

    # Generate the spirograph points using the hypotrochoid formula.
    # Formula:
    #   x(t) = center_x + (R - r)*cos(t) + l*cos(((R - r)/r)*t)
    #   y(t) = center_y + (R - r)*sin(t) - l*sin(((R - r)/r)*t)
    steps = 600
    points = []
    for i in range(steps):
        # Sample t from 0 to current_t.
        t_val = spiro["current_t"] * i / (steps - 1)
        x = (
            spiro["center"][0]
            + (spiro["R"] - spiro["r"]) * math.cos(t_val)
            + spiro["l"] * math.cos(((spiro["R"] - spiro["r"]) / spiro["r"]) * t_val)
        )
        y = (
            spiro["center"][1]
            + (spiro["R"] - spiro["r"]) * math.sin(t_val)
            - spiro["l"] * math.sin(((spiro["R"] - spiro["r"]) / spiro["r"]) * t_val)
        )
        points.append((int(x), int(y)))

    # Draw the spirograph as a connected polyline.
    pygame.draw.lines(screen, spiro["color"], False, points, spiro["thickness"])


def scene_t(screen):
    """
    Scene T: Evolving full-screen heatmap via localized pulses.

    - The heatmap is defined on a fixed 70x70 grid.
    - At random intervals, a pulse is triggered at a random grid cell.
    - Each pulse evolves over its duration (from 0 to peak to 0) and affects nearby cells,
      with a linear fall-off in influence over a radius of 5 to 10 cells.
    - The grid values (clipped to [0,1]) are mapped to a purple-to-red palette:
          0 -> purple (128, 0, 128)
          1 -> red    (255, 0, 0)
    - The resulting 70x70 image is scaled to fill the screen.
    """
    import pygame, numpy as np, random, math

    # Define grid dimensions.
    grid_w, grid_h = 70, 70

    # Initialize persistent pulse list on first call.
    if not hasattr(scene_t, "pulses"):
        scene_t.pulses = []  # List of active pulses.

    # Get current time in milliseconds.
    current_time = pygame.time.get_ticks()

    # --- Pulse Management ---
    # Remove expired pulses.
    scene_t.pulses = [
        p for p in scene_t.pulses if current_time - p["start"] < p["duration"]
    ]

    # With a small probability, add a new pulse.
    # (Adjust probability as desired for more or less activity.)
    if random.random() < 0.35:
        # Choose a random cell (grid indices).
        pos_x = random.randint(0, grid_w - 1)
        pos_y = random.randint(0, grid_h - 1)
        # Duration in milliseconds (e.g., 2000 to 5000 ms).
        duration = random.randint(2000, 5000)
        # Influence radius: between 5 and 10 grid cells.
        radius = random.randint(3, 15)
        pulse = {
            "pos": (pos_x, pos_y),  # grid coordinate
            "start": current_time,  # timestamp in ms
            "duration": duration,  # total duration of the pulse
            "radius": radius,  # influence radius (in grid cells)
        }
        scene_t.pulses.append(pulse)

    # --- Compute the Grid Values ---
    # Start with a grid of zeros.
    grid = np.zeros((grid_h, grid_w), dtype=np.float32)

    # For each active pulse, add its contribution.
    for pulse in scene_t.pulses:
        elapsed = current_time - pulse["start"]
        T = pulse["duration"]
        # Intensity evolves as sin(pi * (elapsed/T)): 0 at start, peaks at T/2, then returns to 0.
        intensity = math.sin(math.pi * elapsed / T)
        cx, cy = pulse["pos"]  # center of the pulse in grid coordinates
        R = pulse["radius"]

        # Define a window around the pulse center.
        x_min = max(0, cx - R)
        x_max = min(grid_w - 1, cx + R)
        y_min = max(0, cy - R)
        y_max = min(grid_h - 1, cy + R)
        for i in range(x_min, x_max + 1):
            for j in range(y_min, y_max + 1):
                # Compute Euclidean distance from the pulse center.
                d = math.sqrt((i - cx) ** 2 + (j - cy) ** 2)
                if d <= R:
                    # Linear attenuation: maximum effect at the center, zero at distance R.
                    grid[j, i] += intensity * (1 - d / R)

    # Clip grid values to [0, 1].
    grid = np.clip(grid, 0, 1)

    # --- Map the Grid to a Purple-to-Red Palette ---
    # Purple (low value): (128, 0, 128)
    # Red (high value): (255, 0, 0)
    # Linear mapping:
    #   R = 128 + 127 * value
    #   G = 0
    #   B = 128 - 128 * value
    v = grid
    B_color = (255 * v).astype(np.uint8)
    G_color = np.zeros_like(B_color, dtype=np.uint8)
    R_color = np.zeros_like(B_color, dtype=np.uint8)
    # Build a (grid_h, grid_w, 3) color array.
    color_array = np.dstack((R_color, G_color, B_color))

    # --- Create a Surface from the Color Array and Scale It ---
    # Pygame expects a surface array with shape (width, height, 3) so transpose the array.
    heatmap_surface = pygame.surfarray.make_surface(
        np.transpose(color_array, (1, 0, 2))
    )
    # Scale the 70x70 surface to the full screen dimensions.
    screen_width, screen_height = screen.get_width(), screen.get_height()
    heatmap_scaled = pygame.transform.scale(
        heatmap_surface, (screen_width, screen_height)
    )

    # --- Blit the Heatmap onto the Screen ---
    screen.blit(heatmap_scaled, (0, 0))


def scene_z(screen):
    """
    Scene Z: Pixel Rain with Trailing Effects

    - The background is a purple tone (150, 0, 150).
    - Many "rain drops" (white squares) fall from above the screen.
    - Each drop is a square with a random size (2x2 to 10x10) and a random falling speed.
    - Each drop leaves a trail of up to 10 squares behind it, with decreasing opacity.
    """
    import pygame, random

    # Fill the background with a purple tone.
    screen.fill((0, 0, 0))
    width = screen.get_width()
    height = screen.get_height()

    # Initialize persistent drops if not already present.
    if not hasattr(scene_z, "drops"):
        scene_z.drops = []
        num_drops = 90  # Total number of drops on screen.
        for _ in range(num_drops):
            drop = {
                "x": random.randint(0, width),
                "y": random.randint(-height, 0),  # Start above the screen.
                "size": random.randint(2, 10),
                "speed": 60,
                "trail": [],  # List of previous positions (up to 10)
            }
            scene_z.drops.append(drop)

    # Update and draw each drop.
    for drop in scene_z.drops:
        # Record the current position at the start of the trail.
        drop["trail"].insert(0, (drop["x"], drop["y"]))
        # Keep only the most recent 10 trail positions.
        if len(drop["trail"]) > 10:
            drop["trail"] = drop["trail"][:10]

        # Update the drop's vertical position.
        drop["y"] += drop["speed"]

        # If the drop is below the screen, respawn it above.
        if drop["y"] > height:
            drop["x"] = random.randint(0, width)
            drop["y"] = random.randint(-50, -10)
            drop["size"] = random.randint(2, 10)
            drop["speed"] = 60
            drop["trail"] = []

        # Draw the drop's trail.
        # The most recent trail element (index 0) is the most opaque,
        # and opacity decreases for older trail positions.
        for i, pos in enumerate(drop["trail"]):
            # Compute alpha: full opacity for the most recent (i=0), then linearly fading.
            alpha = int(255 * (1 - i / 10.0))
            # Create a temporary surface for the trail square.
            trail_surface = pygame.Surface(
                (drop["size"], drop["size"]), pygame.SRCALPHA
            )
            trail_surface.fill((255, 255, 255, alpha))
            screen.blit(trail_surface, pos)

        # Draw the drop itself (full opacity).
        drop_surface = pygame.Surface((drop["size"], drop["size"]), pygame.SRCALPHA)
        drop_surface.fill((255, 255, 255, 255))
        screen.blit(drop_surface, (drop["x"], drop["y"]))


import pygame, random, math


def generate_fractal_lines(depth, length, angle):
    """
    Recursively generate a list of line segments representing a fractal pattern.
    Each segment is a tuple: ((x1, y1), (x2, y2)) relative to (0,0).
    """
    segments = []
    if depth == 0:
        # Base case: a single line segment from (0,0) to (length*cos(angle), length*sin(angle))
        x = length * math.cos(angle)
        y = length * math.sin(angle)
        segments.append(((0, 0), (x, y)))
    else:
        # Draw the main segment.
        x = length * math.cos(angle)
        y = length * math.sin(angle)
        segments.append(((0, 0), (x, y)))
        # Choose a random branch offset.
        branch_angle_offset = random.uniform(0.2, 0.8)
        # Generate two branches with a reduced length.
        segs1 = generate_fractal_lines(
            depth - 1, length * 0.7, angle + branch_angle_offset
        )
        segs2 = generate_fractal_lines(
            depth - 1, length * 0.7, angle - branch_angle_offset
        )
        # Offset each branch so that it starts at the end of the main segment.
        segs1 = [
            ((pt1[0] + x, pt1[1] + y), (pt2[0] + x, pt2[1] + y)) for pt1, pt2 in segs1
        ]
        segs2 = [
            ((pt1[0] + x, pt1[1] + y), (pt2[0] + x, pt2[1] + y)) for pt1, pt2 in segs2
        ]
        segments.extend(segs1)
        segments.extend(segs2)
    return segments


def scene_u(screen):
    """
    Scene X: Glitchy Fractal Explosions

    - Random explosion events occur on a black background.
    - Each explosion is created by generating a fractal pattern (via recursion)
      that “explodes” outward from a random position.
    - As the explosion evolves, the fractal pattern is scaled outward and its segments
      are randomly shifted (glitched), producing a dynamic, chaotic effect.
    - Explosions have a short duration and are replaced by new ones over time.
    """
    screen.fill((0, 0, 0))
    current_time = pygame.time.get_ticks()

    # Initialize persistent explosion events if needed.
    if not hasattr(scene_u, "explosions"):
        scene_u.explosions = []

    # With a small probability, spawn a new explosion event.
    if random.random() < 0.03:  # Adjust the spawn frequency as desired.
        pos = (
            random.randint(0, screen.get_width()),
            random.randint(0, screen.get_height()),
        )
        duration = random.randint(1500, 15000)  # Duration in milliseconds.
        start_time = current_time
        depth = random.randint(2, 6)
        base_length = random.uniform(50, 750)
        # Generate fractal segments for several starting angles to create a richer explosion.
        all_segments = []
        for _ in range(random.randint(3, 15)):
            angle = random.uniform(0, 8 * math.pi)
            segs = generate_fractal_lines(depth, base_length, angle)
            all_segments.extend(segs)
        explosion = {
            "pos": pos,
            "start": start_time,
            "duration": duration,
            "segments": all_segments,
        }
        scene_u.explosions.append(explosion)

    # Update and draw each explosion.
    for explosion in scene_u.explosions[:]:
        elapsed = current_time - explosion["start"]
        progress = elapsed / explosion["duration"]
        if progress >= 1.0:
            scene_u.explosions.remove(explosion)
            continue

        # For each fractal segment, scale it by the explosion progress and apply glitch offsets.
        for seg in explosion["segments"]:
            (x1, y1), (x2, y2) = seg
            # Scale the coordinates by the progress (so the pattern expands over time).
            x1_scaled = x1 * progress
            y1_scaled = y1 * progress
            x2_scaled = x2 * progress
            y2_scaled = y2 * progress

            # Offset by the explosion's center.
            x1_final = explosion["pos"][0] + x1_scaled
            y1_final = explosion["pos"][1] + y1_scaled
            x2_final = explosion["pos"][0] + x2_scaled
            y2_final = explosion["pos"][1] + y2_scaled

            # Glitch effect: with a 30% chance, randomly perturb each endpoint.
            if random.random() < 0.3:
                x1_final += random.randint(-10, 10)
                y1_final += random.randint(-10, 10)
            if random.random() < 0.3:
                x2_final += random.randint(-10, 10)
                y2_final += random.randint(-10, 10)

            # Choose a color from a set of neon/glitchy colors.
            color = random.choice([(255, 255, 255), (180, 180, 180), (40, 40, 40)])
            thickness = random.randint(1, 2)
            pygame.draw.line(
                screen,
                color,
                (int(x1_final), int(y1_final)),
                (int(x2_final), int(y2_final)),
                thickness,
            )


def scene_i(screen):
    """
    Scene P: Procedural Geometric Chaos

    - Randomly generated polygons and lines appear, overlap, and fade out over time.
    - Shapes are drawn semi-transparently on a dedicated layer for depth.
    - Sudden shifts in density and color schemes occur every few hundred frames.
    """
    import pygame, random, math

    width, height = screen.get_width(), screen.get_height()
    screen.fill((0, 0, 0))  # Black background

    # Initialize persistent state.
    if not hasattr(scene_i, "shapes"):
        scene_i.shapes = []  # List to store active shapes.
        scene_i.frame_count = 0  # Frame counter.
        # Choose an initial color scheme: "cool", "warm", or "neutral"
        scene_i.current_color_scheme = random.choice(["cool", "warm", "neutral"])

    scene_i.frame_count += 1

    # With some probability each frame, add a new shape.
    # Adjust the probability to control spawn density.
    if random.random() < 0.2:
        shape_type = random.choice(["polygon", "line"])
        lifetime = random.randint(60, 180)  # Lifetime in frames.
        # Choose a base color depending on the current scheme.
        if scene_i.current_color_scheme == "cool":
            base_color = (0, 0, 139)  # Deep blue.
        elif scene_i.current_color_scheme == "warm":
            base_color = (139, 0, 0)  # Deep red.
        else:
            base_color = (100, 100, 100)  # Neutral gray.
        # Set an initial alpha between 50 and 150.
        alpha = random.randint(50, 150)
        color = base_color + (alpha,)

        if shape_type == "polygon":
            num_vertices = random.randint(3, 8)
            # Pick a random center.
            cx = random.randint(0, width)
            cy = random.randint(0, height)
            r = random.randint(20, 100)
            vertices = []
            for i in range(num_vertices):
                # Distribute vertices roughly evenly but add randomness.
                angle = 2 * math.pi * i / num_vertices + random.uniform(-0.2, 0.2)
                rr = r * random.uniform(0.7, 1.3)
                x = cx + rr * math.cos(angle)
                y = cy + rr * math.sin(angle)
                vertices.append((x, y))
            shape = {
                "type": "polygon",
                "vertices": vertices,
                "lifetime": lifetime,
                "age": 0,
                "color": color,
            }
        else:  # "line"
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            shape = {
                "type": "line",
                "points": [(x1, y1), (x2, y2)],
                "lifetime": lifetime,
                "age": 0,
                "color": color,
            }
        scene_i.shapes.append(shape)

    # Every 200 frames, randomly change the color scheme.
    if scene_i.frame_count % 200 == 0:
        scene_i.current_color_scheme = random.choice(["cool", "warm", "neutral"])

    # Create a transparent surface for drawing shapes.
    layer = pygame.Surface((width, height), pygame.SRCALPHA)

    # Update shapes: increase age and fade out (reduce alpha).
    new_shapes = []
    for shape in scene_i.shapes:
        shape["age"] += 1
        progress = shape["age"] / shape["lifetime"]
        if progress >= 1:
            continue  # Skip shapes that have expired.
        # Fade alpha linearly over the lifetime.
        orig_alpha = shape["color"][3]
        new_alpha = int(orig_alpha * (1 - progress))
        # Update the color with the new alpha.
        shape["color"] = shape["color"][:3] + (new_alpha,)
        new_shapes.append(shape)
    scene_i.shapes = new_shapes

    # Draw all shapes onto the layer.
    for shape in scene_i.shapes:
        if shape["type"] == "polygon":
            pts = [(int(x), int(y)) for (x, y) in shape["vertices"]]
            pygame.draw.polygon(layer, shape["color"], pts)
        elif shape["type"] == "line":
            pts = [(int(x), int(y)) for (x, y) in shape["points"]]
            pygame.draw.line(
                layer, shape["color"], pts[0], pts[1], random.randint(1, 3)
            )

    # Optionally, add a few extra random lines directly for extra chaos.
    if random.random() < 0.1:
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        extra_color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 150),
        )
        pygame.draw.line(layer, extra_color, (x1, y1), (x2, y2), random.randint(1, 3))

    # Finally, blit the transparent layer onto the screen.
    screen.blit(layer, (0, 0))


def scene_o(screen):
    """
    Scene O: Liquid Light Show Effects

    - Organic, morphing shapes ("blobs") flow like liquid metal.
    - Each blob is a polygon computed from a base radius with sinusoidal distortions.
      Its shape slowly evolves over time.
    - Multiple semi-transparent blobs overlap to create layers of pulsating color.
    - Occasionally, a glitch is triggered that abruptly changes the blob colors,
      simulating analog interference.
    - Blobs are colored with a blue range (from deep dark blue to bright blue).
    - Each blob disappears after a random interval (10–30 seconds) and is replaced.
    - Blob movement (phase evolution) is faster.
    - Each blob is outlined with a thick black line.
    """
    import pygame, random, math

    # Fill the screen to black.
    screen.fill((0, 0, 0))
    width, height = screen.get_width(), screen.get_height()
    current_time = pygame.time.get_ticks()

    # --- Initialize Persistent State for Blobs ---
    if not hasattr(scene_o, "blobs"):
        scene_o.blobs = []
        num_blobs = random.randint(6, 10)
        for _ in range(num_blobs):
            blob = {
                "center": (random.randint(0, width), random.randint(0, height)),
                "base_radius": random.uniform(100, 400),
                "vertex_count": 50,
                "amplitude": random.uniform(5, 30),
                "phase": random.uniform(0, 3 * math.pi),
                "phase_speed": random.uniform(0.05, 0.2),  # faster movement
                # One offset per vertex.
                "offsets": [random.uniform(-15, 15) for _ in range(50)],
                # Color is chosen from a blue range: either deep (0,0,139) or bright (0,0,255), with alpha 150.
                "color": random.choice([(0, 0, 139, 150), (0, 0, 255, 150)]),
                "birth": current_time,
                "lifetime": random.randint(
                    10000, 30000
                ),  # 10 to 30 seconds in milliseconds.
            }
            scene_o.blobs.append(blob)

    # --- Glitch Mechanism ---
    if not hasattr(scene_o, "glitch_timer"):
        scene_o.glitch_timer = random.randint(300, 800)
        scene_o.glitch_counter = 0
    scene_o.glitch_counter += 1
    if scene_o.glitch_counter >= scene_o.glitch_timer:
        glitch = True
        scene_o.glitch_counter = 0
        scene_o.glitch_timer = random.randint(300, 800)
        # On glitch, reassign each blob's color to a random gradient from black to blue.
        for blob in scene_o.blobs:
            blue_val = random.randint(0, 255)  # 0 = black, 255 = full blue
            blob["color"] = (0, 0, blue_val, 200)

    # --- Remove Expired Blobs and Spawn New Ones ---
    new_blob_list = []
    num_blobs_target = random.randint(6, 10)
    for blob in scene_o.blobs:
        if current_time - blob["birth"] < blob["lifetime"]:
            new_blob_list.append(blob)
    # If any blob has expired, create new ones to reach the target count.
    while len(new_blob_list) < num_blobs_target:
        new_blob = {
            "center": (random.randint(0, width), random.randint(0, height)),
            "base_radius": random.uniform(40, 600),
            "vertex_count": 50,
            "amplitude": random.uniform(5, 20),
            "phase": random.uniform(0, 3 * math.pi),
            "phase_speed": random.uniform(0.05, 0.2),
            "offsets": [random.uniform(-15, 15) for _ in range(50)],
            "color": random.choice([(0, 0, 139, 150), (0, 0, 255, 150)]),
            "birth": current_time,
            "lifetime": random.randint(10000, 30000),
        }
        new_blob_list.append(new_blob)
    scene_o.blobs = new_blob_list

    # --- Update and Draw Blobs ---
    # Create a transparent layer for drawing.
    layer = pygame.Surface((width, height), pygame.SRCALPHA)
    for blob in scene_o.blobs:
        # Update the blob's phase faster.
        blob["phase"] += blob["phase_speed"]
        vertices = []
        for i in range(blob["vertex_count"]):
            angle = 2 * math.pi * i / blob["vertex_count"]
            # Update each vertex's offset slightly.
            blob["offsets"][i] += random.uniform(-0.5, 0.5)
            blob["offsets"][i] = max(-15, min(15, blob["offsets"][i]))
            # Compute a dynamic radius with sinusoidal distortion.
            r = (
                blob["base_radius"]
                + blob["amplitude"] * math.sin(angle + blob["phase"])
                + blob["offsets"][i]
            )
            x = blob["center"][0] + r * math.cos(angle)
            y = blob["center"][1] + r * math.sin(angle)
            vertices.append((int(x), int(y)))
        # Draw the blob as a filled polygon.
        pygame.draw.polygon(layer, blob["color"], vertices)
        # Draw a thicker black outline (4 pixels) for extra texture.
        pygame.draw.polygon(layer, (0, 0, 0, 255), vertices, 4)
    screen.blit(layer, (0, 0))


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
        pygame.K_e: (scene_e, ["lines", "theta", "u", "v"]),
        pygame.K_4: (scene_4, ["config"]),
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
