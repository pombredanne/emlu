# -*- coding:utf-8 -*-
#
# Copyright (C) 2009 Sander Marechal and contributors.
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
Test module for ecryptfs-mlu daemon module.
"""


import sys
sys.path.insert(0, '../src/lib')

import os
from time import sleep
from ecryptfs_mlu.daemon import GenericDaemon, DaemonCtrl


class TestDaemon(GenericDaemon):

    def __init__(self, config):
        super(TestDaemon, self).__init__(config=config)

    def loop(self):
        counter = 0
        while True:
            print('TestDaemon loop() #{}'.format(counter))
            counter += 1;
            sleep(10)

    def terminate(self):
        print('Terminating daemon...')


if __name__ == '__main__':

    usage = 'Usage: {} [start|stop|restart|foreground]'.format(sys.argv[0])
    if len(sys.argv) < 2:
        sys.stderr.write(usage + '\n')
        sys.exit(1)

    config = {
            'pidfile'  : '/var/run/daemon.py.pid',
            'workdir'  : '/',
            'stdin'    : os.devnull,
            'stdout'   : '/var/log/daemon.py.log',
            'stderr'   : '/var/log/daemon.py.log',
        }
    dc = DaemonCtrl(TestDaemon, config)

    param = sys.argv[1]
    if param == 'start':
        dc.start()
    elif param == 'stop':
        dc.stop()
    elif param == 'restart':
        dc.restart()
    elif param == 'foreground':
        dc.foreground()
    else:
        sys.stderr.write('Unknown param "{}".'.format(param) + '\n')
        sys.exit(2)

