import time
import sys
sys.path.insert(0, '../')
from src.communication.server.mqtt_agent import MQTTAgent
from src.communication.server.rpc import RPCServer


class SystemServer:
    def __init__(self, port_mqtt, port_rpc, send_function, refresh):
        self.rpc_server = RPCServer(port_rpc, send_function)
        self.mqtt_agent = MQTTAgent('mqtt://localhost:{0}'.format(port_mqtt))
        self.refresh = refresh

    def start(self):
        self.rpc_server.start()
        self.mqtt_agent.start()

    def loop(self):
        while True:
            new_data = self.mqtt_agent.get_data()
            self.rpc_server.refresh_info(new_data)
            time.sleep(5)


if __name__ == '__main__':
    assert len(sys.argv) >= 5, "Must supply only 4 arguments.\n" + "Usage: system_server.py port_mqtt port_rpc send_function refresh"
    scriptname, port_mqtt, port_rpc, send_function, refresh, *arguments = sys.argv
    system_server = SystemServer(int(port_mqtt), int(port_rpc), send_function, int(refresh))
    system_server.start()
    system_server.loop()
