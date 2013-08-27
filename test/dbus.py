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

from gi.repository import GLib
from emlu.dbus import dbus_method, DBusService

DBUS_WKN = 'org.emlu.Test'

class TestDBus(DBusService):
    def __init__(self):
        super(TestDBus, self).__init__()
        self.number = 10
    @dbus_method(dbus_interface=DBUS_WKN + '.Hello',
                 in_signature='s', out_signature='s')
    def hello(self, message):
        if message == 'error':
            raise ValueError('Requested error')
        return 'Good day {}'.format(message)

# These spawn a separate process for doing queries (cheesy hack), so our main
# loop can keep runnin
def send_request(arg):
    print '\n----- sending request hello("%s") -------' % arg
    subprocess.Popen(['gdbus', 'call', '-e', '-d', 'de.piware.Demo', '-o', '/',
        '-m', 'de.piware.Demo.Hello.hello', arg])
    return False

def send_property_get():
    print '\n----- sending property get -------'
    subprocess.Popen(['gdbus', 'call', '-e', '-d', 'de.piware.Demo', '-o', '/',
        '-m', 'org.freedesktop.DBus.Properties.Get', 'de.piware.Demo.Hello', 'number'])
    return False

def send_property_set():
    print '\n----- sending property set -------'
    subprocess.Popen(['dbus-send', '--print-reply', '--dest=de.piware.Demo',
            '/', 'org.freedesktop.DBus.Properties.Set',
            'string:de.piware.Demo.Hello', 'string:number',
            'variant:int32:99'])
    return False


if __name__ == '__main__':

    service = PiwareDemo('/')

    bus_id = Gio.bus_own_name(
            Gio.BusType.SESSION,
            'de.piware.Demo',
            Gio.BusNameOwnerFlags.NONE,
            service._add_to_connection,
            None, None
        )

    # now send some requests to check the result
    ml = GLib.MainLoop()
    GLib.timeout_add(1000, send_request, 'Martin')
    GLib.timeout_add(2000, send_request, 'error')
    #GLib.timeout_add(3000, send_property_get)
    #GLib.timeout_add(5000, send_property_set)
    #GLib.timeout_add(6000, send_property_get)
    GLib.timeout_add(3000, ml.quit)
    ml.run()

    print 'unowning bus name...'
    Gio.bus_unown_name(bus_id)
    GLib.timeout_add(500, ml.quit)
    ml.run()
