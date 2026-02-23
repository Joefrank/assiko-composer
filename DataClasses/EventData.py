
import pygame

MOUSE_EVENTS = [
    pygame.MOUSEBUTTONDOWN, 
    pygame.MOUSEBUTTONUP, 
    pygame.MOUSEMOTION,
    pygame.MOUSEWHEEL
]

KEYBOARD_EVENTS = [
    pygame.KEYDOWN,
    pygame.KEYUP
]

EVENT_TYPES = [
        (pygame.MOUSEBUTTONDOWN, "Mouse Button Down", "on_left_mouse_down"),
        (pygame.MOUSEBUTTONUP, "Mouse Button Up", "on_left_mouse_up"),
        (pygame.MOUSEMOTION, "Mouse Motion", "on_mouse_motion"),  
        (pygame.MOUSEWHEEL, "Mouse Wheel", "on_mouse_wheel"),      
        (pygame.VIDEORESIZE, "Video Resize", "on_video_resize"),
        (pygame.KEYDOWN, "Key Down", "on_key_down"),
        (pygame.KEYUP, "Key Up", "on_key_up"),
        (pygame.QUIT, "Quit", "on_quit")
    ]