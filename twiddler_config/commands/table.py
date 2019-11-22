import argparse
import sqlite3
from typing import Dict, List

import texttable

from ..config import Button, Config
from .base import Command


class Table(Command):
    def create_tables(self):
        cursor = self.db.cursor()

        cursor.execute("""
            CREATE TABLE chords (
                num boolean,
                alt boolean,
                ctrl boolean,
                shift boolean,

                one_right boolean,
                one_middle boolean,
                one_left boolean,

                two_right boolean,
                two_middle boolean,
                two_left boolean,

                three_right boolean,
                three_middle boolean,
                three_left boolean,

                four_right boolean,
                four_middle boolean,
                four_left boolean,

                modifier_count int,
                button_count int,
                representation str
            )
        """)
        self.db.commit()

    def insert_chords(self):
        cursor = self.db.cursor()
        for chord in self.cfg.chords:
            cursor.execute("""
                    INSERT INTO chords
                    SELECT
                        ?, ?, ?, ?,
                        ?, ?, ?,
                        ?, ?, ?,
                        ?, ?, ?,
                        ?, ?, ?,
                        ?, ?, ?
                """, (
                    chord.num,
                    chord.alt,
                    chord.ctrl,
                    chord.shift,

                    chord.one_right,
                    chord.one_middle,
                    chord.one_left,

                    chord.two_right,
                    chord.two_middle,
                    chord.two_left,

                    chord.three_right,
                    chord.three_middle,
                    chord.three_left,

                    chord.four_right,
                    chord.four_middle,
                    chord.four_left,

                    len(
                        list(
                            filter(
                                lambda x: x,
                                [
                                    chord.num,
                                    chord.alt,
                                    chord.ctrl,
                                    chord.shift,
                                ],
                            )
                        )
                    ),
                    len(
                        list(
                            filter(
                                lambda x: x,
                                [
                                    chord.one_right,
                                    chord.one_middle,
                                    chord.one_left,

                                    chord.two_right,
                                    chord.two_middle,
                                    chord.two_left,

                                    chord.three_right,
                                    chord.three_middle,
                                    chord.three_left,

                                    chord.four_right,
                                    chord.four_middle,
                                    chord.four_left,
                                ],
                            )
                        )
                    ),

                    ''.join([
                        f'<{key.key_combination}>'
                        for key in chord.mappings
                    ])
                )
            )
        self.db.commit()

    def get_chord(self, pressed: List[Button]):
        buttons: Dict[Button, bool] = {
            button: True for button in pressed
        }

        curs = self.db.cursor()
        curs.execute("""
            SELECT representation
            FROM chords
            WHERE
                num = ?
                AND alt = ?
                AND ctrl = ?
                AND shift = ?
                AND one_right = ?
                AND one_middle = ?
                AND one_left = ?
                AND two_right = ?
                AND two_middle = ?
                AND two_left = ?
                AND three_right = ?
                AND three_middle = ?
                AND three_left = ?
                AND four_right = ?
                AND four_middle = ?
                AND four_left = ?
            """, (
                buttons.get(Button.num, False),
                buttons.get(Button.alt, False),
                buttons.get(Button.ctrl, False),
                buttons.get(Button.shift, False),

                buttons.get(Button.one_right, False),
                buttons.get(Button.one_middle, False),
                buttons.get(Button.one_left, False),

                buttons.get(Button.two_right, False),
                buttons.get(Button.two_middle, False),
                buttons.get(Button.two_left, False),

                buttons.get(Button.three_right, False),
                buttons.get(Button.three_middle, False),
                buttons.get(Button.three_left, False),

                buttons.get(Button.four_right, False),
                buttons.get(Button.four_middle, False),
                buttons.get(Button.four_left, False),
            )
        )

        results = curs.fetchall()
        if len(results) > 1:
            raise ValueError(
                f"Found two chords mapped to {pressed}!"
            )
        elif len(results) == 1:
            return results[0][0]

        # We might not have a match for this chord
        return ''

    def get_table(self, static: List[Button] = None):
        if static is None:
            static = []

        dynamic = [
            [
                [Button.one_left],
                [Button.one_middle],
                [Button.one_right],
            ],
            [
                [Button.one_left, Button.two_left],
                [Button.one_middle, Button.two_middle],
                [Button.one_right, Button.two_right],
            ],
            [
                [Button.two_left],
                [Button.two_middle],
                [Button.two_right],
            ],
            [
                [Button.two_left, Button.three_left],
                [Button.two_middle, Button.three_middle],
                [Button.two_right, Button.three_right],
            ],
            [
                [Button.three_left],
                [Button.three_middle],
                [Button.three_right],
            ],
            [
                [Button.three_left, Button.four_left],
                [Button.three_middle, Button.four_middle],
                [Button.three_right, Button.four_right],
            ],
            [
                [Button.four_left],
                [Button.four_middle],
                [Button.four_right],
            ],
        ]

        if self.right_to_left:
            for row in dynamic:
                row.reverse()

        table = []
        for button_row in dynamic:
            row = []
            for button_position in button_row:
                if len(button_position) == 1 and button_position[0] in static:
                    row.append('\u2022')
                elif (
                    len(button_position) > 1
                    and any(
                        pos in static for pos in button_position
                    )
                ):
                    row.append('')
                else:
                    row.append(
                        self.get_chord(
                            button_position + static
                        )
                    )

            table.append(row)

        return table

    def get_table_as_string(self, table):
        text = texttable.Texttable(max_width=0)
        text.set_cols_align(('c', 'c', 'c'))
        text.set_cols_dtype(('t', 't', 't'))
        #text.set_deco(texttable.Texttable.VLINES)
        #text.set_chars(('\u00a0', '\u00a0', '\u00a0', '\u00a0', ))
        text.add_rows(table)
        return text.draw()

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)
        parser.add_argument(
            '--right-to-left',
            '-r',
            help="Print buttons from right to left instead of left to right",
            action='store_true',
            default=False
        )

    def handle(self, args: argparse.Namespace) -> None:
        self.cfg = Config.from_path(args.path)

        self.db = sqlite3.connect(':memory:')
        self.right_to_left = args.right_to_left

        self.create_tables()
        self.insert_chords()

        enumerations = [
            [
                [],
                [Button.one_right],
                [Button.one_middle],
                [Button.one_left],
            ],
            [
                [Button.two_right],
                [Button.one_right, Button.two_right],
                [Button.one_right, Button.two_middle],
                [Button.one_right, Button.two_left],
            ],
            [
                [Button.two_middle],
                [Button.one_middle, Button.two_right],
                [Button.one_middle, Button.two_middle],
                [Button.one_middle, Button.two_left],
            ],
            [
                [Button.two_right],
                [Button.one_left, Button.two_middle],
                [Button.one_left, Button.two_left],
                [Button.four_left],
            ],
            [
                [Button.four_right],
                [Button.three_middle, Button.four_right],
                [Button.three_left, Button.four_middle],
                [Button.four_middle],
            ]
        ]

        table = texttable.Texttable(max_width=0)
        table.set_cols_align(len(enumerations[0]) * ['c'])
        table.set_deco(0)
        for enumeration_row in enumerations:
            row = []
            for enumeration_instance in enumeration_row:
                row.append(
                    self.get_table_as_string(
                        self.get_table(enumeration_instance)
                    )
                )

            table.add_row(row)

        print(table.draw())
