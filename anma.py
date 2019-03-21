#!/usr/bin/env python3

import contextlib
with contextlib.redirect_stdout(None):
    import pygame

import time
import tkinter
import tkinter.filedialog

colors = []

keys = {
        's': ('do', 59),
        'e': ('do#', 60),
        'd': ('re', 61),
        'r': ('re#', 62),
        'f': ('mi', 63),
        'g': ('fa', 64),
        'y': ('fa#', 65),
        'h': ('sol', 66),
        'u': ('sol#', 67),
        'j': ('la', 69),
        'i': ('la#', 70),
        'k': ('si', 71),
        'l': ('do', 72),
        }

def get_config_filename():
    root_win = tkinter.Tk()
    root_win.withdraw()
    tkinter.filedialog.askopenfilename()

def init(config_file):
    global colors
    with open("anma.conf", "r") as conf:
        colors = [int(line.strip()) for line in conf.readlines()]

def get_key(event):
    return pygame.key.name(event.key)

def print_note(key):
    if  key in keys:
        print(key, end=" ")
        print(keys[key][0], end=" ")

def print_rgb(key):
    if key in keys:
        print(colors[keys[key][1]])
    else:
        print("key " + key + " is not mapped")

def play_key(key):
    pass

def main():
    #pygame.mixer.init(fps, -16, 1, 2048)
    config_file = get_config_filename()
    init(config_file) # Read config
    screen = pygame.display.set_mode((220, 220))
    pygame.display.set_caption('anma')
    bg = pygame.image.load('cat.png')
    screen.blit(bg, (0, 0))
    pygame.display.update()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            key = get_key(event)
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                break
            print_note(key)
            print_rgb(key)
            play_key(key)
        time.sleep(0.05)


if __name__ == '__main__':
    main()
