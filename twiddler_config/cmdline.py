import argparse
import sys

# Import all command classes to cause them to be registered
from .commands import *  # noqa
from .commands.base import COMMANDS


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    commands = {}
    for name, cmd in COMMANDS.items():
        commands[name] = cmd()

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='command')
    for name, command in commands.items():
        cmd_parser = subparsers.add_parser(name)
        command.add_arguments(cmd_parser)

    args = parser.parse_args(argv)

    commands[args.command].handle(args)


if __name__ == '__main__':
    main()
