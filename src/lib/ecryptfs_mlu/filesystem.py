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
Module for mount command and fstab file parsing.

Note: This modules is Python 2.7 and 3.x compatible.
"""

import subprocess

def parse_mount():

    """
    Parse the output of the 'mount' command returning a list of dictionaries of
    the type:

    [   {   'file_system': 'proc',
            'mp' : '/proc',
            'options': ['rw', 'noexec', 'nosuid', 'nodev'],
            'type': 'proc'}
        ...
    ]

    This function can raise two exceptions:
        - OSError, if mount command cannot be found.
        - CalledProcessError, if the result of the execution of mount returns
          non-zero.
    """

    out = subprocess.check_output(['/bin/mount'])
    lines = out.split('\n')
    entries = []
    for l in lines:
        l = l.strip()
        if not l:
            continue
        parts = l.split()
        if len(parts) != 6:
            raise Exception('mount output is malformed.')

        entry = {
                'file_system': parts[0],
                'mp'         : parts[2],
                'type'       : parts[4],
                'options'    : parts[5][1:-1].split(','),
            }
        entries.append(entry)

    return entries


def is_mounted(mount_point):
    """
    Check if a particular mount point is already mounted.
    """
    mounted = parse_mount()
    for m in mounted:
        if m['mp'] == mount_point:
            return m
    return None


def parse_fstab():

    """
    Parse the fstab file returning a list of dictionaries of the type:

    [   {   'dump': '0',
            'file_system': 'proc',
            'mp' : '/proc',
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
                'mp'         : parts[1],
                'type'       : parts[2],
                'options'    : parts[3].split(','),
                'dump'       : parts[4],
                'pass'       : parts[5],
            }
        entries.append(entry)

    return entries


def is_listed(mount_point):
    """
    Check if a particular mount point is listed in the fstab.
    """
    listed = parse_fstab()
    for l in listed:
        if l['mp'] == mount_point:
            return l
    return None


# Test
if __name__ == '__main__':
    from pprint import pprint
    print('################ parse_mount() ################')
    pprint(parse_mount(), indent=4)
    print('################ is_mounted() ################')
    print('is_mounted(\'/proc\') : {}'.format(is_mounted('/proc')))
    print('################ parse_fstab() ################')
    pprint(parse_fstab(), indent=4)
    print('################ is_listed() ################')
    print('is_listed(\'/proc\') : {}'.format(is_listed('/proc')))
