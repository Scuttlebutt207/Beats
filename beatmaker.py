#First import pygame, run pip3 install pygame if not installed yet
#Then import mixer which handles sounds
#Then initialize pygame

import pygame
from pygame import mixer
pygame.init()

#Used wider than tall for beats screen
WIDTH = 1400
HEIGHT = 800

black =(0,0,0)
white = (255,255,255)
gray = (128,128,128)
green = (0,255,0)
gold = (212,175,55)
blue = (0,255,255)


#Create screen using dimensions used above, name the caption and label
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Silly Rabbit, Beats are for Kids')
label_font = pygame.font.Font('freesansbold.ttf', 32)

#set fps and timer which is super important for games
fps = 60
timer = pygame.time.Clock()
#square boxes for beats
beats = 8
#basically rows
instruments = 6
boxes = []
#-1 is not active, 1 is active
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 0
beat_changed = True

#define function for draw grid
def draw_grid(clicks, beat):
    #start by making the left side menu. it is a rectangle so I have to call 4 arguments
    #Fifth one outside of the [], determines the width of the edges and make it a hollow object
    left_box = pygame.draw.rect(screen,gray, [0, 0, 200, HEIGHT - 200], 5)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 200, WIDTH, 200], 5)
    boxes = []
    colors = [gray, white, gray]
    hi_hat_text = label_font.render('Hi Hat', True, white)
    screen.blit(hi_hat_text, (30,30))
    snare_text = label_font.render('Snare', True, white)
    screen.blit(snare_text, (30,130))
    kick_text = label_font.render('Bass Drum', True, white)
    screen.blit(kick_text, (30,230))
    crash_text = label_font.render('Snare', True, white)
    screen.blit(crash_text, (30,330))
    clap_text = label_font.render('Clap', True, white)
    screen.blit(clap_text, (30,430))
    floor_tom_text = label_font.render('Floor Tom', True, white)
    screen.blit(floor_tom_text, (30,530))

    #Create lines in between instruments
    #i range is 6 because we have 6 instruments
    #I'm telling pygame to draw a line across the screen every 100 pixels.
    #Since python starts at 0 and goes up by 5, I am also telling it its starting position
    #each line has a thickness of 3px
    for i in range(instruments):
        pygame.draw.line(screen, gray, (0, (i * 100) + 100), (200, (i * 100) + 100), 3)

    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray
            else:
                color = green
            #use floor division to make sure the width - 200 stays an integer
            #odd math needed to scale this
            #Basically, taking the amount of beats and separating them by width - 200,
            #Then for each instrument, we are doing the same, with the height - 200 for each instrument
            #Finally, starting the loop at 5 pixels with a thickness of 5pxs.
            rect = pygame.draw.rect(screen, color,
                    [i * ((WIDTH - 200) // beats) + 205, (j * 100) + 5, 
                        ((WIDTH - 200) // beats) -10, ((HEIGHT - 200)//instruments) -10], 0, 3)
            pygame.draw.rect(screen, gold,
                [i * ((WIDTH - 200) // beats) + 200, (j * 100), 
                    ((WIDTH - 200) // beats), ((HEIGHT - 200)//instruments)], 5, 5)  
            pygame.draw.rect(screen, black,
                [i * ((WIDTH - 200) // beats) + 200, (j * 100), 
                    ((WIDTH - 200) // beats), ((HEIGHT - 200)//instruments)], 2, 5)    
            #for each rectangle, we are returning which beat it is, and the row, as well as
            #the rectangle itself to determine if it was clicked on.
            boxes.append((rect, (i, j)))

        active = pygame.draw.rect(screen, blue, [beat * ((WIDTH-200)//beats) + 200, 0, ((WIDTH - 200)//beats), instruments * 100], 5, 3)
    return boxes



#Main Game Loop
run = True
while run:
    #as long as run is true, we will execute this code at the fps(60)
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat)

    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
    
    #fps * 60(seconds) = 3600 // bpm
    beat_length = 3600 // bpm

    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat +=1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True

    #Throws everything on screen        
    pygame.display.flip()

pygame.quit()        