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
Test script for emlu dbus module.
"""

import sys
sys.path.insert(0, '../src/lib')

import subprocess

from gi.repository import Gio, GLib
from emlu.dbus import dbus_method, DBusService

DBUS_WKN = 'org.emlu.TestDBus'

class TestDBus(DBusService):
    def __init__(self):
        super(TestDBus, self).__init__()

        self.bus_id = Gio.bus_own_name(
            Gio.BusType.SESSION,
            DBUS_WKN,
            Gio.BusNameOwnerFlags.NONE,
            self._add_to_connection,
            None, None
        )

    @dbus_method(interface=DBUS_WKN + '.hello', in_sig='s', out_sig='s')
    def hello(self, message):
        if message == 'error':
            raise ValueError('Requested error')
        return 'Good day {}'.format(message)

# These spawn a separate process for doing queries (cheesy hack), so our main
# loop can keep running
def send_request(arg):
    print('\n----- sending request hello("{}") -------'.format(arg))
    subprocess.call(
            ['gdbus', 'call', '-e', '-d', DBUS_WKN,
             '-o', '/', '-m', DBUS_WKN + '.hello', arg]
        )
    return False


if __name__ == '__main__':

    service = TestDBus()
    ml = GLib.MainLoop()

    # Program some requests
    GLib.timeout_add(1000, send_request, 'World')
    GLib.timeout_add(2000, send_request, 'error')

    # Program termination and run
    GLib.timeout_add(3000, ml.quit)
    ml.run()

    print('Unowning bus name...')
    Gio.bus_unown_name(service.bus_id)
    GLib.timeout_add(500, ml.quit)
    ml.run()
