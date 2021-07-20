
'''This is the main entry point for the code'''

import pygame
import menu
import lesson
from parameters import params
import lingqAPI as api

class App:

    def __init__(self):

        # initialise LingQ api
        api.init()

        # initialise pygame and the window
        pygame.init()
        self._window = pygame.display.set_mode((params["WINDOW_WIDTH"],params["WINDOW_HEIGHT"]))

        # should end execution if False
        self._running = True

        # start screens but only load the menu now (load a lesson if selected)
        self._menuScreen = menu.Menu()
        self._lessonScreen = None
        self._currentScreen = self._menuScreen

        # set tracker for drawing the contents
        self._render = True



    def _onEvent(self):
        for event in pygame.event.get():
            
            # send event to current screen (menu or lesson) and get four bits of 
            # information. These are
            #  1. if should end simulation
            #  2. if should redraw
            #  3. id of lesson to load ("" for not doing anything, "menu" for switching to menu)
            shouldEnd, self._render, lessonId = self._currentScreen.onEvent(event)

            # check if event type is for quitting
            if shouldEnd or (event.type==pygame.QUIT):
                self._running = False

            # check for loading menu or lesson
            if lessonId == "":
                pass
            elif lessonId == "menu":
                self._currentScreen = self._menuScreen
            else:
                self._lessonScreen = lesson.Lesson(lessonId)
                self._currentScreen = self._lessonScreen

    def _onLoop(self):
        pass

    def _onRender(self):
        if self._render:
            self._currentScreen.onRender(self._window)
            self._render = False

    def execute(self):

        while self._running:
            self._onEvent()
            self._onLoop()
            self._onRender()

if __name__ == "__main__":
    App().execute()

