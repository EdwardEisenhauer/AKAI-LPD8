import mido

class Akai:
	def __init__(self):

		input_list = mido.get_input_names()
		for input_name in enumerate(input_list):
			print(input_name)
		input_name = input_list[int(input("Choose input: "))]	
		
		self.port = input_name

		self.knobs = [0, 0, 0]

	def listen(self):
		with mido.open_input(self.port) as inport:
			for msg in inport:
				if msg.control in range(1,4):
					self.knobs[msg.control-1] = msg.value
					print("self.knobs[" + str(msg.control-1) + "] == " + str(msg.value))
					print(self.knobs)

	def set_knobs(self, red, green, blue):
		self.knobs = [red, green, blue]

	def get_knobs(self):
		return self.knobs