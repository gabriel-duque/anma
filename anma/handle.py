#import time

import contextlib
with contextlib.redirect_stdout(None):
    import pygame

import cst
import config


class AnmaHandle:
    def __init__(self, arg, colors, screen, player, led_hndl):
        self.arg = arg
        self.screen = screen
        self.player = player
        self.keys = cst.KEY_TO_NOTE
        self.notes = config.init_notes(colors, led_hndl)

    def loop(self):
        #event = pygame.event.wait()
        event = pygame.event.poll()
        while event.type == pygame.NOEVENT:
            event = pygame.event.poll()
            #time.sleep(0)

        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            if event.key == pygame.K_ESCAPE:
                return False
            if key in self.keys:
                # Calculate the right color
                self.notes[self.keys[key] - 21].play(self)
            else:
                print('Key {} is not mapped'.format(key))
        elif event.type == pygame.KEYUP:
            key = pygame.key.name(event.key)
            if  key in self.keys:
                self.notes[self.keys[key] - 21].stop(self)
        return True
