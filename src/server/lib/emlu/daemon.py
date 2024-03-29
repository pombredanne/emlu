# -*- coding:utf-8 -*-
#
# Copyright (C) 2009 Sander Marechal <s.marechal@jejik.com>
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
Generic daemon and control class.
"""
# Note: This modules is Python 2.7 and 3.x compatible.

import os
import sys
import time
import signal
import traceback


class GenericDaemon(object):
    """
    A generic UNIX daemon base class.

    Subclass this class and override the loop() method with the continous task
    your daemon needs to perform. The loop() method should never return.
    Optionally, override the terminate() method to implement any clean up or
    any routines that should run at daemon termination (daemons are always
    terminated by a SIGTERM signal).

    The config parameter is a dictionary that can contain whatever data your
    daemon requires. The base class will use the following keys if defined in
    the dictionary:

    - 'pidfile': path to put the pid file. Default is '/var/run/daemon.py.pid'
    - 'workdir': working directory of the daemon. Default is '/'
    - 'stdin'  : path to a file to use as std input. Default is os.devnull
    - 'stdout' : path to a file to use as std output. Default is os.devnull
    - 'stderr' : path to a file to use as std error. Default is os.devnull
    """
    def __init__(self, config={}, **kwargs):

        super(GenericDaemon, self).__init__(**kwargs)

        conf = {
            'pidfile'  : '/var/run/daemon.py.pid',
            'workdir'  : '/',
            'stdin'    : os.devnull,
            'stdout'   : os.devnull,
            'stderr'   : os.devnull,
        }
        conf.update(config)
        self.config = conf

        self.__dict__.update(conf)

    def _fatal(self, msg, err):
        """
        Print error message and exit.
        """
        sys.stderr.write(msg.format(err))
        sys.stderr.write('\n')
        sys.exit(1)

    def daemonize(self):
        """
        Deamonize process using UNIX double fork mechanism.

        See W. Richard Stevens "Advanced Programming in the UNIX Environment"
        for details (ISBN 0201563177).
        """

        # Check working directory
        if not os.path.isdir(self.workdir):
            self._fatal('Working directory doesn\'t exist.', '')

        # Exit first parent process
        try:
            pid = os.fork()
            # If parent, return to continue processing
            if pid > 0:
                return
        except OSError as err:
            self._fatal('Fork #1 failed: {0}', err)

        # Decouple from parent environment
        try:
            os.chdir(self.workdir)
        except OSError as err:
            self._fatal('Path change failed: {0}', err)

        # Run program in a new session
        os.setsid()

        # Set the new numeric mask
        os.umask(0)

        # Exit from second parent (first child)
        try:
            pid = os.fork()
            if pid > 0:
                os._exit(0)
        except OSError as err:
            self._fatal('Fork #2 failed: {0}', err)

        # Write pidfile
        pid = str(os.getpid())
        print('[{}]'.format(pid))
        with open(self.pidfile, 'w+') as f:
            f.write(pid + '\n')

        # Redirect standard file descriptors
        sys.stdin.close()
        sys.stdout.close()
        sys.stderr.close()
        sys.stdin = file(self.stdin, 'r')
        sys.stdout = file(self.stdout, 'a+', 1)
        sys.stderr = file(self.stderr, 'a+', 0)

        # Register termination routine
        signal.signal(signal.SIGTERM, self._sigterm_handler)

        # Run daemon
        self._run()

    def _run(self):
        """
        Run daemon.
        """
        try:
            self.loop()
        except:
            sys.stderr.write(traceback.format_exc())
        self._on_exit(1)

    def _sigterm_handler(self, signum, frame):
        """
        SIGTERM signal handler.
        """
        self._on_exit(0)

    def _on_exit(self, status):
        """
        Daemon common termination routine.
        """
        try:
            self.terminate()
        except:
            sys.stderr.write(traceback.format_exc())
        sys.stdin.close()
        sys.stdout.close()
        sys.stderr.close()
        if os.path.exists(self.pidfile):
            os.remove(self.pidfile)
        sys.exit(status)

    def loop(self):
        """
        Worker method.

        It will be called after the process has been daemonized.
        You must override this method and provide that it never returns.
        """
        while True:
            time.sleep(1)

    def terminate(self):
        """
        Clean-up method.

        It will be called at the termination of the daemon process. You can
        optionally override this method if your daemon requires to clean-up or
        release resources before quiting.
        """
        pass


class DaemonCtrl(object):
    """
    Control class for a daemon.

    Usage:
    >>> dc = DaemonCtrl(GenericDaemon, config)
    >>> dc.start()

    This class allows to stop or start (spawn) a daemon class.
    """
    def __init__(self, daemoncls, config):
        """
        Constructor.

        @param daemoncls: daemon class (not instance)
        @param pidfile: daemon pid file
        @param workdir: daemon working directory
        """
        self.daemoncls = daemoncls
        self.config = config
        self.pidfile = config['pidfile']

    def start(self):
        """
        Start the daemon.
        """
        # Check for pidfile to see if the daemon already runs
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        # Check if pid is still valid by querying /proc/{pid}/status on Linux
        if pid and sys.platform.startswith('linux'):
            proc_status = '/proc/{}/status'.format(pid)
            if not os.path.exists(proc_status):
                os.remove(self.pidfile)
                pid = None
                message = 'Removing dead pid file {}\n'
                sys.stderr.write(message.format(self.pidfile))

        if pid:
            message = 'pid file {0} already exist. Daemon already running.\n'
            sys.stderr.write(message.format(self.pidfile))
            sys.exit(1)

        sys.stdout.write('Starting daemon... ')
        sys.stdout.flush()

        # Start the daemon
        d = self.daemoncls(self.config)
        d.daemonize()

    def stop(self):
        """
        Stop the daemon.
        """

        # Get the pid from the pidfile
        try:
            with open(self.pidfile,'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:
            message = 'pid file {0} does not exist. Daemon not running.\n'
            sys.stderr.write(message.format(self.pidfile))
            return # Not an error in a restart
        else:
            print('Stopping daemon... [{}]'.format(pid))

        # Try killing the daemon process
        try:
            while True:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            if err.errno == 3: # No such process
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                sys.stderr.write(str(err.args) + '\n')
                sys.exit(1)

    def restart(self):
        """
        Restart the daemon.
        """
        self.stop()
        self.start()

    def foreground(self):
        """
        Run the user loop on the foreground.

        Use this to test the daemon on a headed environment.
        """
        print('Running daemon...')
        d = self.daemoncls(self.config)
        d._run()
