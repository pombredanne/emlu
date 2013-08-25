ecryptfs-mlu D-Bus interface
============================

The ecryptfs-mlu daemon expose the following interface on the D-Bus System bus:

Object: 'org.ecryptfs.mlu'
Object path: 'org/ecryptfs/mlu/MLUDaemon'
Interface  : 'org.ecryptfs.mlu.MLUDaemon'

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

- Mount(mp, pwd):
    Purpose    : Mount a configured mount point using given password.
    Parameters :
        - mp : String
              Mount point to mount (e.g. '/media/mymount1')
        - pwd: String
              Password to use to mount the ecryptfs mount point.
    Return     : Integer
        0 success.
       -1 unkown mount point.
       -2 already mounted.
       -3 target point doesn't exists.
       -4 mount point not defined in fstab.
       -5 wrong options.
       -6 mount error (wrong password?).

- Umount(mp):
    Purpose    : Umount a mount point.
    Parameters :
        - mp : String
              Mount point to mount (e.g. '/media/mymount1')
    Return     : Integer
        0 success.
       -1 unkown mount point.
       -2 not mounted.

