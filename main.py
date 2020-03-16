from threading import Thread
import time
from lights import Lights
from akai import Akai

ip = '192.168.1.101'

pasek = Lights(ip)

akai = Akai()

def behaviour():
	# TODO: Detect incoming MIDI data at the mido level?
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
	
