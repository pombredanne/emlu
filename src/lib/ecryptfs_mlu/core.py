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

from time import sleep
from gi.repository import GObject
from .daemon import GenericDaemon
from .filesystem import parse_fstab, parse_mount

def get_mounts(config):

    # Get all configured visiable mount points
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


class MountPoint(object):

    def __init__(self, name, mount_point, publish):

        self.name = name
        self.mount_point = mount_point
        self.publish = publish

        #self.timestamp =
        #self.watch_manager =

class MLUDaemon(GenericDaemon):

    def loop(self):
        GObject.MainLoop().run()

    def terminate(self):
        pass


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_mounts())

