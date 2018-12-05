import asyncio
import threading
import json
import sys
from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_1
from predictor import Predictor
from expert_system import ExpertSystem


class MQTTAgent(threading.Thread):
    def __init__(self, broker_uri):
        super(MQTTAgent, self).__init__(name='Server MQTT client')
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.client = MQTTClient()
        self.broker_uri = broker_uri
        self.system_info = dict()
        self.predictor = Predictor()
        self.expert_system = ExpertSystem(n_count=3, n_normal=25)
        print('MQTT thread ready.')

    def data_analysis(self, rcvd_data):
        idn = list(rcvd_data.keys())[0]  # From received data, we get the ID
        vals = list(rcvd_data.values())[0]  # From received data, we get the data
        prediction = self.predictor.predict(vals)  # From data, we obtain a prediction
        evaluation = self.expert_system.evaluate(idn, vals, prediction)  # Finally, the RBS makes a decision
        return evaluation

    def get_data(self):
        return self.system_info

    async def ready(self):
        await self.client.connect(self.broker_uri)
        await self.client.subscribe([('windturbine/data', QOS_1)])

    async def listen(self):
        message = await self.client.deliver_message()
        rcvd_data = json.loads(message.publish_packet.payload.data.decode())
        self.system_info.update(rcvd_data)
        status = self.data_analysis(rcvd_data)
        if status is not None:
            await self.publish(list(rcvd_data.keys())[0], status)

    async def publish(self, id, status):
        await self.client.publish('windturbine/action/{0}'.format(id), status.encode(), qos=QOS_1)

    async def system_loop(self):
        await asyncio.sleep(1)
        await self.ready()
        while True:
            await self.listen()
            print(self.system_info)

    def run(self):
        self.loop.run_until_complete(self.system_loop())


if __name__ == '__main__':
    assert len(sys.argv) >= 2, "Must supply only 1 arguments.\n" + "Usage: mqtt_agent.py port"
    scriptname, port, *arguments = sys.argv
    mqtt_agent = MQTTAgent('mqtt://localhost:{0}'.format(port))
    mqtt_agent.start()
