import lights
import mido

ip = '192.168.1.101'

red, green, blue = 0, 0, 0

input_list = mido.get_input_names()

for input_name in enumerate(input_list):
	print(input_name)

input_name = input_list[int(input("Choose input: "))]

with mido.open_input(input_name) as inport:
	for msg in inport:
		print(msg.control)
		if msg.control == 1:
			red = msg.value*2
		elif msg.control == 2:
			green = msg.value*2
		elif msg.control == 3:
			blue = msg.value*2 
		print(red)
		print(green)
		print(blue)
		lights.set(ip, red, green, blue)