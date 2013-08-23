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

from time import sleep
from threading Thread, Event
from .daemon import GenericDaemon

class Mounter(Thread):
    def run(self):
        while True:
            sleep(10)


class MountPoint(object):

    def __init__(self, name, mount_point, publish):

        self.name = name
        self.mount_point = mount_point
        self.publish = publish

        self.timestamp =
        self.watch_manager =


class Umounter(Thread):

    def __init__(self, event, ):
        self.event = event
        self.


    def run(self):

        # Get list of mount points to watch (defined and already mounted)

        # Loop
        while True:
            shutdown = self.event.wait(self.timeout)
            if shutdown:
                break

        # Umount all mounts


class MLUDaemon(GenericDaemon):

    def init(self):

        self.m_event = Event()
        self.u_event = Event()

        self.m = Mounter(self.m_event)
        self.u = Umounter(self.u_event)

    def loop(self):

        self.init()
        while True:
            sleep(10)

    def terminate(self):

        self.m_event.set()
        self.m.join(1.0)

        self.u_event.set()
        self.u.join(1.0)

