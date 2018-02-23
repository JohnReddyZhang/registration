#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
# Set the shebang to whatever your computer runs on.
# It is different from what I have here.
# Also, be sure to change permission.

import pathlib
import sys
import stat
import pwd
import grp
import time


class DisplayStats(object):
    def __init__(self, path):
        self.path_lst = sorted([pathlib.Path(a_path) for a_path in path], key=lambda item: item.is_dir())
        self.run(self.path_lst)

    def run(self, path):
        try:
            for a_path in path:
                p = pathlib.Path(a_path)
                if not p.exists():
                    raise FileNotFoundError
                else:
                    if p.is_file():
                        # Reference on how to get the permission in rwxrwxrwx style:
                        # https://stackoverflow.com/questions/17809386/how-to-convert-a-stat-output-to-a-unix-permissions-string
                            self.print_stat(p, name=str(p))
                    elif p.is_dir():
                        if self.path_lst.index(a_path) is not 0:
                            print(f'\n{p}')
                        self.print_stat(p, name='.')
                        self.print_stat(p.parent, name='..')
                        for under_p_path in sorted(p.iterdir()):
                            self.print_stat(under_p_path)
        except FileNotFoundError:
            print(f"Cannot access '{p.name}': No such file or directory")

    @staticmethod
    def print_stat(print_path, name=None):
        print(f'{stat.filemode(print_path.stat().st_mode):10}'
              f'{print_path.stat().st_nlink:3} '
              f'{pwd.getpwuid(print_path.stat().st_uid).pw_name}  '
              f'{grp.getgrgid(print_path.stat().st_gid).gr_name}'
              f'{print_path.stat().st_size:5} '
              f'{time.strftime("%b  %d %H:%M",time.localtime(print_path.stat().st_mtime))} '
              f'{print_path.name if not name else name}')


if len(sys.argv) is not 1:
    p = DisplayStats(sys.argv[1:])

else:
    p = DisplayStats(['.'])

