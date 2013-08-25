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

from gi.repository import Gio, GObject
from .daemon import GenericDaemon
from .dbus import DBusService, dbus_method
from .mount import get_mounts, mount, umount

DBUS_WKN = 'org.ecryptfs.mlu.MLUDaemon'

class MLUDaemon(GenericDaemon, DBusService):

    def __init__(config):
        super(MLUDaemon, self).__init__(
                config=config,
                object_path='/'
            )

        # Publish service
        self.bus_id = Gio.bus_own_name(
                Gio.BusType.SYSTEM,
                DBUS_WKN,
                Gio.BusNameOwnerFlags.NONE,
                self._add_to_connection,
                None,
                None
            )

    #--- DBus methods ----------------------------------------------------------
    @dbus_method(dbus_interface=DBUS_WKN + '.GetMounts',
                 in_signature='', out_signature='s')
    def get_mounts(self):
        print('get_mounts()')
        return 'here should be an encoded json'

    @dbus_method(dbus_interface=DBUS_WKN + '.Mount',
                 in_signature='ss', out_signature='i')
    def mount(self, mp, pwd):
        print('mount({}, {})'.format(mp, pwd))
        return 0

    @dbus_method(dbus_interface=DBUS_WKN + '.Umount',
                 in_signature='s', out_signature='i')
    def umount(self, mp):
        print('umount({})'.format(mp))
        return 0

    #--- Daemon methods --------------------------------------------------------
    def loop(self):
        # Run GLib main loop
        self.ml = GObject.MainLoop().run()

    def terminate(self):
        # Stop GLib main loop
        self.ml.quit()

        # Unpublish service
        Gio.bus_unown_name(self.bus_id)
