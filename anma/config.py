import contextlib
with contextlib.redirect_stdout(None):
    import pygame
    import pygame.midi

import note


def parse_colors(color_config):
    with open(color_config, "r") as color_input:
        return [int(color.strip()) for color in color_input.readlines()]

def init_pygame(midi_output, bg_file):
    """ Initialize PyGame window and MIDI. """
    screen = pygame.display.set_mode((220, 220))
    pygame.display.set_caption('anma')
    bg = pygame.image.load(bg_file)
    screen.blit(bg, (0, 0))
    pygame.display.update()

    pygame.midi.init()
    out_id = pygame.midi.get_default_output_id()
    player = pygame.midi.Output(out_id)
    player.set_instrument(0)
    return screen, player

def init_notes(colors):
    pitch_count = 88
    names = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    # 21 is the MIDI pitch for the first piano key (A0)
    return [note.Note(names[i % 12] + str((i + 9) // 12), 21 + i, colors[21 + i])
            for i in range(pitch_count)]
