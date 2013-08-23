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
Module for fstab file parsing.
See http://en.wikipedia.org/wiki/Fstab

Note: This modules is Python 2.7 and 3.x compatible.
"""

def parse_fstab():

    """
    Parse the fstab file returning a list of dictionaries of the type:

    [   {   'dump': '0',
            'file_system': 'proc',
            'mount_point': '/proc',
            'options': ['nodev', 'noexec', 'nosuid'],
            'pass': '0',
            'type': 'proc'},
        ...
    ]

    This function can raise two exceptions:
        - IOError, if fstab is unreadable or doesn't exists.
        - Exception, if fstab is empty or malformed.
    """

    fstab = '/etc/fstab'

    lines = []
    with open(fstab, 'r') as f:
        for l in f:
            l = l.strip()
            if l and not l.startswith('#'):
                lines.append(l)

    if not lines:
        raise Exception("fstab file is empty.")

    entries = []
    for l in lines:
        parts = l.split()

        if len(parts) != 6:
            raise Exception('fstab is malformed.')

        entry = {
                'file_system': parts[0],
                'mount_point': parts[1],
                'type'       : parts[2],
                'options'    : parts[3].split(','),
                'dump'       : parts[4],
                'pass'       : parts[5],
            }
        entries.append(entry)

    return entries

# Test
if __name__ == '__main__':
    from pprint import pprint
    pprint(parse_fstab(), indent=4)