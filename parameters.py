
'''Holds layout parameters as list'''

params = {}

# window dimensions
params["WINDOW_WIDTH"] = 800
params["WINDOW_HEIGHT"] = 800

# margins in menu and lesson
params["MARGIN_WIDTH"] = params["WINDOW_WIDTH"]/20.0
params["MARGIN_HEIGHT"] = params["WINDOW_HEIGHT"]/10.0

# menu scaling stuff
params["NLESSONS_MENU"] = 5    # number of cources/lessons to show per page in menu
params["FONT_SIZE_LESSON_LIST"] = 20        # font size for course/lesson titles in menu
params["MENU_BACKGROUND_COLOR"] = (164,244,249)       # background color for menu
params["MENU_LESSON_BUTTON_COLOR"] = (240,255,255)       # button color for menu


# some HUD properties for menu and lesson
params["EXIT_BUTTON_SCALING"] = 0.1     # size of exit button relative to image size 
params["ARROW_BUTTON_SCALING"] = 0.15   # size of arrows relative to image sizes


# Lesson text
params["FONT_SIZE"] = 20    # font size for lesson text
params["LINE_SPACE"] = 40   # line spacing for lesson text
params["PARAGRAPH_SPACE"] = int(params["LINE_SPACE"]*1.5) # paragraph spacing for lesson text
params["PARAGRAPH_STRING"] = '</p>' # string to indicate paragraph breaks


# Lesson layout
params["LESSON_BACKGROUND_COLOR"] = (178,190,189)   # background color for the lesson

# params[""] =        #
