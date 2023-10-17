"""
Author: Davide Buoso
Description: Record Audio with the integrated/USB Microphone.
"""

import sounddevice as sd
from scipy.io.wavfile import write
from time import time
from os.path import getsize

import argparse as ap

# ARGUMENT PARSER
parser = ap.ArgumentParser()
parser.add_argument('--device', type=int, default=0)
parser.add_argument('--channels', type=int, default=1)
parser.add_argument('--dtype', type=str, default='int32')
parser.add_argument('--sr', type=int, default=48000)


args = parser.parse_args()

STORE_AUDIO = True

def callback(indata, frames, callback_time, status):
    global STORE_AUDIO
    timestamp = time()
    if STORE_AUDIO:
        filename = f'data/{timestamp}.wav'
        write(filename, args.sr, indata)
        # SIZE = 4 (bytes) * SAMPLE_RATE * DURATION / 1024 to get KB, not exactly equal due to metadata (header)
        print(f"Size: {getsize(filename)/1024}")
    
with sd.InputStream(device=args.device, 
                    channels=args.channels, 
                    dtype=args.dtype, 
                    samplerate=args.sr, 
                    callback=callback,
                    blocksize=args.sr):
    """
    channels: audio channels, we select 1 for sake of simplicity
    dtype: resolution (32bits in this case)
    samplerate: number of samples collected every second
    callback: callback function
    blocksize: how frequent execute blocksize (in number of samples), using samplerate we execute it every second.
    To improve audio quality we need higher resolution and higher samplerate but this implies higher
    storage needed. Decreasing audio quality we need less space. It's a tradeoff.
    """
    while True:
        # Starting the recording
        key = input()

        # Logic to stop the recording (using timestamp as file name)
        if key in ('q', 'Q'):
            print("Stopping recording...")
            break

        # We then store the recording on disk through callback and blocksize (automated)

        # Logic for record
        if key in ('p', 'P'):
            STORE_AUDIO = not STORE_AUDIO
            print(f"Registration {'stopped' if STORE_AUDIO else 'started'}.")


        
            
            
        


