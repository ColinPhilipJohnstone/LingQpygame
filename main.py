
'''This is the main entry point for the code'''

import pygame
import menu
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

        # start screens as list 
        self._screens = []
        self._currentScreen = menu.Menu()



    def _onEvent(self):
        for event in pygame.event.get():
            
            self._running = self._currentScreen.onEvent(event)

            if event.type == pygame.QUIT:
                self._running = False
                

    def _onLoop(self):
        pass

    def _onRender(self):
        self._currentScreen.onRender(self._window)

    def execute(self):

        while self._running:
            self._onEvent()
            self._onLoop()
            self._onRender()

if __name__ == "__main__":
    App().execute()

