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
Module for reading a JSON formatted configuration file.

Note: This modules is Python 2.7 and 3.x compatible.
"""

import json
from os.path import exists


config_file = '/etc/emlu.conf'

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


def read_config():

    conf = default_conf.copy()

    with open(config_file, 'r') as f:
        conf.update(json.loads(f.read()))

    return conf


def write_config(new_conf={}):

    conf = default_conf.copy()
    conf.update(new_conf)

    with open(config_file, 'w') as f:
        f.write(json.dumps(conf, indent=4))


# Test
if __name__ == '__main__':
    from pprint import pprint
    pprint(read_config())
