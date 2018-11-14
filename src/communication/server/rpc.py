import sys
import threading
from xmlrpc.server import SimpleXMLRPCServer


class RPCServer(threading.Thread):
    def __init__(self, port, send_function):
        super(RPCServer, self).__init__(name='RPC server thread')
        self.system_info = dict()
        self.server = SimpleXMLRPCServer(('localhost', port), logRequests=True)
        self.server.register_function(self.send_info, send_function)
        print('RPC thread ready.')

    def send_info(self):
        return self.system_info

    def refresh_info(self, new_data):
        self.system_info.update(new_data)

    def run(self):
        self.server.serve_forever()


if __name__ == '__main__':
    assert len(sys.argv) >= 3, "Must supply only 2 arguments.\n" + "Usage: rpc.py port send_function"
    scriptname, port, send_function, *arguments = sys.argv
    rpc_server = RPCServer(int(port), send_function)
    rpc_server.start()
