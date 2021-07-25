
import pygame
from parameters import params

class ImageButton():
    def __init__(self,pos,filename,size=None,scale=None,centered=False,clickPos=None):
        '''
        Takes filename of image and returns button object for image
        
        Input parameters:-
        pos - tuple in form (x,y) of position of button, generally top left corner
        filename - string with path of fle holding image to use to make button
        size - tuple holding the size of the image, if None then use image size from file
        scale - scaling factor for image size, if None then assumed 1, not used if size specified
        centered - set to True to use pos as position of center of button
        clickPos - (x,y,xSize,ySize) tuple holding position and size of clickable area with x,y being position of top left, if None then assume image area

        '''

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

        # set x and y position and size variables
        self.xPos , self.yPos = self.pos
        self.xSize , self.ySize = self.size
        self.xPos2 , self.yPos2 = self.xPos+self.xSize , self.yPos+self.ySize

        # set x and y positions of the clickable area 
        if clickPos is not None:
            self.xPosClick = clickPos[0]
            self.xPos2Click = clickPos[0]+clickPos[2]
            self.yPosClick = clickPos[1]
            self.yPos2Click = clickPos[1]+clickPos[3]
        else:
            self.xPosClick = self.xPos
            self.xPos2Click = self.xPos2
            self.yPosClick = self.yPos
            self.yPos2Click = self.yPos2

    def isIn(self,pos):
        '''Takes position tuple in format (x,y) and returns if this is in this button'''
        isInX = (pos[0] >= self.xPosClick) and (pos[0] <= self.xPos2Click)
        isInY = (pos[1] >= self.yPosClick) and (pos[1] <= self.yPos2Click) 
        return (isInX and isInY)

    def draw(self,surface):
        '''Draws button to a given surface'''
        surface.blit(self.image,(self.xPos,self.yPos))


class InvisibleButton():
    def __init__(self,pos,centered=False):
        '''
        Returns button object for invisible button
        
        Input parameters:-
        pos - (x,y,xSize,ySize) tuple holding position and size of clickable area with x,y being position of top left
        centered - set to True to use pos as position of center of button

        '''

        # set position
        self.pos = (pos[0],pos[1])
        self.size = (pos[2],pos[3])
        
        # if wanting position to be centered then reset position
        if centered:
            self.pos = ( int(self.pos[0]-self.size[0]/2.0) , int(self.pos[1]-self.size[1]/2.0) )

        # set x and y position and size variables
        self.xPos , self.yPos = self.pos
        self.xSize , self.ySize = self.size
        self.xPos2 , self.yPos2 = self.xPos+self.xSize , self.yPos+self.ySize

        # set x and y positions of the clickable area 
        self.xPosClick = self.xPos
        self.xPos2Click = self.xPos2
        self.yPosClick = self.yPos
        self.yPos2Click = self.yPos2

    def isIn(self,pos):
        '''Takes position tuple in format (x,y) and returns if this is in this button'''
        isInX = (pos[0] >= self.xPosClick) and (pos[0] <= self.xPos2Click)
        isInY = (pos[1] >= self.yPosClick) and (pos[1] <= self.yPos2Click) 
        return (isInX and isInY)

    def draw(self,surface):
        '''Dummy function that does nothing'''
        pass
        
class TextButton():
    def __init__(self,pos,text,fontsize,italic=False,bold=False,color=(0,0,0),backgroundColor=None,outlineColor=None,outlineThick=1,backgroundSizeFactor=1.0):
        '''Takes text string, fontsize, and position and returns button object'''

        # save input parameters
        self.pos = pos
        self.text = text
        self.fontsize = fontsize

        # get image and other parameters
        font = pygame.font.SysFont("Arial",fontsize,italic=italic,bold=bold)
        self.image = font.render(text,True,color)
        self.size = (self.image.get_width(), self.image.get_height())

        # set x and y position and size variables
        self.xPos , self.yPos = self.pos
        self.xSize , self.ySize = self.size
        self.xPos2 , self.yPos2 = self.xPos+self.xSize , self.yPos+self.ySize

        # setup background rectangle if desired
        self.hasBackground = False
        self.drawBackground = False
        if backgroundColor is not None:
            self.hasBackground = True
            self.drawBackground = True
            self.backgroundColor = backgroundColor
            dx = self.xSize*(backgroundSizeFactor-1.0)/2.0
            dy = self.ySize*(backgroundSizeFactor-1.0)/2.0
            self.backgroundRect = pygame.Rect(self.xPos-dx,self.yPos-dy,self.xSize+2*dx,self.ySize+2*dy)

        # setup outline if desired
        self.hasOutline = False
        self.drawOutline = False
        if outlineColor is not None:
            self.hasOutline = True
            self.drawOutline = True
            self.outlineColor = outlineColor
            self.outlineThick = outlineThick
            dx = self.xSize*(backgroundSizeFactor-1.0)/2.0
            dy = self.ySize*(backgroundSizeFactor-1.0)/2.0
            self.outlineRect = pygame.Rect(self.xPos-dx,self.yPos-dy,self.xSize+2*dx,self.ySize+2*dy)

    def move(self,pos):
        '''Moves button to a new position'''
        self.pos = pos
        self.xPos , self.yPos = self.pos
        self.xPos2 , self.yPos2 = self.xPos+self.xSize , self.yPos+self.ySize
        if self.hasBackground:
            self.backgroundRect = pygame.Rect(self.xPos,self.yPos,self.xSize,self.ySize)
        if self.hasOutline:
            self.outlineRect = pygame.Rect(self.xPos,self.yPos,self.xSize,self.ySize)

    def isIn(self,pos):
        '''Takes position tuple in format (x,y) and returns if this is in this button'''
        isInX = (pos[0] >= self.xPos) and (pos[0] <= self.xPos2)
        isInY = (pos[1] >= self.yPos) and (pos[1] <= self.yPos2) 
        return (isInX and isInY)

    def draw(self,surface):
        '''Draws button to a given surface'''
        if self.drawBackground:
            pygame.draw.rect(surface,self.backgroundColor,self.backgroundRect)
        if self.drawOutline:
            pygame.draw.rect(surface,self.outlineColor,self.outlineRect,self.outlineThick)
        surface.blit(self.image,(self.xPos,self.yPos))

class Word(TextButton):
    def __init__(self,pos,text,term,status=None,lingq=None):
        '''Sets up word button either as a normal word, an unknown word, or a lingq'''

        # save the basic term 
        self.term = term

        # how to set it up depends entirely on the status
        self.status = status
        if status == "unknown":
            # make an unknown word
            super().__init__(pos,
                             text,params["FONT_SIZE"],
                             backgroundColor=params["UNKNOWN_HIGHLIGHT_COLOR"],
                             outlineColor=params["WORD_OUTLINE_COLOR"],
                             outlineThick=params["WORD_OUTLINE_THICK"],
                             backgroundSizeFactor=params["WORD_HIGHLIGHT_SIZE_FACTOR"])
        elif status == "lingq":
            # make a lingq
            super().__init__(pos,
                             text,
                             params["FONT_SIZE"],
                             backgroundColor=params["LINGQ_HIGHLIGHT_COLOR_1"],
                             outlineColor=params["WORD_OUTLINE_COLOR"],
                             outlineThick=params["WORD_OUTLINE_THICK"],
                             backgroundSizeFactor=params["WORD_HIGHLIGHT_SIZE_FACTOR"])
        else:
            # just assume normal word
            super().__init__(pos,
                             text,
                             params["FONT_SIZE"],
                             outlineColor=params["WORD_OUTLINE_COLOR"],
                             outlineThick=params["WORD_OUTLINE_THICK"],
                             backgroundSizeFactor=params["WORD_HIGHLIGHT_SIZE_FACTOR"])

        # set not to show the outline first
        self.drawOutline = False

    def toogleSelected(self):
        '''Turns on/off the outline showing selection'''
        self.drawOutline = not self.drawOutline

class WordBubble():

    def __init__(self,word):
        '''Takes a Word object and sets up the hint bubble for it'''

        # save the corresponding word object
        self.word = word

        # get position and size 
        self.xSize = params["BUBBLE_WIDTH"]
        self.ySize = params["BUBBLE_HEIGHT"]
        self.xPos, self.yPos = self.getBubblePosition()
        self.xPos2 = self.xPos+self.xSize
        self.yPos2 = self.yPos+self.ySize

        # get background rectangle
        if word.status == 'lingq':
            self.backgroundColor = params["BUBBLE_BACKGROUND_COLOR_LINGQ"]
        elif word.status == 'unknown':
            self.backgroundColor = params["BUBBLE_BACKGROUND_COLOR_UNKNOWN"]
        else:
            self.backgroundColor = params["BUBBLE_BACKGROUND_COLOR_WORD"]
        self.backgroundRect = pygame.Rect(self.xPos,self.yPos,self.xSize,self.ySize)

        # get outline
        self.outlineColor = params["BUBBLE_OUTLINE_COLOR"]
        self.outlineWidth = params["BUBBLE_OUTLINE_WIDTH"]
        self.outlineRect = pygame.Rect(self.xPos,self.yPos,self.xSize,self.ySize)

        # setup contents of bubble
        self.getBubbleContents()

    def getBubblePosition(self):
        '''Gets position of top left corner of bubble'''

        # determine x position

        # initially assume to the right of the word so left side of bubble at middle point of word
        # then check if it is too close to edge
        xPos = self.word.xPos+0.5*self.word.xSize
        if xPos+params["BUBBLE_WIDTH"] > 0.95*params["WINDOW_WIDTH"]:
            xPos += -params["BUBBLE_WIDTH"]

        # move bubble to right if off left side of screen
        if xPos < params["MARGIN_WIDTH"]:
            xPos = params["MARGIN_WIDTH"]

        # move bubble to left if off right side of screen
        if xPos+params["BUBBLE_WIDTH"] > params["WINDOW_WIDTH"]-params["MARGIN_WIDTH"]:
            xPos = params["WINDOW_WIDTH"]-params["MARGIN_WIDTH"]-params["BUBBLE_WIDTH"]

        # initially assume below word then move above word if too low
        yPos = self.word.yPos2+params["BUBBLE_VERTICAL_SEPARATION"]
        if yPos+params["BUBBLE_HEIGHT"] > 0.95*params["WINDOW_HEIGHT"]:
            yPos = self.word.yPos-params["BUBBLE_VERTICAL_SEPARATION"]-params["BUBBLE_HEIGHT"]

        return xPos, yPos

    def getBubbleContents(self):
        '''Gets contents of a bubble'''

        # get term and start item list with it
        self.term = TextButton((self.xPos+params['BUBBLE_MARGIN'],self.yPos+params['BUBBLE_MARGIN']), self.word.term, params['FONT_SIZE_BUBBLE_TERM'])
        self.items = [self.term]

        if self.word.status == 'lingq':
            self.getBubbleContentsLingq()
        else:
            self.getBubbleContentsUnknown()
            
    def getBubbleContentsLingq(self):
        '''Gets contents of a bubble for a lingq'''

        # # number of hints to show
        # nHints = len( lingq['hints'] )
        # self.nHintsShow = min(nHints,params['BUBBLE_MAX_HINTS'])
            
        # # loop over hints and add each one
        # xPosHint = self.xPos+2*params['BUBBLE_MARGIN']
        # yPosHist = self.yCenter + 0.2*self.height
        # for iHint in range(0,nHintsShow):
      

        pass
            

    def getBubbleContentsUnknown(self):
        '''Gets contents of a bubble for an unknown word'''
        pass

    def isIn(self,pos):
        '''Takes position tuple in format (x,y) and returns if this is in this button'''
        isInX = (pos[0] >= self.xPos) and (pos[0] <= self.xPos2)
        isInY = (pos[1] >= self.yPos) and (pos[1] <= self.yPos2) 
        return (isInX and isInY)

    def draw(self,surface):
        '''Draws button to a given surface'''

        # draw box
        pygame.draw.rect(surface,self.backgroundColor,self.backgroundRect)
        pygame.draw.rect(surface,self.outlineColor,self.outlineRect,self.outlineWidth)
        
        # draw items
        for item in self.items:
            surface.blit(item.image, (item.xPos,item.yPos))
