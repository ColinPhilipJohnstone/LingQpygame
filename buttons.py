
import pygame
from parameters import params
import copy 

class ImageButton():
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

        # set x and y position and size variables
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

class TextButton():
    def __init__(self,pos,text,fontsize,italic=False,bold=False,color=(0,0,0),backgroundColor=None):
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
        self.drawBackground = False
        if backgroundColor is not None:
            self.drawBackground = True
            self.backgroundColor = backgroundColor
            self.backgroundRect = pygame.Rect(self.xPos,self.yPos,self.xSize,self.ySize)

    def move(self,pos):
        '''Moves button to a new position'''
        self.pos = pos
        self.xPos , self.yPos = self.pos
        self.xPos2 , self.yPos2 = self.xPos+self.xSize , self.yPos+self.ySize
        if self.drawBackground:
            self.backgroundRect = pygame.Rect(self.xPos,self.yPos,self.xSize,self.ySize)

    def isIn(self,pos):
        '''Takes position tuple in format (x,y) and returns if this is in this button'''
        isInX = (pos[0] >= self.xPos) and (pos[0] <= self.xPos2)
        isInY = (pos[1] >= self.yPos) and (pos[1] <= self.yPos2) 
        return (isInX and isInY)

    def draw(self,surface):
        '''Draws button to a given surface'''
        if self.drawBackground:
            pygame.draw.rect(surface,self.backgroundColor,self.backgroundRect)
        surface.blit(self.image,(self.xPos,self.yPos))

class Word(TextButton):
    def __init__(self,pos,text,status=None):
        '''Sets up word button either as a normal word, an unknown word, or a lingq'''

        # save the basic term 
        self.term = getTerm(text)

        # how to set it up depends entirely on the status
        self.status = status
        if status == "unknown":
            # make an unknown word
            super().__init__(pos,text,params["FONT_SIZE"],backgroundColor=params["UNKNOWN_HIGHLIGHT_COLOR"])
        elif status == "lingq":
            # make a lingq
            super().__init__(pos,text,params["FONT_SIZE"],backgroundColor=params["LINGQ_HIGHLIGHT_COLOR_1"])
        else:
            # just assume normal word
            super().__init__(pos,text,params["FONT_SIZE"])

def getTerm(string):
  
  """Takes string with word, returns string with punctuation removed and lowercase."""
  
  # Make sure there is at least one real letter in word and return -1 if not
  isWord = False
  for char in string:
    if char.isalpha():
      isWord = True
  if not isWord:
    return -1
      
  # Make deep copy of string 
  word = copy.deepcopy(string)
  
  # Make word lower case
  word = word.lower()
  
  # Check if need to shave characters off edges
  if not ( word[0].isalpha() and word[-1].isalpha() ):
    
    # Loop forward and get first letter
    for i in range(0,len(word),1):
      if word[i].isalpha():
        iStart = i
        break
    
    # Loop backwards and get last letter
    for i in range(len(word)-1,-1,-1):
      if word[i].isalpha():
        iEnd = i
        break
    
    # Get new word
    word = word[iStart:iEnd+1]
  
  return word
