#!/usr/bin/env python3

import args
import config
import handle


def main():
    """Run the program.

    * Parse command-line arguments for output file name, config name etc.
    * Get colors scheme for each note from config file.
    * Initialize PyGame library.
    * Dump config if verbose is active.
    * Create an instance of the AnmaHandle class to handle everything.
    * Loop and get notes until user exits.
    * Write the resulting MIDI file.
    * Cleanup.
    """
    arg = args.parse_args()
    colors = config.parse_colors(arg.conf)
    screen, player = config.init_pygame(arg.midi_output, arg.background)
    led_hndl = config.init_gpio()

    if arg.verbose:
        args.dump_config(arg)

    hndl = handle.AnmaHandle(arg, colors, screen, player, led_hndl)
    if arg.verbose:
        for note in hndl.notes:
            print("{} {}".format(note.name, note.pitch))

    while hndl.loop():
        pass

    #hndl.write_midi()
    #hndl.cleanup()

if __name__ == '__main__':
    main()
