import pygame
from defs import *
from math import sqrt

def create_3d_text(screen, text, size, x, y, console=None):
    """Tạo hiệu ứng chữ 3D với viền"""

    font = pygame.font.Font(FONT, int(size * sqrt(console.ratio_x ** 2 + console.ratio_y ** 2)))
    
    # Vẽ outline (viền)
    outline_offsets = [
        (-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
        (-1, -2), (-1, 2),
        (0, -2), (0, 2),
        (1, -2), (1, 2),
        (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)
    ]
    
    for dx, dy in outline_offsets:
        outline_surface = font.render(text, True, BLUE_LIGHT)
        dx, dy = console.convertCoordinate(dx, dy)
        screen.blit(outline_surface, (x + dx, y + dy))
    
    # Vẽ chữ chính
    main_surface = font.render(text, True, WHITE)
    screen.blit(main_surface, (x, y))