
import sys
import pygame


class MenuActivator:

    def new_file(self):
        print("New file created")

    def open_file(self):
        print("Open file dialog")

    def save_file(self):
        print("Save current file")

    def exit_app(self):
        print("Exiting application")
        pygame.quit()
        sys.exit()

    def play_file(self):
        print("Playing file")

    def undo_action(self):
        print("Undo last action")

    def redo_action(self):
        print("Redo last action")

    def undo_last_action(self):
        print("Undo last action")

    def redo_last_action(self):
        print("Redo last action")