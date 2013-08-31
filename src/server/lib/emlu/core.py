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

import .mount as mm
from .config import default_conf
from .daemon import GenericDaemon


class EMLUDaemon(GenericDaemon):

    def __init__(self, config):

        # Handle config dict
        conf = default_conf.copy()
        conf.update(config)
        conf['stdout'] = conf['log']
        conf['stderr'] = conf['log']

        super(EMLUDaemon, self).__init__(config)

        self.server = SimpleJSONRPCServer((self.addr, self.port))
        self.server.register_function(self.get_mounts)
        self.server.register_function(self.mount)
        self.server.register_function(self.umount)

    def watch(self, mp, timeout):
        # FIXME Implement
        pass

    #--- Exposed methods -------------------------------------------------------
    def get_mounts(self):
        print('get_mounts()')
        return json.dumps(mm.get_mounts())

    def mount(self, mp, pwd, timeout):
        print('mount({}, ******)'.format(mp))
        code = mm.mount(mp, pwd)
        if code == 0:
            self.watch(mp, timeout)
        return code

    def umount(self, mp):
        print('umount({})'.format(mp))
        code = mm.umount(mp)
        if code == 0:
            self.unwatch(mp)
        return code

    #--- Daemon methods --------------------------------------------------------
    def loop(self):
        print('Starting EMLU server at {}:{}'.format(self.addr, self.port))
        server.serve_forever()

    def terminate(self):
        pass