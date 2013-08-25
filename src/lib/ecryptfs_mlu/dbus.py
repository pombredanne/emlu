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

import inspect
from gi.repository import Gio, GLib, GObject

class _Gio_DBusMethodInfo(object):
    interface = None
    in_args = None
    out_signature = None

def dbus_method(dbus_interface, in_signature=None, out_signature=None):
    def decorator(func):
        func._dbus_method = _Gio_DBusMethodInfo()
        func._dbus_method.interface = dbus_interface
        func._dbus_method.out_signature = out_signature or ''

        func._dbus_method.in_args = []
        in_signature_list = GLib.Variant.split_signature(in_signature)
        arg_names = inspect.getargspec(func).args
        arg_names.pop(0) # eat "self" argument
        if len(in_signature) != len(arg_names):
            raise TypeError, 'specified signature %s for method %s does not match length of arguments' % (str(in_signature_list), func.func_name)
        for pair in zip(in_signature_list, arg_names):
            func._dbus_method.in_args.append(pair)

        return func

    return decorator


class DBusService(object):

    class _DBusInfo:
        object_path = None
        connection = None
        reg_id = None
        methods = None # interface -> method_name -> info_map
                       # info_map keys: method_name, in_signature, out_signature

    def __init__(self, object_path='/', **kwargs):

        super(DBusService, self).__init__(**kwargs)

        self.__dbus_info = DBusService._DBusInfo()
        self.__dbus_info.object_path = object_path

        # set up the vtable maps, for more efficient lookups at runtime
        self.__dbus_info.methods = {}
        for id in dir(self):
            attr = getattr(self, id)
            if hasattr(attr, '_dbus_method'):
                self.__dbus_info.methods.setdefault(attr._dbus_method.interface, {})[id] = {
                    'in_args': attr._dbus_method.in_args,
                    'out_signature': attr._dbus_method.out_signature,
                }

    def _add_to_connection(self, connection, name=None):
        self.__dbus_info.connection = connection
        print 'add_to_connection', connection

        vtable = Gio.DBusInterfaceVTable.new()
        vtable.set_method_call(self.__dbus_method_call, None)
        vtable.set_get_property(self.__dbus_get_property, None)
        vtable.set_set_property(self.__dbus_set_property, None)

        node_info = Gio.DBusNodeInfo.new_for_xml(self.__dbus_introspection_xml())
        print '--- XML: ---\n%s\n-------' % node_info.generate_xml(4).str

        for interface in self.__dbus_info.methods:
            self.__dbus_info.reg_id = connection.register_object(
                    self.__dbus_info.object_path,
                    node_info.lookup_interface(interface),
                    vtable,
                    None,
                    (lambda *args: None), # workaround for gbo#655051
                    )
            print 'registered object id %i for interface %s' % (self.__dbus_info.reg_id, interface)

    def _remove_from_connection(self):
        print 'remove_from_connection', self.__dbus_info.connection
        self.connection.unregister_object(self.__dbus_info.reg_id)
        self.__dbus_info.reg_id = None
        self.__dbus_info.connection = None

    def __dbus_introspection_xml(self):
        '''Generate introspection XML'''

        xml = '<node>\n'

        for interface in self.__dbus_info.methods:
            xml += '  <interface name="%s">\n' % interface

            for method, data in self.__dbus_info.methods[interface].items():
                xml += '    <method name="%s">\n' % method
                for (sig, name) in data['in_args']:
                    xml += '      <arg type="%s" name="%s" direction="in"/>' % (sig, name)
                xml += '      <arg type="%s" name="return" direction="out"/>' % data['out_signature']
                xml += '    </method>\n'

            xml += '  </interface>\n'

        xml += '</node>\n'
        return xml

    def __dbus_method_call(self, conn, sender, object_path, iface_name, method_name,
            parameters, invocation, user_data):

        print 'method call: %s %s.%s(%s)' % (object_path, iface_name, method_name, str(parameters))

        try:
            info = self.__dbus_info.methods[iface_name][method_name]
        except KeyError:
            invocation.return_error_literal(Gio.dbus_error_quark(),
                    Gio.DBusError.UNKNOWN_METHOD,
                    'No such interface or method: %s.%s' % (iface_name, method_name))
            return

        print 'method_call: got info', info
        print 'calling with', parameters.unpack()
        try:
            ret = getattr(self, method_name)(*parameters.unpack())
            print 'method_call: got ret', ret
            invocation.return_value(GLib.Variant('(' + info['out_signature'] + ')', (ret,)))
        except Exception as e:
            print 'method_call: got exception', e
            invocation.return_error_literal(Gio.dbus_error_quark(),
                    Gio.DBusError.IO_ERROR,
                    'Method %s.%s failed with: %s' % (iface_name, method_name, str(e)))

    def __dbus_get_property(self, conn, sender, object_path, iface_name, prop_name,
            error, user_data):
        error = GLib.Error.new_literal(GLib.io_channel_error_quark(), 1,
                'Not implemented yet')
        return None

    def __dbus_set_property(self, conn, sender, object_path, iface_name, prop_name,
            value, error, user_data):
        error = GLib.Error.new_literal(GLib.io_channel_error_quark(), 1,
                'Not implemented yet')
        return False

