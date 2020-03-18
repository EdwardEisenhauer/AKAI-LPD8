import requests
import sys


class Lights:
    """
    Control and monitor BleBox LightBox.

    TODO:
     - Introduce a Boom function.
     - Introduce a Boom-Boom meter function.
    """
    def __init__(self, ip):
        """
        Create a Lights object.

        TODO:
         - Check if IP is reachable.

        :param ip: LightBox's IP.
        """
        self.ip = ip
        try:
            r = requests.get('http://' + self.ip + '/api/rgbw/state')
        except OSError as e:    # OSError will be raised if IP won't be correct
                                # TODO: There should be a better way to do this
            print("Something went wrong with the GET request:\n", e)
            sys.exit()  # Terminate the program
        else:
            print("Connected to IP: " + self.ip)
            current = r.json()['rgbw']['currentColor']
            print("Current colours settings: " + current)
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
