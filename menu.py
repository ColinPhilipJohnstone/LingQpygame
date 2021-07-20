
import pygame
import buttons
import lingqAPI as api
from parameters import params
import math


class Menu:

    def __init__(self):
        '''Setus up the main menu'''
        
        # navigation buttons
        params["WINDOW_WIDTH"]
        params["WINDOW_HEIGHT"]

        self._exitButton = buttons.ImageButton((10,10),"data/close_icon.png",scale=params["EXIT_BUTTON_SCALING"] )
        self._upButton = buttons.ImageButton((params["WINDOW_WIDTH"]/2.0,params["MARGIN_HEIGHT"]/4.0),"data/upward_arrow_icon.png",scale=params["ARROW_BUTTON_SCALING"],centered=True)
        self._downButton = buttons.ImageButton((params["WINDOW_WIDTH"]/2.0,params["WINDOW_HEIGHT"]-params["MARGIN_HEIGHT"]/4.0),"data/downward_arrow_icon.png",scale=params["ARROW_BUTTON_SCALING"],centered=True)
        self._leftButton = buttons.ImageButton((params["MARGIN_WIDTH"]/2.0,params["WINDOW_HEIGHT"]/2.0),"data/backward_arrow_icon.png",scale=params["ARROW_BUTTON_SCALING"],centered=True)
        self._rightButton = buttons.ImageButton((params["WINDOW_WIDTH"]-params["MARGIN_WIDTH"]/2.0,params["WINDOW_HEIGHT"]/2.0),"data/forward_arrow_icon.png",scale=params["ARROW_BUTTON_SCALING"],centered=True)
    
        # get list of courses
        self.courses = api.GetCourses()
        self.nCourses = len(self.courses)

        # get pages for courses
        self.nPagesCourse = int(math.ceil(self.nCourses/params["NLESSONS_MENU"]))
        self.pageCourseCurrent = 0
        self.pagesCourse = []
        for i in range(self.nPagesCourse):
            iMin = i*params["NLESSONS_MENU"]
            iMax = (i+1)*params["NLESSONS_MENU"]
            page = []
            for j,course in enumerate(self.courses[iMin:iMax]):
                xPos = params["MARGIN_WIDTH"]
                yPos = params["MARGIN_HEIGHT"] + j*(params["WINDOW_HEIGHT"]-2*params["MARGIN_HEIGHT"])/params["NLESSONS_MENU"]
                button = buttons.TextButton((xPos,yPos),course["title"],params["FONT_SIZE_LESSON_LIST"])
                course["button"] = button
                page.append(course)
            self.pagesCourse.append(page)

        # setup lesson pages variables without doing anything (only to be done if cource clicked on)
        self.courseIdLoaded = "" 
        self.nPagesLesson = 0
        self.pageLessonCurrent = 0
        self.pagesLesson = []

        # for tracking if in course menu or lesson menu
        self.inLessonMenu = False
        
    def initLessonMenu(self,course):
        '''Loads the lesson menu for a given course'''

        # do nothing if this course is already loaded
        if self.courseIdLoaded == course["id"]:
            return

        # get list of lessons
        self.lessons = api.GetCourseLessons(course['id'])

        # get pages for lessons
        self.nPagesLesson = int(math.ceil(self.nCourses/params["NLESSONS_MENU"]))
        self.pageLessonCurrent = 0
        self.pagesLesson = []
        for i in range(self.nPagesLesson):
            iMin = i*params["NLESSONS_MENU"]
            iMax = (i+1)*params["NLESSONS_MENU"]
            page = []
            for j,lesson in enumerate(self.lessons[iMin:iMax]):
                xPos = params["MARGIN_WIDTH"]
                yPos = params["MARGIN_HEIGHT"] + j*(params["WINDOW_HEIGHT"]-2*params["MARGIN_HEIGHT"])/params["NLESSONS_MENU"]
                button = buttons.TextButton((xPos,yPos),lesson["title"],params["FONT_SIZE_LESSON_LIST"])
                lesson["button"] = button
                page.append(lesson)
            self.pagesLesson.append(page)

    def shouldDrawUp(self):
        '''Determines if the up arrow should be present'''
        return ((not self.inLessonMenu) and (self.pageCourseCurrent>0)) or (self.inLessonMenu and (self.pageLessonCurrent>0))

    def shouldDrawDown(self):
        '''Determines if the down arrow should be present'''
        return ((not self.inLessonMenu) and (self.pageCourseCurrent<self.nPagesCourse-1)) or (self.inLessonMenu and (self.pageLessonCurrent<self.nPagesLesson-1))

    def shouldDrawLeft(self):
        '''Determines if the left arrow should be present'''
        return self.inLessonMenu 

    def shouldDrawRight(self):
        '''Determines if the right arrow should be present'''
        return (not self.inLessonMenu) and (not self.courseIdLoaded == "")

    def shouldDrawExit(self):
        '''Determines if the exit symbol should be present'''
        return True

    def onEvent(self,event):
        '''Handles what to do when something happens'''

        continueRunning = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # get if clicked on course
            if not self.inLessonMenu:
                for course in self.pagesCourse[self.pageCourseCurrent]:
                    if course["button"].isIn(pos):
                        self.initLessonMenu(course)
                        self.inLessonMenu = True
                        self.courseIdLoaded = course["id"]
                        return continueRunning

            # get if clicked on lesson
            if self.inLessonMenu:
                for lesson in self.pagesLesson[self.pageLessonCurrent]:
                    if lesson["button"].isIn(pos):
                        print(lesson['title'])
                        return continueRunning

            # test for up and down navigation buttons
            if self.shouldDrawUp() and self._upButton.isIn(pos):
                if not self.inLessonMenu:
                    self.pageCourseCurrent = max(0,self.pageCourseCurrent-1)
                else:
                    self.pageLessonCurrent = max(0,self.pageLessonCurrent-1)
                return continueRunning

            if self.shouldDrawDown() and self._downButton.isIn(pos):
                if not self.inLessonMenu:
                    self.pageCourseCurrent = min(self.nPagesCourse-1,self.pageCourseCurrent+1)
                else:
                    self.pageLessonCurrent = min(self.nPagesCourse-1,self.pageLessonCurrent+1)
                return continueRunning

            # test for going back to the course menu
            if self.inLessonMenu:
                if self._leftButton.isIn(pos):
                    self.inLessonMenu = False
                    return continueRunning
            
            # test for going back to the lesson menu if a lesson had already been loaded
            if (not self.inLessonMenu) and (not self.courseIdLoaded == ""):
                if self._rightButton.isIn(pos):
                    self.inLessonMenu = True
                    return continueRunning

            # test for exit button
            if self._exitButton.isIn(pos):
                continueRunning = False

        return continueRunning
    
    def onRender(self,window):

        # background
        window.fill(params["MENU_BACKGROUND_COLOR"])

        # draw navigation buttons
        if self.shouldDrawUp():
            self._upButton.draw(window)

        if self.shouldDrawDown():
            self._downButton.draw(window)
        
        if self.shouldDrawLeft():
            self._leftButton.draw(window)
        
        if self.shouldDrawRight():
            self._rightButton.draw(window)
        
        if self.shouldDrawExit():
            self._exitButton.draw(window)

        # draw list of courses or lessons to select from
        if not self.inLessonMenu:
            for course in self.pagesCourse[self.pageCourseCurrent]:
                course["button"].draw(window)
        else:
            for lesson in self.pagesLesson[self.pageLessonCurrent]:
                lesson["button"].draw(window)

        # update display
        pygame.display.update()
