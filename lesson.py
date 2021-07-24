
from parameters import params
import pygame
import lingqAPI as api
import buttons

def dict_to_list(dictIn):
  '''Takes dictionary, returns list of items in dictionary.'''
  listOut = []
  for item in dictIn:
    listOut.append(item)
  return listOut



class Lesson:

    def __init__(self,lessonId):
        '''Sets up a lesson'''
        
        print("loading lesson",lessonId)

        # save lesson id
        self.lessonId = lessonId
        
        # load full text, LingQs, unknown words, and hints
        self.text = api.GetText(lessonId)
        self.lingqsDict , self.lingqs = api.GetLingQs(lessonId)
        self.unknownList , self.unknownIdDict = api.GetUnknownWords(lessonId)
        api.GetLingQHintsList(self.unknownList)
        api.GetLingQHintsList(dict_to_list(self.lingqsDict))
        
        print(self.text)

        # setup text
        self.page_word_list = self.setup_lesson_text()
        self.nPages = len(self.page_word_list)
        
        # setup LingQs and unknown
        # self.page_lingq_list = self.setup_lingqs()
        # self.page_unknown_list = self.setup_unknown()
        
        # setup HUD on page
        self.setup_lesson_hud()
        
        # start on first page
        self.nPageCurrent = 0
        
        # assume no bubble to display
        self.displayBubble = None
        
        # assume not showing the hud
        self.showHud = False
        
        # assuming not clicking change status button
        self.clickingStatus = False
        
        # assume no word select box to display 
        self.wordSelectBox = None
        
        # make bubble timer as 0
        self.BubbleTimer = 0
        
        return
  

    def setup_lesson_text(self):
        '''Sets up the text for a lesson'''

        # start list of word lists for each page
        wordList = []       # list of words for a given page
        pageWordList = []   # list of list of words for all pages
        
        # get list of words
        words = self.text.split()
                
        # width of a space
        spaceButton = buttons.TextButton((0,0),' ',params["FONT_SIZE"])
        spaceWidth = spaceButton.xSize
        
        # loop over all words in the text
        xLeft = params['MARGIN_WIDTH']
        yTop = params['MARGIN_HEIGHT']
        nPage = 0
        for word in words:
        
            # check if this word is a paragraph indicator
            if word == params["PARAGRAPH_STRING"]:
                xLeft = params['MARGIN_WIDTH']
                yTop += params["PARAGRAPH_SPACE"]
                continue
            
            # get word button
            wordButton = buttons.TextButton((xLeft,yTop),word,params["FONT_SIZE"])
        
            # check if need to move to next line and regenerate button if so
            wordRight = xLeft + wordButton.xSize
            if ( wordRight > params["WINDOW_WIDTH"]-params['MARGIN_WIDTH'] ):
                xLeft = params['MARGIN_WIDTH']
                yTop += params['LINE_SPACE']
                wordButton = buttons.TextButton((xLeft,yTop),word,params["FONT_SIZE"])

            # check if need to move to next page
            if yTop > params["WINDOW_HEIGHT"]-params['MARGIN_HEIGHT']:
                
                # save this word list and start new one for next page
                pageWordList.append(wordList)
                wordList = []
                
                # reset positions for next page and regenerate word with new position
                xLeft = params['MARGIN_WIDTH']
                yTop = params['MARGIN_HEIGHT']
                wordButton = buttons.TextButton((xLeft,yTop),word,params["FONT_SIZE"])
            
            # Add word to word list
            wordList.append(wordButton)
            
            # Update x position
            xLeft += wordButton.xSize + spaceWidth
        
        # add final page
        pageWordList.append(wordList)
        
        return pageWordList
    
    def setup_lesson_hud(self):

        # navigation buttons
        self._leftButton = buttons.ImageButton((params["MARGIN_WIDTH"]/2.0,params["WINDOW_HEIGHT"]/2.0),"data/backward_arrow_icon.png",scale=params["ARROW_BUTTON_SCALING"],centered=True)
        self._rightButton = buttons.ImageButton((params["WINDOW_WIDTH"]-params["MARGIN_WIDTH"]/2.0,params["WINDOW_HEIGHT"]/2.0),"data/forward_arrow_icon.png",scale=params["ARROW_BUTTON_SCALING"],centered=True)
        self._finishButton = buttons.ImageButton((params["WINDOW_WIDTH"]-params["MARGIN_WIDTH"],params["WINDOW_HEIGHT"]-params["MARGIN_HEIGHT"]/2.0),"data/tick_icon.png",scale=params["EXIT_BUTTON_SCALING"],centered=True)
        self._exitButton = buttons.ImageButton((10,10),"data/close_icon.png",scale=params["EXIT_BUTTON_SCALING"] )

        return 


    def shouldDrawLeft(self):
        '''Determines if the left arrow should be present'''
        return True

    def shouldDrawRight(self):
        '''Determines if the right arrow should be present'''
        return True

    def shouldDrawFinish(self):
        '''Determines if the finish symbol should be present'''
        return True

    def shouldDrawExit(self):
        '''Determines if the exit symbol should be present'''
        return True

    def onEvent(self,event):
        '''Handles what to do when something happens'''

        # initially assume should output (should not end, should not redraw, should not change page)
        shouldEnd, shouldRender, loadLessonId = False, False, ""


        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # test for exit button to go back to menu
            if self._exitButton.isIn(pos):
                return shouldEnd, True, "menu"

        return shouldEnd, shouldRender, loadLessonId
    



    def onRender(self,window):

        # background
        window.fill(params["LESSON_BACKGROUND_COLOR"])

        # draw navigation buttons
        if self.shouldDrawLeft():
            self._leftButton.draw(window)
        
        if self.shouldDrawRight():
            self._rightButton.draw(window)
        
        if self.shouldDrawFinish():
            self._finishButton.draw(window)
        
        if self.shouldDrawExit():
            self._exitButton.draw(window)

        # update display
        pygame.display.update()
