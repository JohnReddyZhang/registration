#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
# Set the shebang to whatever your computer runs on.
# There are several points I could not figure out how to print:
# nanoseconds of time stamps, and "-6000" after time stamp, and uid / gid numeric representation.

import pathlib
import sys
import stat
import pwd
import grp
import time


class ShowStats(object):
    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.run_stat(self.path)

    def run_stat(self, path):
        try:
            if not path.exists():
                raise FileNotFoundError
            else:
                mode = self.file_mode_detector(path)

                print(f"File: '{path.name}'")
                print(f"Size: {path.stat().st_size:<11}"
                      f"Blocks: {path.stat().st_blocks:<11}"
                      f"IO Block: {path.stat().st_blksize} ", end=' ')
                print(f'{mode}')
                print(f"Device: {path.stat().st_dev}  "
                      f"Inode: {path.stat().st_ino:<12}"
                      f"Links: {path.stat().st_nlink}")
                print(f"Access: ({oct(path.stat().st_mode)[-4:]}/{stat.filemode(path.stat().st_mode)})  "
                      f"Uid: ({path.stat().st_uid}/{pwd.getpwuid(path.stat().st_uid).pw_name})  "
                      f"Gid: ({path.stat().st_gid}/{grp.getgrgid(path.stat().st_gid).gr_name})")
                print(f"Access: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(path.stat().st_atime))}")
                print(f"Modify: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(path.stat().st_mtime))}")
                print(f"Change: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(path.stat().st_ctime))}")
        except FileNotFoundError:
            print(f"Cannot stat '{path.name}, No such file or dir.")

    @staticmethod
    # Inspired from discussions with Mr. Ziqing Zhang and Mr. Yang Chen,
    # Referenced form https://docs.python.org/3.6/library/stat.html
    def file_mode_detector(path):
        mode = path.stat().st_mode
        if stat.S_ISDIR(mode):
            return 'directory'

        elif stat.S_ISCHR(mode):
            return 'special file'

        elif stat.S_ISBLK(mode):
            return 'block special'

        elif stat.S_ISREG(mode):
            if path.stat().st_size == 0:
                return 'regular empty file'
            else:
                return 'regular file'

        elif stat.S_ISFIFO(mode):
            return 'FIFO/pipe'

        elif stat.S_ISLNK(mode):
            return 'symbolic link'

        elif stat.S_ISSOCK(mode):
            return 'socket'

        elif stat.S_ISDOOR(mode):
            return 'door'

        elif stat.S_ISPORT(mode):
            return 'event port'

        elif stat.S_ISWHT(mode):
            return 'whiteout'


if len(sys.argv) is 1:
    print("stat: missing operand\n"
          "Try stat --help for more info\n"
          "Although help is not implemented in this script")
else:
    p = ShowStats(sys.argv[1])
