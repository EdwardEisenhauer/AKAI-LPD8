from threading import Thread
import time
from lights import Lights
from akai import Akai

ip = '192.168.1.101'

pasek = Lights(ip)

akai = Akai()

def behaviour():
	while True:
		[red, green, blue] = [i * 2 for i in akai.get_knobs()]
		pasek.set(red, green, blue)
		time.sleep(0.1)

if __name__ == '__main__':
	Thread(target=akai.listen).start()
	Thread(target=behaviour).start()
	
