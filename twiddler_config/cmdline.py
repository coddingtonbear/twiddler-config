import argparse
import os
import sys

from .config import Config


COMMANDS = {}


def command(fn):
    COMMANDS[fn.__name__] = fn


@command
def chords(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str)
    args = parser.parse_args(argv)

    cfg = Config.from_path(args.path)

    for chord in cfg.chords:
        print(chord)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=COMMANDS.keys())
    args, extra = parser.parse_known_args(argv)

    COMMANDS[args.command](extra)


if __name__ == '__main__':
    main()
