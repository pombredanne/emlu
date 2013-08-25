import json

config = {
        'timeout'      : 30,
        'pid'          : '/var/run/ecryptfs-mlu.pid',
        'log'          : '/var/log/ecryptfs-mlu.log',
        'samba-check'  : True,
        'force-options': ['user', 'noauto'],
        'mounts'       : [
                {
                    'name'   : 'user1',
                    'mp'  : '/media/mount1',
                    'hidden': False,
                }
            ],
    }

print json.dumps(config, indent=4)
