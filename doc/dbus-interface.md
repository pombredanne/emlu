emlu daemon D-Bus interface
============================

The emlu daemon expose the following interface on the D-Bus System bus:

Object     : 'org.emlu'
Object path: 'org/emlu/Daemon'
Interface  : 'org.emlu.Daemon'

- GetMounts():
    Purpose    : Get a list of all the well configured and visible mount points.
    Parameters : None.
    Return     : String (JSON).
        [{
            'name'       : 'user1',
            'mp'         : '/media/share/user1',
            'mounted'    : True
         },
         ...
        ]

- Mount(mp, pwd, timeout):
    Purpose    : Mount a configured mount point using given password.
    Parameters :
        - mp     : String
              Mount point to mount (e.g. '/media/mymount1')
        - pwd    : String
              Password to use to mount the ecryptfs mount point.
        - timeout: Integer
              0 to disable auto-umount,
              < 0 to use default timeout (as in config file),
              > 0 timeout in minutes.
    Return     : Integer
        0 success.
       -1 unkown mount point.
       -2 already mounted.
       -3 target mount point doesn't exists.
       -4 mount error (wrong password?).

- Umount(mp):
    Purpose    : Umount a mount point.
    Parameters :
        - mp : String
              Mount point to mount (e.g. '/media/mymount1')
    Return     : Integer
        0 success.
       -1 unkown mount point.
       -2 not mounted.
       -3 umount error.

