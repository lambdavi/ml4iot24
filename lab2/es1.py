"""
Author: Davide Buoso
Description: Make experience with chunck size and information retrieval of Redis (compressed version).
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

try:
    redis_client.ts().create('temperature', chunk_size=128) # Default value of chunck_size 4096
except redis.ResponseError:
    pass

info = redis_client.ts().info('temperature')
print("Memory Usage (bytes): ", info.memory_usage) # Just created the memory is chunck_size + something for setup
print("Total Samples: ", info.total_samples)
print("Number of Chunks: ", info.chunk_count) # Thanks to compression the size to store data is lower than the behaviour expected

for i in range(100):
    timestamp_ms = int(time()*1000)
    redis_client.ts().add('temperature', timestamp_ms, 25+i//50)
    sleep(0.1)

# savings = 100 * (uncompressed_memory - compressed_memory) / uncompressed_memory
compressed_memory = redis_client.ts().info('temperature').memory_usage
uncompressed_memory = redis_client.ts().info('temperature_uncom').memory_usage
savings = 100 * (uncompressed_memory - compressed_memory) / uncompressed_memory
print(f'Memory Savings: {savings:.2f}%') # Memory Savings: 60.70%





