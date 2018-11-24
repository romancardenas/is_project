
# coding: utf-8

# In[106]:


import asyncio
import threading
import json
import sys
from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_1
import sys
sys.path.append("../../faulty_turbine")
import faulty_turbine
import pandas as pd


class WindTurbine(threading.Thread):
    def __init__(self, broker_uri, id, data):
        super(WindTurbine, self).__init__(name='Wind turbine {0}'.format(id))
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.client = MQTTClient()
        self.broker_uri = broker_uri
        self.id = id
        self.status = 'active'
        self.data = data.copy()
        self.data['state'] = pd.Series('w', index=data.index)
        self.pointer = 0
        faulty = self.data.copy()
        self.faulty = faulty_turbine.fu_data(faulty)
        print('Wind turbine {0} thread ready'.format(id))

    def get_data(self):
        data = self.faulty.values[self.pointer, :]
        self.pointer += 1
        if data[5]=='w':
            self.status='active'
        data0={'status': self.status,
               'time':data[0],
              'output_power':data[1],
              'wind_speed':data[2],
              'temperature':data[3],
              'pressure':data[4]}
        
        return data0
    
    def process_message(self, msg):
        if (msg == 'stop' & self.status=='active'):
            realStatus = self.data.values[self.pointer-1,'status']
            if realStatus == 'w':
                print('Server commited an error, as there was no fault! But I am a good slave, so I stop...')
                self.status='stop'
                faulty_turbine.server_error(self.faulty, self.data, self.pointer)
                
            elif realStatus == 'r':
                print('Server is such a smart guy')
                self.status='stop'
                
            else:
                faulty_turbine.fault_detected(self.faulty, self.data, self.pointer)
                self.status='stop'

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
            self.process_message(msg)

    async def publish(self):
        msg = json.dumps({self.id: self.get_data()})
        print('Publishing message: {0}'.format(msg))
        await self.client.publish('windturbine/data', msg.encode(), qos=QOS_1)

    async def system_loop(self):
        await asyncio.sleep(1)
        await self.ready()
        while self.pointer<self.faulty.shape[0]:
            await self.publish()
            await self.listen()
            await asyncio.sleep(0.5)

    def run(self):
        self.loop.run_until_complete(self.system_loop())


if __name__ == '__main__':
    
    df = pd.read_csv('../../../data/data_simulation.csv')
    wind_turbine = WindTurbine('mqtt://localhost:{0}'.format(port), id, df)

