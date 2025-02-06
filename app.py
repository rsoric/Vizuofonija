import pygame
import random
import sys
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
    """Placeholder: Fill screen with a reddish tint."""
    screen.fill((100, 50, 50))


def scene_e(screen):
    """Placeholder: Fill screen with a greenish tint."""
    screen.fill((50, 100, 50))


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
