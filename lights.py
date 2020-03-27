import json
import requests
import sys

from enums import EffectID


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
        self.api_endpoint_get  = "http://" + self.ip + "/api/rgbw/state"
        self.api_endpoint_post = "http://" + self.ip + "/api/rgbw/set"
        try:
            r = requests.get(self.api_endpoint_get).json()
        except OSError as e:    # OSError will be raised if IP won't be correct
                                # TODO: There should be a better way to do this
            print("Something went wrong with the GET request:\n", e)
            sys.exit()  # Terminate the program
        else:
            print("Connected to IP: " + self.ip)

            self.get_state()
            self.print_state()

    def set_colors(self, red, green, blue):
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
            # print("Sending: " + message)

    def set_white(self, white):
        """
        Send the http GET to adust all RGB diodes brightness.

        :param white: Intensity of RGB diodes.
        :return:
        """
        if white in range(0, 256):
            self.set(white, white, white)

    def set_effect(self):
        message =   json.dumps(
                    {"rgbw":
                        {"effectID": self.effect_id}
                    }, separators=(',',':'))
        requests.post(self.api_endpoint_post, message)  # Maybe some error handling later?

    def set_durations(self):
        message =   json.dumps(
                    {"rgbw": 
                        { "durationsMs": {
                            "colorFade" : self.color_fade,
                            "effectFade": self.effect_fade,
                            "effectStep": self.effect_step
                            }
                        }
                    }, separators=(',',':'))
        requests.post(self.api_endpoint_post, message)

    def set_bpm(self, bpm):
        """Set bpm for a current effect"""
        pass

    def get_state(self):
        r = requests.get(self.api_endpoint_get).json()
        current = r['rgbw']['currentColor']
        self.red = int(current[0:2], 16)
        self.green = int(current[2:4], 16)
        self.blue = int(current[4:6], 16)

        self.color_fade     = r['rgbw']['durationsMs']['colorFade']
        self.effect_fade    = r['rgbw']['durationsMs']['effectFade']
        self.effect_step    = r['rgbw']['durationsMs']['effectStep']

        self.effect_id      = r['rgbw']['effectID']
        self.color_mode     = r['rgbw']['colorMode']

    def print_state(self):
        print("Current LightBox setting:")
        print("Red:           " + str(self.red))
        print("Green:         " + str(self.green))
        print("Blue:          " + str(self.blue))
        print("Color Fade:    " + str(self.color_fade))
        print("Effect Fade:   " + str(self.effect_fade))
        print("Effect Step:   " + str(self.effect_step))
        print("Effect ID:     " + str(self.effect_id) + " " + EffectID(self.effect_id).name)
        print("Color Mode:    " + str(self.color_mode))

