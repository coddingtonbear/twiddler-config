import argparse

from ..config import Config
from .base import Command


class Chords(Command):
    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, args: argparse.Namespace) -> None:
        cfg = Config.from_path(args.path)

        for chord in cfg.chords:
            print(chord)
