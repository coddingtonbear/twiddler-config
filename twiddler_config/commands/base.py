import argparse


COMMANDS = {}


class CommandMetaclass(type):
    def __new__(cls, clsname, superclasses, attributedict):
        new_cls = type.__new__(cls, clsname, superclasses, attributedict)

        if superclasses:
            COMMANDS[clsname.lower()] = new_cls

        return new_cls


class Command(metaclass=CommandMetaclass):
    def add_arguments(self, parser) -> None:
        pass

    def handle(self, args: argparse.Namespace) -> None:
        raise NotImplementedError()

    @property
    def name(self) -> str:
        return self.__class__.__name__.lower()
