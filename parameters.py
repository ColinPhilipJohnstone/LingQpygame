
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

# word highlighting options
params["LINGQ_HIGHLIGHT_COLOR_1"] = (255,255,0)     # color for lingq highlight background
params["LINGQ_HIGHLIGHT_COLOR_2"] = (255,255,0)
params["LINGQ_HIGHLIGHT_COLOR_3"] = (255,255,0)
params["LINGQ_HIGHLIGHT_COLOR_4"] = (255,255,0)
params["UNKNOWN_HIGHLIGHT_COLOR"] = (172,229,238)   # color for unknown word highlight background
params["WORD_OUTLINE_COLOR"] = (255,0,0)            # color for outline of selected word
params["WORD_OUTLINE_THICK"] = 2                    # thickness for outline of selected word
params["WORD_HIGHLIGHT_SIZE_FACTOR"] = 1.05         # factor by which to increase the size of the word highlighting relative to text

# lesson text
params["FONT_SIZE"] = 20    # font size for lesson text
params["LINE_SPACE"] = 40   # line spacing for lesson text
params["PARAGRAPH_SPACE"] = int(params["LINE_SPACE"]*1.5) # paragraph spacing for lesson text
params["PARAGRAPH_STRING"] = '</p>' # string to indicate paragraph breaks


# bubble properties
params["BUBBLE_WIDTH"] = int(params["WINDOW_WIDTH"]/1.7)    # width of bubble
params["BUBBLE_HEIGHT"] = int(params["BUBBLE_WIDTH"]/1.8)   # height of bubble                
params["BUBBLE_VERTICAL_SEPARATION"] = 0.2*params["LINE_SPACE"] # distance between top/bottom of bubble ant top/bottom of word
params["BUBBLE_MARGIN"] = int(params["BUBBLE_WIDTH"]/20.0)
params["FONT_SIZE_BUBBLE_TERM"] = 20
params["FONT_SIZE_BUBBLE_HINT"] = 15
params["BUBBLE_HINT_SPACING"] = 30
params["BUBBLE_STATUS_WIDTH"] = int(min(50,(params["BUBBLE_WIDTH"]-2*params["BUBBLE_MARGIN"])/6.0))
params["BUBBLE_STATUS_HEIGHT"] = params["BUBBLE_STATUS_WIDTH"]
params["BUBBLE_MAX_HINTS"] = 3
params["BUBBLE_OPEN_TIME"] = 3.0

# lesson layout
params["LESSON_BACKGROUND_COLOR"] = (178,190,189)   # background color for the lesson

# params[""] =        #
