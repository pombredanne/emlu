# -*- coding:utf-8 -*-
#
# Copyright (C) 2013 Carlos Jenkins <carlos@jenkins.co.cr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
EMLU watcher module.
"""

import os
import sys

if sys.version_info[0] < 3:
    from Queue import Queue
else:
    from queue import Queue
from threading import Thread, Event

from .mount import umount


_POLL = 30

class EMLUWatcher(Thread):

    def __init__(self):
        # Communication
        self._event = Event()
        self._queue = Queue()
        # Local
        self._shutdown = False
        self._watched = []

    def run(self):
        while not self._shutdown:
            # Wait for event
            self._event.wait(_POLL)
            self._event.clear()

            # Quit thread if requested
            if self._shutdown:
                break

            # Attend messages
            while True:
                try:
                    item = self._queue.get(block=False)
                    # Fix me, do something with item
                except Empty as e:
                    break

            # Attend inotify events
            # FIXME: Implement.

        # Umount all watched mounts
        # FIXME: Implement.


    #--- Local methods ---------------------------------------------------------


    #--- Methods to be called from another thread ------------------------------
    def stop(self):
        self._shutdown = True
        self._event.set()

    def watch(self, mp, timeout=-1):
        if timeout != 0:
            self._queue.put((True, mp, timeout))
            self._event.set()

    def unwatch(self, mp):
        self._queue.put((False, mp))
        self._event.set()

