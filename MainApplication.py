import pygame
from Builders.MainWindowBuilder import MainWindowBuilder
from Renderers.MainWindowRenderer import MainWindowRenderer


pygame.init()

clock = pygame.time.Clock()

main_window = MainWindowBuilder().build()
MainWindowRenderer(main_window).render()


# --------------------------------------------------
# Main Loop
# --------------------------------------------------
running = True
while running: 
    dt = clock.tick(60)  # Limit to 60 FPS
    main_window.handle_events(dt) # handles all types of events on window
    pygame.display.flip()
    
pygame.quit()
