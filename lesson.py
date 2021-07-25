
from parameters import params
import pygame
import lingqAPI as api
import buttons

class Lesson:

    def __init__(self,lessonId):
        '''Sets up a lesson'''
        
        print("loading lesson",lessonId)

        # save lesson id
        self.lessonId = lessonId
        
        # load full text, LingQs, unknown words, and hints
        self.text = api.GetText(lessonId)
        self.lingqList , self.lingqs = api.GetLingQs(lessonId)
        self.unknownList , self.unknownIdDict = api.GetUnknownWords(lessonId)
        api.GetLingQHintsList(self.unknownList)
        api.GetLingQHintsList(self.lingqList)
        
        # setup text
        self.pageWordList = self.setup_lesson_text()
        self.nPages = len(self.pageWordList)
        
        # setup LingQs and unknown
        # self.page_lingq_list = self.setup_lingqs()
        # self.page_unknown_list = self.setup_unknown()
        
        # setup HUD on page
        self.setup_lesson_hud()
        
        # setup initial state
        self.nPageCurrent = 0           # start on first page
        self.displayBubble = None       # assume no bubble to display
        self.showHud = False            # assume not showing the hud
        self.clickingStatus = False     # assuming not clicking change status button
        self.wordSelectBox = None       # assume no word select box to display 
        self.BubbleTimer = 0            # make bubble timer as 0
        
        return

    def isUnknown(self,word):
        '''Takes word string, returns if is unknown'''
        return buttons.getTerm(word) in self.unknownList

    def isLingq(self,word):
        '''Takes word string, returns if is lingq'''
        return buttons.getTerm(word) in self.lingqList

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
            
            # determine if lingq or unknown
            status = None
            if self.isUnknown(word):
                status = 'unknown'
            elif self.isLingq(word):
                status = 'lingq'

            # get word button
            wordButton = buttons.Word((xLeft,yTop),word,status=status)
        
            # check if need to move to next line 
            wordRight = xLeft + wordButton.xSize
            if ( wordRight > params["WINDOW_WIDTH"]-params['MARGIN_WIDTH'] ):
                xLeft = params['MARGIN_WIDTH']
                yTop += params['LINE_SPACE']
                wordButton.move((xLeft,yTop))

            # check if need to move to next page
            if yTop > params["WINDOW_HEIGHT"]-params['MARGIN_HEIGHT']:
                
                # save this word list and start new one for next page
                pageWordList.append(wordList)
                wordList = []
                
                # reset positions for next page and move word to start of next page
                xLeft = params['MARGIN_WIDTH']
                yTop = params['MARGIN_HEIGHT']
                wordButton.move((xLeft,yTop))
            
            # add word to word list
            wordList.append(wordButton)
            
            # Uupdate x position
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

            # test for back a page
            if self._leftButton.isIn(pos):
                self.nPageCurrent = max(0,self.nPageCurrent-1)
                return shouldEnd, True, loadLessonId

            # test for forward a page
            if self._rightButton.isIn(pos):
                self.nPageCurrent = min(self.nPages-1,self.nPageCurrent+1)
                return shouldEnd, True, loadLessonId

            # test for exit button to go back to menu
            if self._exitButton.isIn(pos):
                return shouldEnd, True, "menu"

        return shouldEnd, shouldRender, loadLessonId
    



    def onRender(self,window):

        # background
        window.fill(params["LESSON_BACKGROUND_COLOR"])

        # draw words of current page
        for word in self.pageWordList[self.nPageCurrent]:
            word.draw(window)

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
