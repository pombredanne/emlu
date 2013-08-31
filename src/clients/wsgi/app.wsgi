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

import json

from bottle import route, view
from gi.repository import Gio

from .dbus import *


main_template = '''\
<!DOCTYPE HTML>

<html>

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>ecryptfs-mlu web client</title>
    <link rel="stylesheet" href="style.css">
</head>

<body>

    <section >

    </section>

    <footer>
        <p>Copyright (C) 2013 ecryptfs-mlu project.</p>
    </footer>

</body>

</html>
'''

@route('/')
@view('main.tpl')
def root():

    return {}

