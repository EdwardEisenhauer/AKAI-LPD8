import requests

class Lights:
	def __init__(self, ip):
		self.ip = ip
		self.red = 0
		self.green = 0
		self.blue = 0

	def set(self, red, green, blue):
		if red in range(0,256) and green in range(0,256) and blue in range(0,256):
			self.red = red
			self.green = green
			self.blue = blue
			message = format(self.red, '02x') + format(self.green, '02x') + format(self.blue, '02x') + '00'
			requests.get('http://' + self.ip + '/s/' + message)
			print("Sending: " + message)


	