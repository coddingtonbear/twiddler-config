import argparse
import os
import sys

from .config import Config


def main(*argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs=1, type=str)

    args = parser.parse_args(argv)
    with open(os.path.expanduser(args.path[0]), 'rb') as inf:
        cfg = Config.from_buffer(inf)

    for chord in cfg.chords:
        print(chord)


if __name__ == '__main__':
    main(*sys.argv[1:])
