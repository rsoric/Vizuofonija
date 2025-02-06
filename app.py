import pygame
import random
import sys

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
    # Iterate from x=0 to the full width of the screen.
    for x in range(0, width + step, step):
        # Random vertical offset between -amplitude and +amplitude.
        offset = random.randint(-amplitude, amplitude)
        y = base_y + offset
        points.append((x, y))
    return points

def main():
    # Initialize Pygame
    pygame.init()
    
    # Define screen dimensions and create a borderless window.
    WIDTH, HEIGHT = 1600, 900
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    pygame.display.set_caption("Pygame App - TV Static Lines")
    
    # Set up a clock for frame rate control.
    clock = pygame.time.Clock()
    
    # Calculate baseline positions for the 5 horizontal lines.
    spacing = HEIGHT / 6  # Dividing the screen into 6 equal parts creates 5 equally spaced division lines.

    # Random number of lines with random heights
    num_lines = random.randint(17, 56)
    baseline_y_positions = [random.randint(0, HEIGHT) for _ in range(num_lines)]

    
    # Parameters to control the static effect.
    amplitude = 15  # Maximum vertical offset for each segment.
    step = 5       # Horizontal distance between points along the line.
    
    running = True
    while running:
        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Fill the background with black.
        screen.fill((0, 0, 0))
        
        # For each baseline line, generate a polyline with random vertical offsets and draw it.
        for base_y in baseline_y_positions:
            points = generate_static_line_points(base_y, amplitude, step, WIDTH)
            pygame.draw.lines(screen, (100, 100, 100), False, points, 1)
        
        # Update the display.
        pygame.display.flip()
        
        # Cap the frame rate.
        clock.tick(15)
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
