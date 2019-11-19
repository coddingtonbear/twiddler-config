from __future__ import annotations

import enum
import struct
from typing import Dict, List
from typing.io import BinaryIO

from .scancodes import SCANCODES


class MouseClick(enum.Enum):
    right = 0
    left = 1


class ChordMapping:
    def __init__(self, modifier_byte: int, keycode: int):
        self._modifier_byte = modifier_byte
        self._keycode = keycode

    @property
    def keyname(self) -> str:
        return SCANCODES.get(self._keycode, hex(self._keycode))

    @property
    def left_ctrl(self) -> bool:
        return bool(self._modifier_byte & 1 << 0)

    @property
    def left_shift(self) -> bool:
        return bool(self._modifier_byte & 1 << 1)

    @property
    def left_alt(self) -> bool:
        return bool(self._modifier_byte & 1 << 2)

    @property
    def left_gui(self) -> bool:
        return bool(self._modifier_byte & 1 << 3)

    @property
    def right_ctrl(self) -> bool:
        return bool(self._modifier_byte & 1 << 4)

    @property
    def right_shift(self) -> bool:
        return bool(self._modifier_byte & 1 << 5)

    @property
    def right_alt(self) -> bool:
        return bool(self._modifier_byte & 1 << 6)

    @property
    def right_gui(self) -> bool:
        return bool(self._modifier_byte & 1 << 7)

    @property
    def key_combination(self) -> str:
        keys = []
        if self.left_ctrl:
            keys.append('L_Ctrl')
        if self.left_shift:
            keys.append('L_Shift')
        if self.left_alt:
            keys.append('L_Alt')
        if self.left_gui:
            keys.append('L_Gui')
        if self.right_ctrl:
            keys.append('R_Ctrl')
        if self.right_shift:
            keys.append('R_Shift')
        if self.right_alt:
            keys.append('R_Alt')
        if self.right_gui:
            keys.append('R_Gui')

        keys.append(self.keyname)

        return '+'.join(keys)

    def __str__(self):
        return self.key_combination

    def __repr__(self):
        return f"<ChordMapping {self}>"


class Chord:
    def __init__(self, buttons: int, mappings: List[ChordMapping]):
        self._buttons = buttons
        self._mappings = mappings

    @property
    def mappings(self) -> List[ChordMapping]:
        return self._mappings

    @property
    def num(self) -> bool:
        return bool(self._buttons & 1 << 0)

    @property
    def alt(self) -> bool:
        return bool(self._buttons & 1 << 4)

    @property
    def ctrl(self) -> bool:
        return bool(self._buttons & 1 << 8)

    @property
    def shift(self) -> bool:
        return bool(self._buttons & 1 << 12)

    @property
    def one_right(self) -> bool:
        return bool(self._buttons & 1 << 1)

    @property
    def one_middle(self) -> bool:
        return bool(self._buttons & 1 << 2)

    @property
    def one_left(self) -> bool:
        return bool(self._buttons & 1 << 3)

    @property
    def two_right(self) -> bool:
        return bool(self._buttons & 1 << 5)

    @property
    def two_middle(self) -> bool:
        return bool(self._buttons & 1 << 6)

    @property
    def two_left(self) -> bool:
        return bool(self._buttons & 1 << 7)

    @property
    def three_right(self) -> bool:
        return bool(self._buttons & 1 << 9)

    @property
    def three_middle(self) -> bool:
        return bool(self._buttons & 1 << 10)

    @property
    def three_left(self) -> bool:
        return bool(self._buttons & 1 << 11)

    @property
    def four_right(self) -> bool:
        return bool(self._buttons & 1 << 13)

    @property
    def four_middle(self) -> bool:
        return bool(self._buttons & 1 << 14)

    @property
    def four_left(self) -> bool:
        return bool(self._buttons & 1 << 15)

    @property
    def representation(self) -> str:
        modifier_str = '{n}{a}{c}{s}'.format(
            n='N' if self.num else '',
            a='A' if self.alt else '',
            c='C' if self.ctrl else '',
            s='S' if self.shift else '',
        )

        row_strs = []
        rows = [
            [self.one_right, self.one_middle, self.one_left],
            [self.two_right, self.two_middle, self.two_left],
            [self.three_right, self.three_middle, self.three_left],
            [self.four_right, self.four_middle, self.four_left],
        ]
        for row in rows:
            left, middle, right = row

            representation = '{right}{middle}{left}'.format(
                right='R' if right else '',
                middle='M' if middle else '',
                left='L' if left else '',
            )
            if len(representation) > 1:
                representation = f'({representation})'
            elif len(representation) == 0:
                representation = 'O'

            row_strs.append(representation)

        row_str = ''.join(row_strs)

        representation = row_str
        if modifier_str:
            representation = f'{modifier_str} {row_str}'

        return representation

    def __str__(self):
        mapping_strs = [
            f'<{c.key_combination}>' for c in self.mappings
        ]
        mapping_str = ''.join(mapping_strs)
        return f'{self.representation} -> {mapping_str}'

    def __repr__(self):
        return f"<Chord {self}>"


class Config:
    def __init__(
        self,
        version=0,
        sleep_timeout=1500,
        mouse_left_action=0,
        mouse_middle_action=0,
        mouse_right_action=0,
        mouse_acceleration=10,
        key_repeat_delay=100,
        options_a=0,
        options_b=0,
        options_c=0,
        chords=None
    ):
        self._version: int = version

        self._sleep_timeout: int = sleep_timeout

        self._mouse_left_action: int = mouse_left_action
        self._mouse_middle_action: int = mouse_middle_action
        self._mouse_right_action: int = mouse_right_action

        self._mouse_acceleration: int = mouse_acceleration
        self._key_repeat_delay: int = key_repeat_delay

        self._options_a: int = options_a
        self._options_b: int = options_b
        self._options_c: int = options_c

        self._chords: List[Chord] = []
        if chords:
            self._chords.extend(chords)

    @property
    def version(self) -> int:
        return self._version

    @property
    def sleep_timeout(self) -> int:
        return self._sleep_timeout

    @property
    def mouse_left_action(self) -> int:
        return self._mouse_left_action

    @property
    def mouse_middle_action(self) -> int:
        return self._mouse_middle_action

    @property
    def mouse_right_action(self) -> int:
        return self._mouse_right_action

    @property
    def mouse_acceleration(self) -> int:
        return self._mouse_acceleration

    @property
    def key_repeat_delay(self) -> int:
        return self._key_repeat_delay

    @property
    def options_a(self) -> int:
        return self._options_a

    @property
    def options_b(self) -> int:
        return self._options_b

    @property
    def options_c(self) -> int:
        return self._options_c

    @property
    def chords(self) -> List[Chord]:
        return self._chords

    @property
    def enable_key_repeat(self) -> bool:
        return bool(self.options_a & 1 << 0)

    @property
    def enable_direct_key_mode(self) -> bool:
        return bool(self.options_a & 1 << 1)

    @property
    def joystick_mouse_click(self) -> MouseClick:
        if self.options_a & 1 << 2:
            return MouseClick.left
        return MouseClick.right

    @property
    def enable_bluetooth_radio(self) -> bool:
        return not bool(self.options_a & 1 << 3)

    @property
    def enable_sticky_num(self) -> bool:
        return bool(self.options_a & 1 << 4)

    @property
    def enable_sticky_shift(self) -> bool:
        return bool(self.options_a & 1 << 7)

    @property
    def enable_haptic_feedback(self) -> bool:
        return bool(self.options_c & 1 << 0)

    @classmethod
    def from_path(cls, path: str) -> Config:
        with open(path, 'rb') as inf:
            return cls.from_file(inf)

    @classmethod
    def from_file(cls, file_obj: BinaryIO) -> Config:
        header = file_obj.read(16)
        (
            version,
            options_a,
            chord_count,
            sleep_timeout,
            mouse_left_action,
            mouse_middle_action,
            mouse_right_action,
            mouse_acceleration,
            key_repeat_delay,
            options_b,
            options_c
        ) = struct.unpack(
            "<BBHHHHHBBBB",
            header,
        )

        all_chords_bytes = file_obj.read(chord_count * 4)

        chords_bytes = [
            all_chords_bytes[i:i+4]
            for i in range(0, len(all_chords_bytes), 4)
        ]

        string_chord_count = 0 
        for chord_bytes in chords_bytes:
            type_byte = chord_bytes[2]
            if type_byte == 0xff:
                string_chord_count += 1

        string_table_bytes = file_obj.read(string_chord_count * 4)
        string_table = [
            struct.unpack('<I', string_table_bytes[i:i+4])[0]
            for i in range(0, len(string_table_bytes), 4)
        ]

        chord_mappings: Dict[int, ChordMapping] = {}
        while True:
            position = file_obj.tell()
            mappings = []

            try:
                length = struct.unpack('<H', file_obj.read(2))[0]
            except struct.error:
                break

            end = position + length

            while file_obj.tell() < end:
                (
                    modifier_byte,
                    keycode
                ) = struct.unpack(
                    "<BB",
                    file_obj.read(2),
                )

                mappings.append(
                    ChordMapping(modifier_byte, keycode)
                )

            chord_mappings[position] = mappings

        chords = []
        for chord_bytes in chords_bytes:
            (
                representation, hid_modifier, hid_keycode
            ) = struct.unpack('<HBB', chord_bytes)

            # If the hid_modifier is 0xff, we're storing
            # the ID of a string instead of an actual keycode
            if hid_modifier == 0xff:
                keycodes = chord_mappings[string_table[hid_keycode]]
            else:
                keycodes = [ChordMapping(hid_modifier, hid_keycode)]

            chords.append(Chord(representation, keycodes))

        return Config(
            version=version,
            sleep_timeout=sleep_timeout,
            mouse_left_action=mouse_left_action,
            mouse_middle_action=mouse_middle_action,
            mouse_right_action=mouse_right_action,
            mouse_acceleration=mouse_acceleration,
            key_repeat_delay=key_repeat_delay,
            options_a=options_a,
            options_b=options_b,
            options_c=options_c,
            chords=chords,
        )
