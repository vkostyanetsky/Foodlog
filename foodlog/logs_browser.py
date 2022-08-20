#!/usr/bin/env python3

from collections import namedtuple

import keyboard
from vkostyanetsky import cliutils

from foodlog import logs_viewer


class LogsBrowser:
    _data: namedtuple

    _max_index: int = 0
    _index: int = 0

    _prev_log_hotkey: str = "Left"
    _next_log_hotkey: str = "Right"
    _exit_hotkey: str = "Esc"

    def __init__(self, data: namedtuple):
        self._data = data

        self._max_index = len(self._data.journal) - 1
        self._index = self._max_index

    def open(self) -> None:

        self.show_log_by_index()

        keyboard.add_hotkey(self._prev_log_hotkey, self.show_previous_fast)
        keyboard.add_hotkey(self._next_log_hotkey, self.show_next_fast)

        keyboard.wait(self._exit_hotkey)

        keyboard.remove_all_hotkeys()

    def show_log_by_index(self):

        cliutils.clear_terminal()

        info = logs_viewer.get(self._index, self._data)

        for line in info:
            print(line)

        print()
        print(
            f"Press [{self._prev_log_hotkey}] and "
            f"[{self._next_log_hotkey}] to switch logs."
        )
        print(f"Press [{self._exit_hotkey}] to return to the main menu.")

    def show_previous_fast(self):
        if self._index > 0:
            self._index -= 1
            self.show_log_by_index()

    def show_next_fast(self):
        if self._index < self._max_index:
            self._index += 1
            self.show_log_by_index()
