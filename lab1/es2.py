"""
Author: Davide Buoso
Description: : Monitor your PC battery status with Python.
"""
import psutil 
from time import sleep, time
from datetime import datetime
import uuid

import redis

REDIS_HOST = 'redis-12775.c3.eu-west-1-2.ec2.cloud.redislabs.com'
REDIS_PORT = 12775
REDIS_USERNAME = 'default'
REDIS_PSW = 'lphlxTFuLOGpziPIWVIFq1VekXKOEsTM'

redis_client = redis.Redis(host=REDIS_HOST, 
                           port=REDIS_PORT, 
                           username=REDIS_USERNAME, 
                           password=REDIS_PSW)

is_connected = redis_client.ping()
print(is_connected)
 
#redis_client.ts().create('battery_level')
#redis_client.ts().create('power_plugged')

while True:
        info = psutil.sensors_battery()
        battery_level = info.percent
        power_plugged = int(info.power_plugged)
        ts = time()
        formatted_ts = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')
        print(f'{formatted_ts} - {hex(uuid.getnode())}:battery={battery_level}')
        print(f'{formatted_ts} - {hex(uuid.getnode())}:power={power_plugged}')

        redis_client.ts().add('battery_level', int(ts*1000), battery_level)
        redis_client.ts().add('power_plugged', int(ts*1000), power_plugged)

        sleep(2)
