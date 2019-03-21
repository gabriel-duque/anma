#!/usr/bin/env python3

import contextlib
with contextlib.redirect_stdout(None):
    import pygame
    import pygame.midi

import midiutil
import time
import tkinter
import tkinter.filedialog

colors = []

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
    print(key, end=" ")
    print(keys[key][0], end=" ")

def print_rgb(key):
    print(colors[keys[key][1]])

def play_key(key):
    pass

def add_note(m_file, key, time):
    m_file.addNote(0, 0, keys[key][1], time, 1, 100)

def main():
    t = 0
    tempo = 120
    #pygame.mixer.init(fps, -16, 1, 2048)
    m_file = midiutil.MIDIFile(1)
    #m_file.addTempo(0, time, tempo)
    config_file = get_config_filename()
    init(config_file) # Read config
    screen = pygame.display.set_mode((220, 220))
    pygame.display.set_caption('anma')
    bg = pygame.image.load('cat.png')
    screen.blit(bg, (0, 0))
    pygame.display.update()

    pygame.midi.init()
    player = pygame.midi.Output(0)
    player.set_instrument(0)
    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            key = get_key(event)
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                break
            if  key in keys:
                print_note(key)
                print_rgb(key)
                play_key(key)

                player.note_on(keys[key][1], 100)
                time.sleep(1)
                player.note_off(keys[key][1], 100)

                add_note(m_file, key, t)
                t += 1
            else:
                print("key " + key + " is not mapped")
        time.sleep(0.05)
    with open('out.mid', 'wb') as output:
        m_file.writeFile(output)
    player.close()
    pygame.midi.quit()


if __name__ == '__main__':
    main()