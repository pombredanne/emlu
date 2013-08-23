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

def read_config():

    config = '/etc/ecryptfs-mlu.conf'
    if not exists(config):
        config = 'ecryptfs-mlu.conf'

    with open(config, 'r') as f:
        return json.loads(f.read())


# Test
if __name__ == '__main__':
    from pprint import pprint
    pprint(read_config())
