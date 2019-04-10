import contextlib
with contextlib.redirect_stdout(None):
    import pygame
    import pygame.midi

import note
import led
import RPi.GPIO as GPIO

led_ports = [[17, 22, 27], [18, 23, 24]]
freq = 100

GREY = (120, 120, 120)

def parse_colors(color_config):
    with open(color_config, "r") as color_input:
        return [int(color.strip()) for color in color_input.readlines()]

def init_pygame(midi_output, bg_file):
    """ Initialize PyGame window and MIDI. """
    screen = pygame.display.set_mode((1190, 600), pygame.FULLSCREEN, 32)
    pygame.display.set_caption('anma')
    screen.fill(GREY)
    pygame.display.update()
    pygame.midi.init()

    player = pygame.midi.Output(3)
    player.set_instrument(1)
    return screen, player

def init_notes(colors, led_hndl):
    pitch_count = 88
    names = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    # 21 is the MIDI pitch for the first piano key (A0)
    return [note.Note(names[i % 12] + str((i + 9) // 12),
            21 + i, led.Led(led_hndl[i % 2])) for i in range(pitch_count)]

def init_gpio():
    GPIO.setmode(GPIO.BCM) 
    GPIO.setwarnings(False)
    RUNNING = True
    led_hndl = []

    for led in led_ports:
        curr = []
        for port in led:
            GPIO.setup(port, GPIO.OUT) 
            new_led_hndl = GPIO.PWM(port, freq)
            curr.append(new_led_hndl)
            new_led_hndl.start(0)
        led_hndl.append(curr)

    # led_hndl = [[RED1, GREEN1, BLUE1], [RED2, GREEN2, BLUE2]]
    return led_hndl
