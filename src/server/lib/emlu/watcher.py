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


class EMLUWatcher(object):

    class Worker(Thread):
        def __init__(self):
            self.event = Event()
            self.queue = Queue()

    def __init__(self):

        self.worker = Worker()
        self.worker.start()

    def watch(self, mp, timeout):
        self.worker.queue.put((True, mp, timeout))
        self.worker.event.set()

    def unwatch(self, mp):
        self.worker.queue.put((False, mp))
        self.worker.event.set()

