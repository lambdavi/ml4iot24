"""
Author: Davide Buoso
Description: Explore retention in Redis.
"""
import redis
from time import time, sleep

REDIS_HOST = 'redis-12775.c3.eu-west-1-2.ec2.cloud.redislabs.com'
REDIS_PORT = 12775
REDIS_USERNAME = 'default'

with open("psw.txt") as f:
        REDIS_PSW = f.readlines()[0]

redis_client = redis.Redis(host=REDIS_HOST, 
                           port=REDIS_PORT, 
                           username=REDIS_USERNAME, 
                           password=REDIS_PSW)

is_connected = redis_client.ping()
print(is_connected)

# RETENTION
one_day_in_ms = 24 * 3600 * 1000
#redis_client.ts().alter('temperature', retention_msecs=one_day_in_ms) # Retention will delete data after 1 day of data

# AGGREGATION
try:
    redis_client.ts().create('temperature_avg', chunk_size=128) # We have to create a new timeseries to keep aggregated results. It is recome
    redis_client.ts().createrule('temperature', 'temperature_avg', 'avg', bucket_size_msec=1000)
except:
    pass


info = redis_client.ts().info('temperature')
print("Memory Usage (bytes): ", info.memory_usage) # Just created the memory is chunck_size + something for setup
print("Total Samples: ", info.total_samples)
print("Number of Chunks: ", info.chunk_count) # Thanks to compression the size to store data is lower than the behaviour expected

info = redis_client.ts().info('temperature_avg')
print("Memory Usage (bytes): ", info.memory_usage) # Just created the memory is chunck_size + something for setup
print("Total Samples: ", info.total_samples)
print("Number of Chunks: ", info.chunk_count) # Thanks to compression the size to store data is lower than the behaviour expected

print("Adding to temperature.. ")
for i in range(100):
    timestamp_ms = int(time()*1000)
    redis_client.ts().add('temperature', timestamp_ms, 25+i//50)
    sleep(0.1)
print("End. ")

info = redis_client.ts().info('temperature')
print("Memory Usage (bytes): ", info.memory_usage) 
print("Total Samples: ", info.total_samples)
print("Number of Chunks: ", info.chunk_count) 

info = redis_client.ts().info('temperature_avg')
print("Memory Usage (bytes): ", info.memory_usage) 
print("Total Samples: ", info.total_samples)
print("Number of Chunks: ", info.chunk_count)