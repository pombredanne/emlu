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
Test script for emlu web client module.
"""

import sys
sys.path.insert(0, '../server/lib/')

from pprint import pprint

from emlu.mount import *


if __name__ == '__main__':
    print('################ parse_mount() ################')
    pprint(parse_mount(), indent=4)
    print('################ parse_mtab() ################')
    pprint(parse_mtab(), indent=4)
    print('################ parse_fstab() ################')
    pprint(parse_fstab(), indent=4)

