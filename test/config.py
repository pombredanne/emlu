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
Test script to generate a config file.
"""

import json


config = {
        'timeout'      : 30,
        'pid'          : '/var/run/ecryptfs-mlu.pid',
        'log'          : '/var/log/ecryptfs-mlu.log',
        'samba-check'  : True,
        'force-options': ['user', 'noauto'],
        'mounts'       : [
                {
                    'name'   : 'user1',
                    'mp'  : '/media/mount1',
                    'hidden': False,
                }
            ],
    }

if __name__ == '__main__':
    print(json.dumps(config, indent=4))
