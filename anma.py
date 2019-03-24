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
WHITE = (255, 255, 255)
GREY = (120, 120, 120)
BLACK = (0, 0, 0)

keys = {
        's': ('do', 60,  (50,  50, 50, 200), WHITE),
        'd': ('re', 62,  (105, 50, 50, 200), WHITE),
        'f': ('mi', 64,  (160, 50, 50, 200), WHITE),
        'g': ('fa', 65,  (215, 50, 50, 200), WHITE),
        'h': ('sol', 67, (270, 50, 50, 200), WHITE),
        'j': ('la', 69,  (325, 50, 50, 200), WHITE),
        'k': ('si', 71,  (380, 50, 50, 200), WHITE),
        'l': ('do', 72,  (435, 50, 50, 200), WHITE),
        'r': ('re#', 63, (132.5, 50, 50, 100), BLACK),
        'y': ('fa#', 66, (242.5, 50, 50, 100), BLACK),
        'u': ('sol#', 68, (297.5, 50, 50, 100), BLACK),
        'i': ('la#', 70, (352.5, 50, 50, 100), BLACK),
        'e': ('do#', 61, (77.5, 50, 50, 100), BLACK),
        }

"""keys = {
        's': ('do', 60,  (50,  50, 50, 200), WHITE),
        'e': ('do#', 61, (77.5,  50, 50, 100), BLACK),
        'd': ('re', 62,  (105, 50, 50, 200), WHITE),
        'r': ('re#', 63, (132.5,  50, 50, 100), BLACK),
        'f': ('mi', 64,  (160, 50, 50, 200), WHITE),
        'g': ('fa', 65,  (215, 50, 50, 200), WHITE),
        'y': ('fa#', 66, (242.5,  50, 50, 100), BLACK),
        'h': ('sol', 67, (270, 50, 50, 200), WHITE),
        'u': ('sol#', 68,(297.5,  50, 50, 100), BLACK),
        'j': ('la', 69,  (325, 50, 50, 200), WHITE),
        'i': ('la#', 70, (352.5,  50, 50, 100), BLACK),
        'k': ('si', 71,  (380, 50, 50, 200), WHITE),
        'l': ('do', 72,  (435, 50, 50, 200), WHITE),
        }"""

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

def add_note(m_file, key, time):
    m_file.addNote(0, 0, keys[key][1], time, 1, 127)

def main():
    t = 0
    m_file = midiutil.MIDIFile(1)
    #tempo = 120
    #pygame.mixer.init(fps, -16, 1, 2048)
    #m_file.addTempo(0, time, tempo)
    #config_file = get_config_filename()
    #config_file = anma.conf

    with open("anma.conf", "r") as config_file:
        config_file.read()

    pygame.init()
    init(config_file) # Read config
    screen = pygame.display.set_mode((535, 300), 0, 32)
    pygame.display.set_caption('anma')
    screen.fill(GREY)
    pygame.midi.init()
    out_id = pygame.midi.get_default_output_id()
    player = pygame.midi.Output(0)

    player.set_instrument(0)

    while True :

        #player = pygame.midi.Output(out_id)
        player.set_instrument(3)
    while True:

        event = pygame.event.wait()

        for key in keys:
            pygame.draw.rect(screen, keys[key][3], keys[key][2])
            pygame.display.update()

        if event.type == pygame.KEYDOWN:
            key = get_key(event)

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                break

            if  key in keys:
                print_note(key)
                print_rgb(key)

                pygame.draw.rect(screen, colors[color_codes[keys[key][1]]], keys[key][2])
                pygame.display.update()
                player.note_on(keys[key][1], 100)

                set_rgb(key, screen)

                player.note_on(keys[key][1], 127)


                add_note(m_file, key, t)
                t += 1

        elif event.type == pygame.KEYUP:
            key = get_key(event)


            if key in keys:
                player.note_off(keys[key][1], 100)


            if  key in keys:
                player.note_off(keys[key][1], 127)

        time.sleep(0.05)

    with open('out.mid', 'wb') as output:
        m_file.writeFile(output)
    player.close()
    pygame.midi.quit()

if __name__ == '__main__':
    main()