
"""
Functions for using the LingQ API.
"""

import requests
import json
import multiprocessing as mp
import copy
import sys

# API key for my account
API_KEY = ""

# Language
LANGUAGE = 'de'

# Lesson
#LESSON = '4983458' # longer
#LESSON = '35644' # shorter
LESSON = '5113948' # really short

# Maximum character limit on url
URL_LENGTH_LIMIT = 2000

# Dictionary for saving hints that have already been looked for
unknown_hints = {}

# Collection to upload lessons to
DEFAULT_COLLECTION = 713861

#=====================================================================================

def init():
  '''Initialises LingQ stuff (currently just reads API key from file)'''
  global API_KEY
  
  # read api key
  with open("key.txt",'r') as f: content = f.readlines() 
  API_KEY = content[0].replace("\n","")

#=====================================================================================

def GetCourses():
  
  """Returns courses being studied."""
  
  # Set the URL for this task
  URL = 'https://www.lingq.com/api/languages/'+LANGUAGE+'/courses/'
  
  # Authorisation stuff
  headers = {'Authorization': 'Token {}'.format(API_KEY)}
  
  # Request data
  r = requests.get( url=URL , headers=headers )
  
  # Get list of courses
  courses = r.json()
  
  return courses

#=====================================================================================

def GetCourseLessons(courseId):
  
  """Returns lessons for a given course."""
  
  # Set the URL for this task
  URL = 'https://www.lingq.com/api/v2/'+LANGUAGE+'/collections/'+str(courseId)+'/'
  
  # Authorisation stuff
  headers = {'Authorization': 'Token {}'.format(API_KEY)}
  
  # Request data
  r = requests.get( url=URL , headers=headers )
  
  # Get list of lessons
  lessons = r.json()['lessons']
  
  return lessons

#=====================================================================================

def GetRecentLessons(nLessons):
  
  """Takes number, returns list of this number of recent lessons for this language."""
  
  # The URL for this one is not on the API description but I found it using Firefox inspector (ctl+shift+I) 
  # and going to network and XHR and refreshing the main page to see how it determines the lessons 
  
  # Set the URL for this task
  URL = 'https://www.lingq.com/api/v2/de/lessons/recent/?page_size='+str(nLessons)+'&groupBy=collection&page=1'
  
  # Authorisation stuff
  headers = {'Authorization': 'Token {}'.format(API_KEY)}
  
  # Request data
  r = requests.get( url=URL , headers=headers )
  
  # Get list of lessons
  data = r.json()
  lessons = data['results']
  
  return lessons

#=====================================================================================

def GetText(contentId):
  
  """Returns text of the lesson."""
  
  # Set the URL for this task
  URL = 'https://www.lingq.com/api/languages/'+LANGUAGE+'/lessons/'+str(contentId)+'/text/'
  
  # Authorisation stuff
  headers = {'Authorization': 'Token {}'.format(API_KEY)}
  
  # Request data
  r = requests.get( url=URL , headers=headers )
  
  # Get text
  data = r.json() 
  text = data['text']
  
  # Do a simple replace
  text = text.replace('<p>','')
  text = text.replace('</p>',' </p> ')
  
  
  return text

#=====================================================================================

def GetUnknownWords(contentId):
  
  """Get's unknown words from lesson."""
  
  # Set the URL for this task
  URL = 'https://www.lingq.com/api/languages/'+LANGUAGE+'/lessons/'+str(contentId)+'/words/'
  
  # Authorisation stuff
  headers = {'Authorization': 'Token {}'.format(API_KEY)}
  
  # Request data
  r = requests.get(url = URL, headers = headers) 
  
  # Get list
  data = r.json()
  data = data['unknown']
  
  # Get dictionary with each term and index in list of LingQ for this term
  unknownList = []
  for word in data:
    unknownList.append(word['word'])
  
  # Get dictionary of id for each unknown word
  unknownIdDict = {}
  for word in data:
    unknownIdDict[word['word']] = word['id']
  
  return unknownList , unknownIdDict

#=====================================================================================

def GetLingQs(contentId):
  
  """Get's LingQs for a lesson."""
  
  # Set the URL for this task
  URL = 'https://www.lingq.com/api/languages/'+LANGUAGE+'/lessons/'+str(contentId)+'/lingqs/'
  
  # Authorisation stuff
  headers = {'Authorization': 'Token {}'.format(API_KEY)}
  
  # Request data
  r = requests.get(url = URL, headers = headers) 
  
  # Get LingQs
  lingqs = r.json()
  
  # Get list of all lingq terms and dictionary for each lingq
  linqsList = []
  lingqsDict = {}
  index = 0
  for lingq in lingqs:
    term = lingq['term']
    linqsList.append(term)
    lingqsDict[term] = lingq
    index += 1
  
  return linqsList, lingqsDict

#=====================================================================================

def GetLingQHints(word):
  global unknown_hints
  
  """Retrieves hints for a word."""
  
  if word in unknown_hints:
    
    hints = unknown_hints[word]
  
  else:
    
    # Set the URL for this task
    URL = 'https://www.lingq.com/api/languages/'+LANGUAGE+'/hints/?word='+word
    
    # Authorisation stuff
    headers = {'Authorization': 'Token {}'.format(API_KEY)}
    
    # Request data
    r = requests.get(url = URL, headers = headers) 
    
    # Get list of hints for this word
    hints = r.json()
    hints = hints[word]
    
    # Save these hints so don't have to look again
    unknown_hints[word] = hints
  
  return hints

#=====================================================================================

def GetLingQHintsList(word_list):
  
  """Retrieves hints for all words in a list of words and adds to unknown_hints."""
  
  # Set the URL for this task
  URL = 'https://www.lingq.com/api/languages/'+LANGUAGE+'/hints/?'
  
  # To keep track of words added
  words_list_added = []
  
  # Loop over words and add each to URL
  for word in word_list:
    
    # Get potential URL with this word added
    URLpossible = copy.deepcopy(URL)
    URLpossible += 'word='+word + '&'
    
    # If this URL is too long, get word list for what is already there and restart
    if len(URLpossible) > URL_LENGTH_LIMIT:
      _GetLingQHintsList(URL,words_list_added)
      URL = 'https://www.lingq.com/api/languages/'+LANGUAGE+'/hints/?'
      words_list_added = []
    
    # Add this one to the URL
    URL += 'word='+word + '&'
    
    # Add to words_list_added
    words_list_added.append(word)
  
  # Now at end so add the final words
  _GetLingQHintsList(URL,words_list_added)
  
  return

#-----------------------------------------

def _GetLingQHintsList(URL,words_list_added):
  global unknown_hints
  
  # Authorisation stuff
  headers = {'Authorization': 'Token {}'.format(API_KEY)}
  
  # Request data
  r = requests.get(url = URL, headers = headers) 
  
  # Get dictionary with each word
  data = r.json()
  
  # Loop over words and add hint list for each
  for word in words_list_added:
    unknown_hints[word] = data[word]
  
  return

#=====================================================================================

def put(URL,headers,params):
  """Takes URL, headers, and params, performs requests.put()."""
  r = requests.put(url = URL, data=params, headers = headers)
  return

def post(URL,headers,params):
  """Takes URL, headers, and params, performs requests.put()."""
  r = requests.post(url = URL, json=params, headers = headers)
  return

#=====================================================================================

def ChangeLingQStatus(idlingq,status,extended_status):
  
  """Takes LingQ id and a status, changes status remotely."""
  
  # Set the URL for this task
  URL = 'https://www.lingq.com/api/languages/'+LANGUAGE+'/lingqs/'+str(idlingq)+'/'
  
  # Authorisation stuff
  headers = {'Authorization': 'Token {}'.format(API_KEY)}
  
  # Params for changing the LingQ
  params = {'status':status,'extended_status':extended_status}
  
  # Make change without waiting for it to finish
  p = mp.Process(target=put,args=(URL,headers,params))
  p.daemon = True
  p.start()
  
  return

#=====================================================================================

def CreateLingQ(word,hint_text):
  
  """Retrieves hints for all words in a list of words."""
  
  # Set the URL for this task
  URL = 'https://www.lingq.com/api/languages/'+LANGUAGE+'/lingqs/'
  
  # Authorisation stuff
  headers = { 'Authorization':'Token {}'.format(API_KEY) , 'Content-Type':'application/json' }
  
  # Params for creating the LingQ
  params = { "hints":[{"locale": "en", "text":hint_text}] , "term": word , "lesson":LESSON }
  
  # Do post
  r = requests.post(url=URL, headers=headers, json=params)
  
  # Get id
  data = r.json()
  idlingq = data['id']
  
  # Make change without waiting for it to finish
  #p = mp.Process(target=post,args=(URL,headers,params))
  #p.daemon = True
  #p.start()
  
  return idlingq

#linguist@qa:~ % curl -X POST -d '{"status": 3, "fragment": "siete", \
#"hints": [{"locale": "en", "text": "hour"}], "term": "siete horas"}' \
#'https://www.lingq.com/api/languages/es/lingqs/' -H 'Authorization: Token bd894eabcd4c0' -H "Content-Type: application/json"
#{"id": 4678901}

#curl -X POST -d '{"hints":[{"locale": "en", "text": "a test hint"}], "term": "atestword", "lesson": 5113948}' 
#'https://www.lingq.com/api/languages/de/lingqs/' -H 'Authorization: Token 408fa561d040f932be1f3303e50e426794fda139' -H "Content-Type: application/json"

#=====================================================================================

def IgnoreWord(word):
  
  # Set the URL for this task
  URL = 'https://www.lingq.com/api/languages/'+LANGUAGE+'/ignored-words/'
  
  # Authorisation stuff
  headers = { 'Authorization':'Token {}'.format(API_KEY) }
  
  # Params for creating the LingQ
  params = { 'word':word }
  
  # Do post
  r = requests.post(url=URL, headers=headers, data=params)
  
  # Make change without waiting for it to finish
  #p = mp.Process(target=post,args=(URL,headers,params))
  #p.daemon = True
  #p.start()
  
  return


#=====================================================================================

def MakeKnownWord(word):
  
  """Marks a word as known."""
  
  # Set the URL for this task
  URL = 'https://www.lingq.com/api/languages/'+LANGUAGE+'/known-words/'
  
  # Authorisation stuff
  headers = { 'Authorization':'Token {}'.format(API_KEY) }
  
  # Params for creating the LingQ
  params = { 'word':word , 'content_id':int(LESSON) }
  
  # Do post
  r = requests.post(url=URL, headers=headers, data=params)
  
  # Make change without waiting for it to finish
  #p = mp.Process(target=post,args=(URL,headers,params))
  #p.daemon = True
  #p.start()
  
  return


#=====================================================================================

def FinishLesson(contentId):
  
  """Finishes a lesson (including moving all words to known)."""
  
  # Set the URL for this task
  URL = 'https://www.lingq.com/api/v2/'+LANGUAGE+'/lessons/'+str(contentId)+'/complete/'
  
  # Authorisation stuff
  headers = { 'Authorization':'Token {}'.format(API_KEY) }
  
  # Do post
  r = requests.post(url=URL, headers=headers)
  
  return

#=====================================================================================

def UploadLesson(title,content,collectionId):
  
  """Uploads a lesson"""
  
  print('upload - ',title)
  
  # Set the URL for this task
  URL = 'https://www.lingq.com/api/v2/'+LANGUAGE+'/lessons/'
  
  # Authorisation stuff
  headers = { 'Authorization':'Token {}'.format(API_KEY) , 'Content-Type':'application/json' }
  
  # Params for lesson
  params = { 'title':title , 'text':content , 'share_status':'private' , 'share_status':'private' , 'collection':collectionId }
  #params = { 'title':title , 'text':content , 'share_status':'private' , 'share_status':'private' }
  
  # Do post
  r = requests.post(url=URL, headers=headers, json=params)
  
  # Get content ID
  contentId = r.json()['contentId']
  
  return contentId

#=====================================================================================

def open_lesson(contentId):
  
  """Opens a lesson for studying"""
  
  # Set the URL for this task
  URL = 'https://www.lingq.com/api/study/'
  
  # Authorisation stuff
  headers = { 'Authorization':'Token {}'.format(API_KEY) }
  
  # Params for lesson
  params = { 'content_id':contentId }
  
  # Do post
  r = requests.post(url=URL, headers=headers, data=params)
    
  return

#=====================================================================================
