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
dark_gray = (50,50,50)
green = (0,255,0)
gold = (212,175,55)
blue = (0,255,255)


#Create screen using dimensions used above, name the caption and label
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Silly Rabbit, Beats are for Kids')
label_font = pygame.font.Font('freesansbold.ttf', 32)
medium_font = pygame.font.Font('freesansbold.ttf', 24)


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
active_list = [1 for _ in range(instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 0
beat_changed = True

def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_list[i] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                floor_tom.play()

#load in sounds
hi_hat = mixer.Sound('./sounds/hi hat.WAV')
snare = mixer.Sound('./sounds/snare.WAV')
kick = mixer.Sound('./sounds/kick.WAV')
crash = mixer.Sound('./sounds/crash.WAV')
clap = mixer.Sound('./sounds/clap.WAV')
floor_tom = mixer.Sound('./sounds/tom.WAV')
#mixer defaults to 8. Way to get around this is the amount of instruments times 3 or higher.
pygame.mixer.set_num_channels(instruments * 3)

#define function for draw grid
def draw_grid(clicks, beat,actives):
    #start by making the left side menu. it is a rectangle so I have to call 4 arguments
    #Fifth one outside of the [], determines the width of the edges and make it a hollow object
    left_box = pygame.draw.rect(screen,gray, [0, 0, 200, HEIGHT - 200], 5)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 200, WIDTH, 200], 5)
    boxes = []
    colors = [gray, white, gray]
    hi_hat_text = label_font.render('Hi Hat', True, colors[actives[0]])
    screen.blit(hi_hat_text, (30,30))
    snare_text = label_font.render('Snare', True, colors[actives[1]])
    screen.blit(snare_text, (30,130))
    kick_text = label_font.render('Bass Drum', True, colors[actives[2]])
    screen.blit(kick_text, (30,230))
    crash_text = label_font.render('Crash', True, colors[actives[3]])
    screen.blit(crash_text, (30,330))
    clap_text = label_font.render('Clap', True, colors[actives[4]])
    screen.blit(clap_text, (30,430))
    floor_tom_text = label_font.render('Floor Tom', True, colors[actives[5]])
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
                if actives[j] == 1:
                    color = green
                else:
                    color = dark_gray
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
    boxes = draw_grid(clicked, active_beat,active_list)

    #lower menu
    play_pause = pygame.draw.rect(screen,gray, [50, HEIGHT -150, 200, 100], 0 ,5)
    play_text = label_font.render('Play/Pause', True, white)
    screen.blit(play_text, (70,HEIGHT -130))
    if playing:
        play_text2 = medium_font.render('Playing', True, dark_gray)
    else:
        play_text2 = medium_font.render('Paused',True,dark_gray)
    screen.blit(play_text2, (70,HEIGHT -100))

    #BPM Settings
    bpm_rect = pygame.draw.rect(screen,gray,[300,HEIGHT -150, 200, 100], 5,5)
    bpm_text = medium_font.render('BPM:', True, white)
    screen.blit(bpm_text, bpm_text.get_rect(center = (400, HEIGHT - 120))) #(308, HEIGHT - 130))
    bpm_text2 = label_font.render(f'{bpm}', True, white)
    screen.blit(bpm_text2, (370, HEIGHT - 100))
    bpm_add_rect = pygame.draw.rect(screen, gray, [510,HEIGHT -150, 48, 48], 0, 5)
    bpm_sub_rect = pygame.draw.rect(screen, gray, [510, HEIGHT -100, 48, 48],0 ,5)
    add_text = medium_font.render('+5', True, white)
    sub_text = medium_font.render ('-5', True, white)
    screen.blit(add_text, (520, HEIGHT - 140))
    screen.blit(sub_text, (520, HEIGHT -90))

    #beats on beats
    beats_rect = pygame.draw.rect(screen,gray,[600, HEIGHT -150, 200, 100], 5,5)
    beats_text = medium_font.render('Beats in Loop:', True, white)
    screen.blit(beats_text, beats_text.get_rect(center = (700, HEIGHT - 120))) #(308, HEIGHT - 130))
    beats_text2 = label_font.render(f'{beats}', True, white)
    screen.blit(beats_text2, (680, HEIGHT - 100))
    beats_add_rect = pygame.draw.rect(screen, gray, [810,HEIGHT -150, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, gray, [810, HEIGHT -100, 48, 48],0 ,5)
    add_text2 = medium_font.render('+1', True, white)
    sub_text2 = medium_font.render ('-1', True, white)
    screen.blit(add_text2, (820, HEIGHT - 140))
    screen.blit(sub_text2, (820, HEIGHT -90))

    #instruments
    instruments_rect = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0, i * 100), (200,100))
        instruments_rect.append(rect)


    if beat_changed:
        play_notes()
        beat_changed = False

    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
        #Good rule of thumb for events you want to happen once, use MouseButtonUp
        if event.type == pygame.MOUSEBUTTONUP:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                #Don't just use else. If it was playing, it would be not playing
                #see it is not playing, and start playing again immediately.
                elif not playing:
                    playing = True
            elif bpm_add_rect.collidepoint(event.pos):
                bpm += 5
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -= 5
            elif beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif beats_sub_rect.collidepoint(event.pos):
                beats -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)
            for i in range(len(instruments_rect)):
                if instruments_rect[i].collidepoint(event.pos):
                    active_list[i] *= -1
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