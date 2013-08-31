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

import sys
sys.path.insert(0, '../src/lib')

import json
from emlu.core import default_config


config = default_config.copy()

# Append example mount
config['mounts'].append(
        {
            'name'    : 'user1',
            'mp'      : '/media/mount1',
            'hidden'  : False,
            'timeout' : -1,
        }
    )

if __name__ == '__main__':
    print(json.dumps(config, indent=4))
