import requests

def set(ip, red, green, blue):
	if red in range(0,256) and green in range(0,256) and blue in range(0,256):
		message = format(red, '02x') + format(green, '02x') + format(blue, '02x') + '00'
		requests.get('http://' + ip + '/s/' + message)
	