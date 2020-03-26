from threading import Thread
from queue import Queue
from time import sleep
from lights import Lights
from akai import Akai
import sys

ip = sys.argv[1]

pasek = Lights(ip)

akai = Akai()

"""
Read knob values and send the GET to set the Lights.

Monitor the knobs values. If anyone changes send a GET to set the lights. Wait 100ms before next packet.

TODO:
- Detect incoming MIDI data at the mido level?
- Do something about this ugly time.sleep(0.1)
- Introduce an extrapolating method
:return:
"""


def producer(output_queue):
    [r, g, b, w] = [i * 2 for i in akai.knobs][:4]
    w_prev = w
    while True:
        # Oh my ficking god do something about this!!!
        if akai.knobs_change:
            [r, g, b, w] = [i * 2 for i in akai.knobs][:4] # Get RGB values from the AKAI
            if w == w_prev:
                output_queue.put([r, g, b])
            else:
                output_queue.put([w, w, w])
                w_prev = w
            akai.knobs_change = False
        elif akai.pads_change:
            if akai.pads[3]:
                output_queue.put([255, 255, 255])
            else:
                output_queue.put(map(lambda x: 255 if x else 0,akai.pads[:3]))
            akai.pads_change = False
        sleep(0.1)                               # Do something about it!

def consumer(input_queue):
    while True:
        [r, g, b] = input_queue.get()

        pasek.set_colors(r, g, b)

        input_queue.task_done() 


# def print_state():
#     while True:
#         akai.print_state()
#         sleep(3)

if __name__ == '__main__':
    q = Queue()
    Thread(target=producer, args=(q,)).start()
    Thread(target=consumer, args=(q,)).start()
    Thread(target=akai.listen).start()
    # Thread(target=print_state).start()
