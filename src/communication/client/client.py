import sys
import time
from xmlrpc.client import ServerProxy


def request(port, func):
    with ServerProxy('http://{0}:{1}'.format('localhost', port)) as proxy:
        remote_function = getattr(proxy, func)
        return remote_function()


if __name__ == '__main__':
    assert len(sys.argv) >= 3, "Must supply at least 2 arguments.\n" + "Usage: client.py port function [*arguments]"
    scriptname, port, func, *arguments = sys.argv
    while True:
        res = request(port, func)
        print(res)
        time.sleep(10)
