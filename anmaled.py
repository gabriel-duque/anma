#!/usr/bin/env python3
# timidity -iA -B2,8 -Os1l -s 44100
# sdffdsfds

import contextlib
with contextlib.redirect_stdout(None):
    import pygame
    import pygame.midi
import RPi.GPIO as GPIO

color_codes = []
WHITE = (255, 255, 255)
GREY = (120, 120, 120)
BLACK = (0, 0, 0)

whitekeys = {
        'q': ('do1', 48,  (50,  50, 100, 500), WHITE),
        's': ('re1', 50,  (160, 50, 100, 500), WHITE),
        'd': ('mi1', 52,  (270, 50, 100, 500), WHITE),
        'f': ('fa1', 53,  (380, 50, 100, 500), WHITE),
        'g': ('sol1', 55, (490, 50, 100, 500), WHITE),
        'h': ('la1', 57,  (600, 50, 100, 500), WHITE),
        'j': ('si1', 59,  (710, 50, 100, 500), WHITE),
        'k': ('do2', 60,  (820, 50, 100, 500), WHITE),
        'l': ('re2', 62,  (930, 50, 100, 500), WHITE),
        'm': ('mi2', 64,  (1040, 50, 100, 500), WHITE),
        }

blackkeys = {
        'z': ('do#1', 49, (110, 50, 90, 250), BLACK),
        'e': ('re#1', 51, (220, 50, 90, 250), BLACK),
        't': ('fa#1', 54, (440, 50, 90, 250), BLACK),
        'y': ('sol1#', 56, (550, 50, 90, 250), BLACK),
        'u': ('la#1', 58, (660, 50, 90, 250), BLACK),
        'o': ('do#2', 61, (880, 50, 90, 250), BLACK),
        'p': ('re#2', 63, (990, 50, 90, 250), BLACK),
        }

def init(config_file):
    global color_codes
    with open("anma2.conf", "r") as conf:
        color_codes = [line.strip() for line in conf.readlines()]

def get_key(event):
    return pygame.key.name(event.key)

def add_note(m_file, key, time):
    m_file.addNote(0, 0, keys[key][1], time, 1, 127)
    
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)
RUNNING = True

green1 = 22
red1 = 17
blue1 = 27

green2= 23
red2 = 18
blue2 = 24

GPIO.setup(red1, GPIO.OUT) 
GPIO.setup(green1, GPIO.OUT)
GPIO.setup(blue1, GPIO.OUT)
GPIO.setup(red2, GPIO.OUT) 
GPIO.setup(green2, GPIO.OUT)
GPIO.setup(blue2, GPIO.OUT)

Freq = 100

RED1 = GPIO.PWM(red1, Freq)  
GREEN1 = GPIO.PWM(green1, Freq)
BLUE1 = GPIO.PWM(blue1, Freq)

RED2 = GPIO.PWM(red2, Freq)  
GREEN2 = GPIO.PWM(green2, Freq)
BLUE2 = GPIO.PWM(blue2, Freq)

RED1.start(0)
GREEN1.start(0)
BLUE1.start(0)
RED2.start(0)
GREEN2.start(0)
BLUE2.start(0)

def main():

    with open("./anma2.conf", "r") as config_file:
        config_file.read()

    pygame.init()
    init(config_file) # Read config
    screen = pygame.display.set_mode((1190, 600), pygame.FULLSCREEN, 32)
    pygame.display.set_caption('anma')
    screen.fill(GREY)
    
    pygame.midi.init()
    player = pygame.midi.Output(3)
    player.set_instrument(1)
    
    for i in whitekeys: 
        pygame.draw.rect(screen, whitekeys[i][3], whitekeys[i][2])
        pygame.display.update()

    for i in blackkeys: 
        pygame.draw.rect(screen, blackkeys[i][3], blackkeys[i][2])
        pygame.display.update()
        
    while True :

        event = pygame.event.wait()

        if event.type == pygame.KEYDOWN :
            key = get_key(event)
            
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                GPIO.cleanup()
                break
            
            elif key in whitekeys:
                
                player.note_on(whitekeys[key][1], 120)
                
                rgb = color_codes[whitekeys[key][1]]
                list = rgb.split(",")
                r = int(list[0].strip('('))
                g = int(list[1])
                b = int(list[2].strip(')'))
                colorr= (r, g, b)
                print(colorr)
                pygame.draw.rect(screen, colorr, whitekeys[key][2])
                
                for i in blackkeys: 
                    pygame.draw.rect(screen, blackkeys[i][3], blackkeys[i][2])
                pygame.display.update()
                
                RED1.start(100-20*r/51)
                GREEN1.start(100-20*g/51)
                BLUE1.start(100-20*b/51)
                RED2.start(100-20*r/51)
                GREEN2.start(100-20*g/51)
                BLUE2.start(100-20*b/51)
                
            elif key in blackkeys:
                
                player.note_on(blackkeys[key][1], 120)
                
                rgb = color_codes[blackkeys[key][1]]
                list = rgb.split(",")
                
                r = int(list[0].strip('('))
                g = int(list[1])
                b = int(list[2].strip(')'))
                
                colorr= (r, g, b)
                print(colorr)
                pygame.draw.rect(screen, colorr, blackkeys[key][2])
                pygame.display.update()
                
                RED1.start(100-20*r/51)
                GREEN1.start(100-20*g/51)
                BLUE1.start(100-20*b/51)
                RED2.start(100-20*r/51)
                GREEN2.start(100-20*g/51)
                BLUE2.start(100-20*b/51)
            
            elif event.key == pygame.K_w:
                player.set_instrument(1)
            elif event.key == pygame.K_x:
                player.set_instrument(5)
            elif event.key == pygame.K_c:
                player.set_instrument(20)
            elif event.key == pygame.K_v:
                player.set_instrument(50)
            elif event.key == pygame.K_b:
                player.set_instrument(99)
            elif event.key == pygame.K_n:
                player.set_instrument(50)
              
            else:
                print("key " + key + " is not mapped")

        elif event.type == pygame.KEYUP:
            key = get_key(event)

            if key in whitekeys:
                player.note_off(whitekeys[key][1], 120)
                
                for i in whitekeys: 
                    pygame.draw.rect(screen, whitekeys[i][3], whitekeys[i][2])

            if key in blackkeys:
                player.note_off(blackkeys[key][1], 120)
            
            for i in blackkeys: 
                pygame.draw.rect(screen, blackkeys[i][3], blackkeys[i][2])
                pygame.display.update()
                
    player.close()
    pygame.midi.quit()

if __name__ == '__main__':
    main()
