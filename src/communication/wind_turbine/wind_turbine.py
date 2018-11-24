import asyncio
import threading
import json
import sys
from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_1


class WindTurbine(threading.Thread):
    def __init__(self, broker_uri, id, data):
        super(WindTurbine, self).__init__(name='Wind turbine {0}'.format(id))
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.client = MQTTClient()
        self.broker_uri = broker_uri
        self.id = id
        self.status = 'active'
        self.data = {'status': self.status,
                     'time': '2010-01-01 00:00:00+01:00',
                     'output_power': 2350610.791859267,
                     'wind_speed': 5.326969999999998,
                     'temperature': 267.6,
                     'pressure': 98405.7}
        print('Wind turbine {0} thread ready'.format(id))

    def get_data(self):
        self.data['output_power'] += 100000

    async def ready(self):
        await self.client.connect(self.broker_uri)
        await self.client.subscribe([('windturbine/action/{0}'.format(self.id), QOS_1)])

    async def listen(self):
        message = None
        try:
            message = await self.client.deliver_message(timeout=10)
        except:
            pass
        if message is not None:
            msg = message.publish_packet.payload.data.decode()
            print('message received: {0}'.format(msg))
            self.status = msg
            self.data['status'] = msg
            await asyncio.sleep(10)

    async def publish(self):
        msg = json.dumps({self.id: self.data})
        print('Publishing message: {0}'.format(msg))
        await self.client.publish('windturbine/data', msg.encode(), qos=QOS_1)

    async def system_loop(self):
        await asyncio.sleep(1)
        await self.ready()
        while True:
            self.get_data()
            await self.publish()
            await self.listen()

    def run(self):
        self.loop.run_until_complete(self.system_loop())


if __name__ == '__main__':
    assert len(sys.argv) >= 3, "Must supply only 2 arguments.\n" + "Usage: wind_turbine.py id port"
    scriptname, id, port, *arguments = sys.argv
    wind_turbine = WindTurbine('mqtt://localhost:{0}'.format(port), id, None)
    wind_turbine.start()
