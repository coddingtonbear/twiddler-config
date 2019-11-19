import argparse
import os
import sys

from .config import Config


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs=1, type=str)

    args = parser.parse_args(argv)
    cfg = Config.from_path(args.path[0])

    for chord in cfg.chords:
        print(chord)


if __name__ == '__main__':
    main()
