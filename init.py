#/usr/local/bin/python3

import sys
import subprocess

if __name__ == '__main__':
    exit_code = subprocess.call(['/usr/local/bin/python3', '/Users/kz/Projects/Evergreen4/event-loop.py'])
    if exit_code is 0:
        sys.exit(0)
    else:
        sys.exit(1)
