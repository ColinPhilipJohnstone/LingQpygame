from parameters import params
import pygame

class Lesson:

    def __init__(self):
        '''Sets up a lesson'''
        

    def onEvent(self,event):
        '''Handles what to do when something happens'''

        return true
    
    def onRender(self,window):

        # background
        window.fill(params["MENU_BACKGROUND_COLOR"])

        # update display
        pygame.display.update()
