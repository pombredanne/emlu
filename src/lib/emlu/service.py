# -*- coding:utf-8 -*-
#
# Copyright (C) 2010 Martin Pitt <martin@piware.de>
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
"""

import dbus
import dbus.service
import dbus.mainloop.glib


#dbus.mainloop.glib.threads_init()
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

def dbus_method(in_sig=None, out_sig=None):

    def decorator(func):

        def wrapper(*args, **kwargs):
            print args
            name = '{}.{}'.format(self.dbus_name, func.__name__)
            func = dbus.service.method(
                    name, in_sig, out_sig
                )
            #func.dbus_name = name
            return func

        return wrapper

    return decorator


class DBusService(dbus.service.Object):
    def __init__(self, bus, dom, **kwargs):

        self.dbus_name = '{}.{}'.format(dom, self.__class__.__name__)
        self.dbus_path = '/' + self.dbus_name.replace('.','/')

        super(DBusService, self).__init__(
                dbus.service.BusName(self.dbus_name, bus),
                self.dbus_path, **kwargs
            )

