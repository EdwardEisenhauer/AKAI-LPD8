from threading import Thread
from queue import Queue
from time import sleep
from blebox import LightBox
from akai import Akai
import sys

ip = sys.argv[1]

pasek = LightBox(ip)

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

def knob_to_ms(value):
    knob_min = 0
    knob_max = 127
    ms_min   = 0
    ms_max   = 1000

    return int(value/(knob_max-knob_min)*(ms_max-ms_min))

def knob_to_effect(value):
    knob_min = 0
    knob_max = 127
    effect_id_min = 0
    effect_id_max = 6

    return int(value/(knob_max-knob_min)*(effect_id_max-effect_id_min))


def producer(output_queue):
    [r, g, b, w] = [i * 2 for i in akai.knobs][:4]
    w_prev = w
    while True:
        # Oh my ficking god do something about this!!!
        if akai.knobs_color_change:
            [r, g, b, w] = [i * 2 for i in akai.knobs][:4] # Get RGB values from the AKAI
            if w == w_prev:
                output_queue.put([r, g, b])
            else:
                output_queue.put([w, w, w])
                w_prev = w
            akai.knobs_color_change = False
        elif akai.knobs_durations_change:
            [color_fade, effect_fade, effect_step] = map(knob_to_ms, akai.knobs[4:7])
            effect_id = knob_to_effect(akai.knobs[7])
            pasek.color_fade     = color_fade
            pasek.effect_fade    = effect_fade
            pasek.effect_step    = effect_step
            pasek.set_durations() # It shouldn't be like this XD
            pasek.effect_id      = effect_id
            pasek.set_effect()     # Jak to się nie zesra to będzie cud XD
            akai.knobs_durations_change = False
            pasek.print_state()
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
