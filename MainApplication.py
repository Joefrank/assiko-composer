import pygame
from Builders.MainWindowBuilder import MainWindowBuilder
from EventHandlers.MainWindowEventHandler import MainWindowEventHandler
from Model.ApplicationState import ApplicationState
from Renderers.MainWindowRenderer import MainWindowRenderer

pygame.init()

clock = pygame.time.Clock()

event_handler = MainWindowEventHandler()
main_window = MainWindowBuilder(event_handler).build()
main_window.set_app_state(ApplicationState()) # This is to be done once for all.
MainWindowRenderer(main_window).render()

# --------------------------------------------------
# Main Loop
# --------------------------------------------------
running = True
while running:
    event_handler.handle_events()   
    main_window.re_draw_component()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
