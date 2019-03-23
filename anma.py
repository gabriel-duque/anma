#!/usr/bin/env python3

import contextlib
with contextlib.redirect_stdout(None):
    import pygame
    import pygame.midi
import midiutil
import time
import tkinter
import tkinter.filedialog
from tkinter import *

color_codes = []
colors = [[0, 0, 255], [255, 133, 0], [255, 0, 0], [0, 255, 0], [255, 255, 255]]

keys = {
        's': ('do', 60),
        'e': ('do#', 61),
        'd': ('re', 62),
        'r': ('re#', 63),
        'f': ('mi', 64),
        'g': ('fa', 65),
        'y': ('fa#', 66),
        'h': ('sol', 67),
        'u': ('sol#', 68),
        'j': ('la', 69),
        'i': ('la#', 70),
        'k': ('si', 71),
        'l': ('do', 72),
        }

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

#def get_config_filename():
#    root_win = tkinter.Tk()
#    root_win.withdraw()
#    tkinter.filedialog.askopenfilename()

def init(config_file):
    global color_codes
    with open("anma.conf", "r") as conf:
        color_codes = [int(line.strip()) for line in conf.readlines()]

def get_key(event):
    return pygame.key.name(event.key)

def print_note(key):
    print(key, end=" ")
    print(keys[key][0], end=" ")

def print_rgb(key):
    print(color_codes[keys[key][1]])

def set_rgb(key, screen):
    screen.fill(colors[color_codes[keys[key][1]]])
    pygame.display.update()

def add_note(m_file, key, time):
    m_file.addNote(0, 0, keys[key][1], time, 1, 100)

def main():
    t = 0
    #tempo = 120
    #pygame.mixer.init(fps, -16, 1, 2048)
    m_file = midiutil.MIDIFile(1)
    #m_file.addTempo(0, time, tempo)
    #config_file = get_config_filename()
    #config_file = anma.conf

    with open("anma.conf", "r") as config_file:
        config_file.read()

    pygame.init()
    init(config_file) # Read config
    screen = pygame.display.set_mode((535, 300), 0, 32)
    pygame.display.set_caption('anma')

    pygame.midi.init()
    player = pygame.midi.Output(0)
    player.set_instrument(0)

    while True:
        event = pygame.event.wait()

        do1 = pygame.draw.rect(screen, WHITE, (50, 50, 50, 200))
        ree = pygame.draw.rect(screen, WHITE, (105, 50, 50, 200))
        mii = pygame.draw.rect(screen, WHITE, (160, 50, 50, 200))
        faa = pygame.draw.rect(screen, WHITE, (215, 50, 50, 200))
        soll = pygame.draw.rect(screen, WHITE, (270, 50, 50, 200))
        laa = pygame.draw.rect(screen, WHITE, (325, 50, 50, 200))
        sii = pygame.draw.rect(screen, WHITE, (380, 50, 50, 200))
        do2 = pygame.draw.rect(screen, WHITE, (435, 50, 50, 200))
        pygame.display.update()

        if event.type == pygame.KEYDOWN:
            key = get_key(event)

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                break

            if  event.key == pygame.K_s:
                doo = pygame.draw.rect(screen, colors[color_codes[keys[key][1]]], (50, 50, 50, 200))
                pygame.display.update()

            if  event.key == pygame.K_d:
                ree = pygame.draw.rect(screen, colors[color_codes[keys[key][1]]], (105, 50, 50, 200))
                pygame.display.update()

            if  key in keys:
                print_note(key)
                print_rgb(key)
                #set_rgb(key, screen)

                player.note_on(keys[key][1], 100)
                add_note(m_file, key, t)
                t += 1

            else:
                print("key " + key + " is not mapped")

        elif event.type == pygame.KEYUP:
            key = get_key(event)

            if  key in keys:
                player.note_off(keys[key][1], 100)

        time.sleep(0.05)

    with open('out.mid', 'wb') as output:
        m_file.writeFile(output)
    player.close()
    pygame.midi.quit()

if __name__ == '__main__':
    main()
