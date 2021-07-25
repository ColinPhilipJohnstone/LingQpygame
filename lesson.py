
from parameters import params
import pygame
import lingqAPI as api
import buttons
import copy 

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
        
        print(self.lingqs)

        # setup text
        self.pageWordList, self.pageUnknownList, self.pageLingqList = self.setup_lesson_text()
        self.nPages = len(self.pageWordList)
        
        # setup HUD on page
        self.setup_lesson_hud()
        
        # setup initial state
        self.nPageCurrent = 0           # start on first page
        self.displayBubble = False      # assume no bubble to display
        self.bubble = None              # will hold the bubble object when there is one
        self.showHud = False            # assume not showing the hud
        self.clickingStatus = False     # assuming not clicking change status button
        self.bubbleTimer = 0            # make bubble timer as 0
        
        return

    def isUnknown(self,term):
        '''Takes word string, returns if is unknown'''
        return term in self.unknownList

    def isLingq(self,term):
        '''Takes word string, returns if is lingq'''
        return term in self.lingqList

    def setup_lesson_text(self):
        '''Sets up the text for a lesson'''

        # start list of word lists for each page
        wordList = []           # list of words for a given page
        unknownList = []        # list of unknown words for a given page
        lingqList = []          # list of lingqs for a given page
        pageWordList = []       # list of list of words for all pages
        pageUnknownList = []    # list of list of unknown words for all pages
        pageLingqList = []      # list of list of lingqs for all pages
        
        # get list of words
        words = self.text.split()
                
        # width of a space
        spaceButton = buttons.TextButton((0,0),' ',params["FONT_SIZE"])
        spaceWidth = spaceButton.xSize
        
        # loop over all words in the text
        xLeft = params['MARGIN_WIDTH']
        yTop = params['MARGIN_HEIGHT']
        for word in words:
        
            # check if this word is a paragraph indicator
            if word == params["PARAGRAPH_STRING"]:
                xLeft = params['MARGIN_WIDTH']
                yTop += params["PARAGRAPH_SPACE"]
                continue
            
            # get corresponding term for word
            term = getTerm(word)

            # determine if lingq or unknown
            status = None
            if self.isUnknown(term):
                status = 'unknown'
            elif self.isLingq(term):
                status = 'lingq'

            # get word button
            wordButton = buttons.Word((xLeft,yTop),word,term,status=status)
        
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
                pageUnknownList.append(unknownList)
                pageLingqList.append(lingqList)
                wordList = []
                unknownList = []
                lingqList = []
                
                # reset positions for next page and move word to start of next page
                xLeft = params['MARGIN_WIDTH']
                yTop = params['MARGIN_HEIGHT']
                wordButton.move((xLeft,yTop))
            
            # add word to word list
            wordList.append(wordButton)
            if status == 'unknown':
                unknownList.append(wordButton)
            elif status == 'lingq':
                lingqList.append(wordButton)
            
            # Uupdate x position
            xLeft += wordButton.xSize + spaceWidth
        
        # add final page
        pageWordList.append(wordList)
        pageUnknownList.append(unknownList)
        pageLingqList.append(lingqList)
        
        return pageWordList, pageUnknownList, pageLingqList
    
    def setup_lesson_hud(self):

        # navigation buttons
        self._leftButton = buttons.ImageButton((params["MARGIN_WIDTH"]/2.0,params["WINDOW_HEIGHT"]/2.0),
                                                "data/backward_arrow_icon.png",
                                                scale=params["ARROW_BUTTON_SCALING"],
                                                centered=True,
                                                clickPos=(0.0,params["MARGIN_HEIGHT"],params["MARGIN_WIDTH"],params["WINDOW_HEIGHT"]-2*params["MARGIN_HEIGHT"]))
        self._rightButton = buttons.ImageButton((params["WINDOW_WIDTH"]-params["MARGIN_WIDTH"]/2.0,params["WINDOW_HEIGHT"]/2.0),
                                                "data/forward_arrow_icon.png",
                                                scale=params["ARROW_BUTTON_SCALING"],
                                                centered=True,
                                                clickPos=(params["WINDOW_WIDTH"]-params["MARGIN_WIDTH"],params["MARGIN_HEIGHT"],params["MARGIN_WIDTH"],params["WINDOW_HEIGHT"]-2*params["MARGIN_HEIGHT"]))
        self._finishButton = buttons.ImageButton((params["WINDOW_WIDTH"]-params["MARGIN_WIDTH"],params["WINDOW_HEIGHT"]-params["MARGIN_HEIGHT"]/2.0),
                                                "data/tick_icon.png",
                                                scale=params["EXIT_BUTTON_SCALING"],
                                                centered=True)
        self._exitButton = buttons.ImageButton((10,10),
                                                "data/close_icon.png",
                                                scale=params["EXIT_BUTTON_SCALING"] )
        self.showHudButton = buttons.InvisibleButton((0.0,0.0,params["WINDOW_WIDTH"],params["MARGIN_HEIGHT"]))

        return 


    def shouldDrawLeft(self):
        '''Determines if the left arrow should be present'''
        if self.showHud and (self.nPageCurrent > 0):
            return True
        else:
            return False

    def shouldDrawRight(self):
        '''Determines if the right arrow should be present'''
        if self.showHud and (self.nPageCurrent < self.nPages-1):
            return True
        else:
            return False

    def shouldDrawFinish(self):
        '''Determines if the finish symbol should be present'''

        if self.nPageCurrent == self.nPages-1:
            return True
        else:
            return False

    def shouldDrawExit(self):
        '''Determines if the exit symbol should be present'''
        return self.showHud

    def onEvent(self,event):
        '''Handles what to do when something happens'''

        # initially assume should output (should not end, should not redraw, should not change page)
        shouldEnd, shouldRender, loadLessonId = False, False, ""


        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # if a word bubble is being shown and this click is outside its box then this should
            # cause it to stop being displayed 
            # don't return in this case since click could be on something else intentionally
            if self.displayBubble:
                if not self.bubble.isIn(pos):
                    self.bubble.word.toogleSelected()
                    self.displayBubble = False
                    shouldRender = True

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

            # test for show hud button
            if self.showHudButton.isIn(pos):
                self.showHud = not self.showHud
                return shouldEnd, True, loadLessonId
           
            # test for one of the words on the page
            for word in self.pageWordList[self.nPageCurrent]:
                if word.isIn(pos):
                    word.toogleSelected()
                    self.displayBubble = True
                    self.bubble = buttons.WordBubble(word)
                    return shouldEnd, True, loadLessonId

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

        # draw bubble if there is one
        if self.displayBubble:
            self.bubble.draw(window)

        # update display
        pygame.display.update()

def getTerm(string):
  '''Takes string with word, returns string with punctuation removed and lowercase.'''
  
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
