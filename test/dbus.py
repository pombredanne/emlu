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
sys.path = ['../src/lib'] + sys.path[1:]

import subprocess
import glib
import dbus

from emlu.service import dbus_method, DBusService


class TestDBus(DBusService):

    def __init__(self):

        domain = 'org.emlu'
        #bus = dbus.SystemBus()
        bus = dbus.SessionBus()
        super(TestDBus, self).__init__(bus, domain)

    @dbus_method(in_sig='s', out_sig='s')
    def hello(self, message):
        if message == 'error':
            raise ValueError('Requested error')
        return 'Good day {}'.format(message)


if __name__ == '__main__':

    service = TestDBus()

    def send_request(arg):
        print('\n----- sending request hello("{}") -------'.format(arg))
        subprocess.call(
                ['gdbus', 'call', '-e', '-d', service.dbus_name,
                 '-o', '/', '-m', '{}.{}'.format(service.dbus_name, 'hello'), arg]
            )
        return False


    ml = glib.MainLoop()

    # Program some requests
    glib.timeout_add(1000, send_request, 'World')
    glib.timeout_add(2000, send_request, 'error')

    # Program termination and run
    glib.timeout_add(3000, ml.quit)
    ml.run()
