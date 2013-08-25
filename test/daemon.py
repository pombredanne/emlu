
import sys
sys.path.insert(0, '../src/lib')

import os
from time import sleep
from ecryptfs_mlu.daemon import GenericDaemon, DaemonCtrl

class TestDaemon(GenericDaemon):

    def __init__(self, config):
        super(TestDaemon, self).__init__(config=config)

    def loop(self):
        counter = 0
        while True:
            print('TestDaemon loop() #{}'.format(counter))
            counter += 1;
            sleep(10)

    def terminate(self):
        print('Terminating daemon...')



if __name__ == '__main__':

    usage = 'Usage: {} [start|stop|restart|foreground]'.format(sys.argv[0])
    if len(sys.argv) < 2:
        sys.stderr.write(usage + '\n')
        sys.exit(1)

    config = {
            'pidfile'  : '/var/run/daemon.py.pid',
            'workdir'  : '/',
            'stdin'    : os.devnull,
            'stdout'   : '/var/log/daemon.py.log',
            'stderr'   : '/var/log/daemon.py.log',
        }
    dc = DaemonCtrl(TestDaemon, config)

    param = sys.argv[1]
    if param == 'start':
        dc.start()
    elif param == 'stop':
        dc.stop()
    elif param == 'restart':
        dc.restart()
    elif param == 'foreground':
        dc.foreground()
    else:
        sys.stderr.write('Unknown param "{}".'.format(param) + '\n')
        sys.exit(2)

