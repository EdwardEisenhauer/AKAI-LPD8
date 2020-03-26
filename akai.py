import mido

class Error(Exception):
    pass

class NoDeviceFound(Error):
    """Raised when there is no MIDI device found"""

class Akai:
    """
    AKAI-LPD8 representation.

    This class should handle:
        - [ ] PC <-> Interface connection
        - [x] Errors regarding lack of Interface being connected to the PC
          - [ ] During the runtime.
        - [ ] Listeting to the MIDI port and storing the knob values in the memory.
        - [ ] Informing that the knob value has changed
    """
    def __init__(self):
        """
        TODO:
         - Do something with this choose input shit
         - Introduce a good (self describing!) AKAI model
        """
        self.port_name = ""
        for input_name in mido.get_input_names():
            if 'LPD8' in input_name:
                self.port_name = input_name
                print(self.port_name + ' detected!')
                break
        if not self.port_name:
            raise NoDeviceFound

        self.knobs = [0] * 8

    def listen(self, verbose=False):
        """
        Listen for the MIDI messages and set the knobs values.

        TODO:
         - Try different mido functions (pool etc.)

        :param verbose: If True prints the content of the MIDI message.
        :return:
        """
        print('Listening to the ' + self.port_name)
        with mido.open_input(self.port_name) as inport:
            for msg in inport:
                if verbose: print(msg)
                if msg.type == 'control_change':
                    if msg.control in range(1, 8):
                        self.knobs[msg.control-1] = msg.value

    def get_knobs(self):
        return self.knobs
