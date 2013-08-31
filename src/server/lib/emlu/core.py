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

import json

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

from .mount import get_mounts, mount, umount
from .daemon import GenericDaemon


default_conf = {
        # Server
        'addr'         : 'locahost',
        'port'         : 6464,
        'prefork'      : False,
        # Core
        'timeout'      : 30,
        'samba-check'  : True,
        # Daemon
        'pid'          : '/var/run/emlu.pid',
        'log'          : '/var/log/emlu.log',
        # Mounts
        'force-options': ['user', 'noauto'],
        'mounts'       : [],
    }


def exposed(fn):
    server.register_function(fn)
    return fn


class EMLUDaemon(GenericDaemon):

    def __init__(self, config):
        super(EMLUDaemon, self).__init__(config)

        conf = {
            'addr'     : 'localhost',
            'port'     : 6464,
            'stdin'    : os.devnull,
            'stdout'   : os.devnull,
            'stderr'   : os.devnull,
        }
        conf.update(config)

        self.server = SimpleJSONRPCServer((self.addr, self.port))

    #--- Exposed methods -------------------------------------------------------
    @exposed
    def get_mounts(self):
        print('get_mounts()')
        return json.dumps(get_mounts())

    @exposed
    def mount(self, mp, pwd, timeout):
        print('mount({}, ******)'.format(mp))
        code = mount(mp, pwd)
        if code == 0:
            self.watch(mp, timeout)
        return code

    @exposed
    def umount(self, mp):
        print('umount({})'.format(mp))
        code = umount(mp)
        if code == 0:
            self.unwatch(mp)
        return code

    #--- Daemon methods --------------------------------------------------------
    def loop(self):
        server.serve_forever()

    def terminate(self):
        pass
