
import pygame

class Button(pygame.sprite.Sprite):

    def __init__(self):
        '''Sets up button sprite'''

        super().__init__()
        
        # set position and size
        self.xPos , self.yPos = self.pos
        self.xSize , self.ySize = self.size
        self.xPos2 , self.yPos2 = self.xPos+self.xSize , self.yPos+self.ySize

    def isIn(self,pos):
        '''Takes position tuple in format (x,y) and returns if this is in this button'''
        isInX = (pos[0] >= self.xPos) and (pos[0] <= self.xPos2)
        isInY = (pos[1] >= self.yPos) and (pos[1] <= self.yPos2) 
        return (isInX and isInY)

    def draw(self,surface):
        '''Draws button to a given surface'''
        surface.blit(self.image,(self.xPos,self.yPos))


class TextButton(Button):
    def __init__(self,pos,text,fontsize,italic=False,bold=False,color=(0,0,0)):
        '''Takes text string, fontsize, and position and returns button object'''

        self.pos = pos
        font = pygame.font.SysFont("Arial",fontsize,italic=italic,bold=bold)
        self.image = font.render(text,True,color)
        self.size = (self.image.get_width(), self.image.get_height())

        super().__init__()

class ImageButton(Button):
    def __init__(self,pos,filename,size=None,scale=None,centered=False):
        '''Takes filename of image and returns button object for image'''

        # set position
        self.pos = pos

        # load image
        self.image = pygame.image.load(filename)
        
        # scale if size parameter set or get size if not
        if size is not None:
            self.image = pygame.transform.smoothscale(self.image,size)
            self.size = size
        elif scale is not None:
            size = (self.image.get_width(), self.image.get_height())
            ratio = size[1]/size[0]
            self.size = (int(size[0]*scale), int(size[0]*scale*ratio))
            self.image = pygame.transform.smoothscale(self.image,self.size)
        else:
            self.size = (self.image.get_width(), self.image.get_height())
        
        # if wanting position to be centered then reset position
        if centered:
            self.pos = ( int(self.pos[0]-self.size[0]/2.0) , int(self.pos[1]-self.size[1]/2.0) )

        super().__init__()