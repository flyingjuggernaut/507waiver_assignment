# _*_ coding:utf-8 _*_
import operator
import sys
import wikipedia
import nltk
from nltk import sent_tokenize,word_tokenize
import string
import pygame
import test
from numpy.core.multiarray import inner
from audioop import reverse
pygame.init()
#to take the input from the command line
search_item = sys.argv[1]
print(search_item)


summaryWiki = wikipedia.summary("Wikipedia")

results = wikipedia.search(search_item,5,False)
    
result_dict = {} 
for item in results:
    result_dict[item] = wikipedia.page(item).content

text_list = []
for item in result_dict.values():
    text_list.append(word_tokenize(item))

taggedList = []    
for item in text_list:
    taggedList.append(nltk.pos_tag(item))

pos_word_dict = {}
for item in taggedList:
    for innerItem in item:
        if innerItem[1] in pos_word_dict:
            pos_word_dict[innerItem[1]].append(innerItem[0].lower())
        else:
            pos_word_dict[innerItem[1]] = [innerItem[0].lower()]

for item in pos_word_dict.keys():
    word_freq = {}
    for listItem in pos_word_dict[item]:
        if listItem in word_freq:
            word_freq[listItem] += 1
        else:
            word_freq[listItem] = 1
    pos_word_dict[item] = word_freq

for item in pos_word_dict.keys():
    pos_word_dict[item] = sorted(pos_word_dict[item].items(), key=operator.itemgetter(1), reverse = True)
#sorted(freqDict.items(), key=operator.itemgetter(1), reverse = True)

#print(pos_word_dict)
adjList = []
for listItem in taggedList:
    for innerListItem in listItem:
        if innerListItem[1]=='JJ':
            adjList.append(innerListItem[0].lower())

freqDict = {}
for item in adjList:
    if item in freqDict:
        freqDict[item] +=1
    else:
        freqDict[item] = 1     
        
sortedFreq = sorted(freqDict.items(), key=operator.itemgetter(1))

if test.test(pos_word_dict):
    print ("Yay, you passed this part of the test!")
else:
    print ("Oh noes! You didn't pass. Please try again")

topAdjList = []
for i in range(len(sortedFreq)-6,len(sortedFreq)):
    topAdjList.append(sortedFreq[i][0]) 

adj_List = topAdjList


pygame.display.set_caption("Game of adjectives")

black = 0, 0, 0
white = 255,255,255
red = 255, 0, 0
green = 0,255,0

width = 800
height = 600


screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

def text_objects(text,font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
    
def drawBall(x,y,color,text):
    pygame.draw.circle(screen,color,(x,y),50)
    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(text, smallText)
    textRect.center = (x,y)
    screen.blit(textSurf, textRect)
    
def displayKeyPressed(key):
    text = 'keys typed :' + key
    bottomText = pygame.font.Font("freesansbold.ttf",30)
    textSurf, textRect = text_objects(text, bottomText)
    textRect.center = (400,500)
    screen.blit(textSurf, textRect)
    
def displayGameOver():
    largeText = pygame.font.Font("freesansbold.ttf",60)
    textSurf, textRect = text_objects('GAME OVER!!', largeText)
    textRect.center = (400,300)
    screen.blit(textSurf, textRect)
    
def game_loop():
    crashed = False
    start_x = 50
    start_y = 50
    change = 1
    str_keyPressed = ''
    adjIndex = []
    while not crashed:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                crashed = True
            if event.type == pygame.KEYDOWN and len(pygame.key.name(event.key))==1:
                key_name = pygame.key.name(event.key)
                str_keyPressed += key_name
                for item in adj_List:
                    if item[0] == key_name:
                        if adj_List.index(item) not in adjIndex:
                            adjIndex.append(adj_List.index(item))
                            item= ''
        
        start_y += change
        screen.fill(white)
        displayKeyPressed(str_keyPressed)
        
        for i in range(6):
            if i not in adjIndex:
                drawBall(start_x+(50+i*100), start_y, (200+i,255-(i*50),(i**3)),adj_List[i])
                
            if len(adjIndex)==6: 
                screen.fill(white)
                displayGameOver()                
        
        pygame.display.update()
        
        clock.tick(15)
    
game_loop()
pygame.quit()
quit()
