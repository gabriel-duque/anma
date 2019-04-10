import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    parser.add_argument("-c", "--conf", help="set keymap configuration file",
                        type=str, default="misc/anma.conf")
    parser.add_argument("-b", "--background", help="set background image",
                        type=str, default="misc/cat.png")
    parser.add_argument("-M", "--midi_output", help="set MIDI output id",
                        type=int, default=0)
    args = parser.parse_args()
    return args

def dump_config(arg):
    print("totototototot")
    #print(
    #        f'Verbose: {"on" if arg.verbose else "off"}\n'
    #        f'Keymap configuration: {arg.conf}\n'
    #        f'Background image: {arg.background}\n'
    #        f'Midi output identifier: {arg.midi_output}'
    #)
