import pygame
from defs import *

def create_3d_text(screen, text, size, x, y):
    """Tạo hiệu ứng chữ 3D với viền"""
    
    font = pygame.font.Font(FONT, size)
    
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
        screen.blit(outline_surface, (x + dx, y + dy))
    
    # Vẽ chữ chính
    main_surface = font.render(text, True, WHITE)
    screen.blit(main_surface, (x, y))

# from math import sqrt

# def create_3d_text(screen, text, size, ratio_x, ratio_y, x, y):
#     """Tạo hiệu ứng chữ 3D với viền"""
    
#     font = pygame.font.Font(FONT, int(size * sqrt(ratio_x ** 2 + ratio_y ** 2)))
    
#     # Vẽ outline (viền)
#     outline_offsets = [
#         (-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
#         (-1, -2), (-1, 2),
#         (0, -2), (0, 2),
#         (1, -2), (1, 2),
#         (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)
#     ]
    
#     for dx, dy in outline_offsets:
#         outline_surface = font.render(text, True, BLUE_LIGHT)
#         screen.blit(outline_surface, (x + dx, y + dy))
    
#     # Vẽ chữ chính
#     main_surface = font.render(text, True, WHITE)
#     screen.blit(main_surface, (x, y))