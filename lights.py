import requests


class Lights:
    """
    Control and monitor BleBox LightBox.

    TODO:
     - Introduce a Boom function.
     - Introduce a Boom-Boom meter function.
    """
    def __init__(self, ip):
        """
        :param ip: LightBox's IP.
        """
        self.ip = ip
        r = requests.get('http://' + self.ip + '/api/rgbw/state')
        current = r.json()['rgbw']['currentColor']
        print(current)
        self.red = int(current[0:2], 16)
        self.green = 0
        self.blue = 0

    def set(self, red, green, blue):
        """
        Send the http GET with RGB values.

        :param red:
        :param green:
        :param blue:
        :return:
        """
        if red in range(0, 256) and green in range(0, 256) and blue in range(0, 256):
            self.red = red
            self.green = green
            self.blue = blue
            message = format(self.red, '02x') + format(self.green, '02x') + format(self.blue, '02x') + '00'
            requests.get('http://' + self.ip + '/s/' + message)
            print("Sending: " + message)
