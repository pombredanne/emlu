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
Module for mount commands wrappers and fstab file parsing.

Note: This modules is Python 2.7 and 3.x compatible.
"""

import os
import shlex
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


def get_mounts(config):

    # Get all configured visible mount points
    cfg = [m for m in config['mounts'] if not m['hidden']]

    # Get all fstab defined ecryptfs file systems and filter if force
    # options are set
    dfd = [m for m in parse_fstab() if m['type'] == 'ecryptfs']
    fopts = set(config['force-options'])
    if fopts:
        dfd = [d for d in dfd if set(d['options']) >= fopts]
    dfd = [d['mp'] for d in dfd]

    # Get currently mounted ecryptfs file systems
    mtd = [m['mp'] for m in parse_mount() if m['type'] == 'ecryptfs']

    # Now we want:
    #     Configured, visible, defined, well defined, with mount
    #     status, list of mount points.
    mounts = []
    for c in cfg:
        if c['mp'] not in dfd:
            continue
        m = {
            'name'   : c['name'],
            'mp'     : c['mp'],
            'mounted': c['mp'] in mtd
        }
        mounts.append(m)

    return mounts


def mount(mp, pwd):

    mts = get_mounts()

    # Check if valid mount point
    md = None
    for m in mts:
        if m['mp'] == mp:
            md = m
            break
    if not md:
        return -1

    # Check if mounted
    if md['mounted']:
        return -2

    # Check mount point
    if not os.path.exits(mp) or not os.path.isdir(mp):
        return -3

    # Execute mount cmd
    in_fd, out_fd = os.pipe()

    pss = 'passphrase_passwd={}'.format(pwd)
    os.write(out_fd, pss)
    os.close(out_fd)
    del pss

    cmd = '/bin/mount {mp} -o key=passphrase:passphrase_passwd_fd={fd}'.format(
            mp=mp,
            fd=in_fd
        )

    ret_code = subprocess.call(shlex.split(cmd))
    os.close(in_fd)

    if ret_code != 0:
        sys.stderr.write(
            'Unable to mount \'{mp}\'. mount exit code {c}\n'.format(
                mp=mp, c=ret_code
            )
        )
        return -4

    return 0


def umount(mp):

    mts = get_mounts()

    # Check if valid mount point
    md = None
    for m in mts:
        if m['mp'] == mp:
            md = m
            break
    if not md:
        return -1

    # Check if mounted
    if not md['mounted']:
        return -2

    # Execute umount cmd
    cmd = '/bin/umount {mp}'.format(mp=mp)
    ret_code = subprocess.call(shlex.split(cmd))
    if ret_code != 0:
        sys.stderr.write(
            'Unable to umount \'{mp}\'. umount exit code {c}\n'.format(
                mp=mp, c=ret_code
            )
        )
        return -3

    return 0


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
