from threading import Thread
import time
from lights import Lights
from akai import Akai

ip = '192.168.1.101'

pasek = Lights(ip)

akai = Akai()


def behaviour():
    """
    Read knob values and send the GET to set the Lights.

    Monitor the knobs values. If anyone changes send a GET to set the lights. Wait 100ms before next packet.

    TODO:
    - Detect incoming MIDI data at the mido level?
    
    :return:
    """

    [red, green, blue] = [0, 0, 0]
    while True:
        [r, g, b] = [i * 2 for i in akai.get_knobs()]
        if [red, green, blue] == [r, g, b]:
            continue
        [red, green, blue] = [r, g, b]
        pasek.set(red, green, blue)
        time.sleep(0.1)


if __name__ == '__main__':
    Thread(target=akai.listen).start()
    Thread(target=behaviour).start()
