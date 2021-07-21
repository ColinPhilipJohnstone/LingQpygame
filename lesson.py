
from parameters import params
import pygame
import lingqAPI as api


def dict_to_list(dictIn):
  '''Takes dictionary, returns list of items in dictionary.'''
  listOut = []
  for item in dictIn:
    listOut.append(item)
  return listOut



class Lesson:

    def __init__(self,lessonId):
        '''Sets up a lesson'''
                
        # Save lesson id
        self.lessonId = lessonId
        
        # Load full text , LingQs, unknownwords
        self.text = api.GetText(lessonId)
        self.lingqsDict , self.lingqs = api.GetLingQs(lessonId)
        self.unknownList , self.unknownIdDict = api.GetUnknownWords(lessonId)
        
        # Get hints for unknown words and for LingQs
        api.GetLingQHintsList(self.unknownList)
        api.GetLingQHintsList(dict_to_list(self.lingqsDict))
        
        # Setup text
        self.page_word_list = self.setup_lesson_text()
        self.nPages = len(self.page_word_list)
        
        # Setup LingQs and unknown
        # self.page_lingq_list = self.setup_lingqs()
        # self.page_unknown_list = self.setup_unknown()
        
        # Setup HUD on page
        self.setup_lesson_hud()
        
        # Start on first page
        self.nPageCurrent = 0
        
        # Assume no bubble to display
        self.displayBubble = None
        
        # Assume not showing the hud
        self.showHud = False
        
        # Assuming not clicking change status button
        self.clickingStatus = False
        
        # Assume no word select box to display 
        self.wordSelectBox = None
        
        # Make bubble timer as 0
        self.BubbleTimer = 0
        
        return
  

  def setup_lesson_text(self):
    '''Sets up the text for a lesson'''

    # Start list of word lists for each page
    page_word_list = []
    
    # Get list of words
    words = self.text.split()
    
    # Position of first word
    xLeft = params['MARGIN_WIDTH']
    yCenter = params['WINDOW_HEIGHT']-params['MARGIN_HEIGHT']
    
    # # Width of page
    # space_image = get_text_image(text=' ')
    # SPACE_WIDTH = space_image.width
    
    # # Make a first word list
    # word_list = arcade.SpriteList()
    
    # # Start page counter
    # nPage = 0
    
    # # Loop over all words in the text
    # for word in words:
      
    #   # Check if this word is a paragraph indicator
    #   if word == PARAGRAPH_STRING:
    #     xLeft = MARGIN_WIDTH
    #     yCenter += -PARAGRAPH_SPACE
    #     continue
      
    #   # Made image out of word
    #   image = get_text_image(text=word)
      
    #   # Make sprite from image
    #   word_sprite = WordSprite()
    #   word_sprite.SetWord(word)
    #   word_sprite._texture = arcade.Texture(word)
    #   word_sprite.texture.image = image
    #   word_sprite.width = image.width
    #   word_sprite.height = image.height
      
    #   # Check if need to move to next line
    #   word_right = xLeft + word_sprite.width
    #   if ( word_right > SCREEN_WIDTH-MARGIN_WIDTH ):
    #     xLeft = MARGIN_WIDTH
    #     yCenter += -LINE_SPACE
      
    #   # Check if need to move to next page
    #   if yCenter < MARGIN_HEIGHT:
        
    #     # Save this word list
    #     page_word_list.append(word_list)
        
    #     # Start new word list
    #     word_list = arcade.SpriteList()
        
    #     # Reset positions for next page
    #     xLeft = MARGIN_WIDTH
    #     yCenter = SCREEN_HEIGHT-MARGIN_HEIGHT
      
    #   # Set position of word
    #   word_sprite.center_x = xLeft + word_sprite.width / 2
    #   word_sprite.center_y = yCenter
      
    #   # Add word to word list
    #   word_list.append(word_sprite)
      
    #   # Update x position
    #   xLeft += word_sprite.width + SPACE_WIDTH
    
    # # Add final page
    # page_word_list.append(word_list)
    
    return page_word_list
    




        

    def onEvent(self,event):
        '''Handles what to do when something happens'''

        return true
    
    def onRender(self,window):

        # background
        window.fill(params["MENU_BACKGROUND_COLOR"])

        # update display
        pygame.display.update()
