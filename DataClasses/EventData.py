
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
        (pygame.MOUSEBUTTONDOWN, "Mouse Button Down", "on_left_mouse_down", ("button", 1)),
        (pygame.MOUSEBUTTONUP, "Mouse Button Up", "on_left_mouse_up", ("button", 1)),
        (pygame.MOUSEMOTION, "Mouse Motion", "on_mouse_motion", None),  
        (pygame.MOUSEWHEEL, "Mouse Wheel", "on_mouse_wheel", None),      
        (pygame.VIDEORESIZE, "Video Resize", "on_video_resize", None),
        (pygame.KEYDOWN, "Key Down", "on_key_down", None),
        (pygame.KEYUP, "Key Up", "on_key_up", None),
        (pygame.QUIT, "Quit", "on_quit", None)
    ]