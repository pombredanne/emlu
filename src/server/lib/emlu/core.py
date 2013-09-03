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
EMLU core module.
"""

import json
from threading import Thread

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

from .mount import get_mounts as _get_mounts
from .mount import mount as _mount
from .mount import umount as _umount

from .config import default_conf
from .daemon import GenericDaemon


class MountPoint():

    def __init__(self, mp, name, timeout):
        self.mp = mp
        self.timeout = timeout


class EMLUDaemon(GenericDaemon):

    def __init__(self, config):

        # Handle config dict
        conf = default_conf.copy()
        conf.update(config)
        conf['stdout'] = conf['log']
        conf['stderr'] = conf['log']

        super(EMLUDaemon, self).__init__(config)

        # Register functions
        self.server = SimpleJSONRPCServer((self.addr, self.port))
        self.server.register_function(self.get_mounts)
        self.server.register_function(self.mount)
        self.server.register_function(self.umount)

        self.pool = []
        for i in range(conf['pool']):
            self.pool.append(Thread(target=self.server.serve_forever))

    #--- Exposed methods -------------------------------------------------------
    def get_mounts(self):
        print('get_mounts()')
        return json.dumps(_get_mounts())

    def mount(self, mp, pwd, timeout):
        print('mount({}, ******)'.format(mp))
        code = _mount(mp, pwd)
        if code == 0:
            self.watch(mp, timeout)
        return code

    def umount(self, mp):
        print('umount({})'.format(mp))
        code = _umount(mp)
        if code == 0:
            self.unwatch(mp)
        return code

    #--- Daemon methods --------------------------------------------------------
    def loop(self):

        print('Starting EMLU server at {}:{}'.format(self.addr, self.port))

        # Start working threads
        for t in self.pool:
            t.start()

        # Block forever
        while True:
            sleep(sys.maxint)

    def terminate(self):

        # Shutdown server (and working threads)
        self.server.shutdow()

        # FIXME: Umount all opened volumes

        # Wait for all threads to finish
        for t in self.pool:
            t.join()