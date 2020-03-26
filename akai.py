import mido

class Error(Exception):
    pass

class NoDeviceFound(Error):
    """Raised when there is no MIDI device found"""

def kalbak(msg):
    print("DUPA")

class Akai:
    """
    AKAI-LPD8 representation.

    This class should handle:
        - [ ] PC <-> Interface connection
        - [x] Errors regarding lack of Interface being connected to the PC
          - [ ] During the runtime.
        - [x] Listeting to the MIDI port and storing the knob values in the memory.
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
        self.pads  = [False] * 8

        self.waiter = True      # Do something abou this (jak to się w ogóle nie wypierdala?)

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
                print(msg)
                self.waiter = False
                if verbose: print(msg)
                if msg.type == 'control_change':
                    if msg.control in range(1, 8):
                        self.knobs[msg.control-1] = msg.value
                elif msg.type == 'note_on':
                    if msg.note in range(1,8):
                        self.pads[msg.note-1] = True
                elif msg.type == 'note_off':
                    if msg.note in range(1,8):
                        self.pads[msg.note-1] = False

    def get_knobs(self):
        return self.knobs

    def print_state(self):
        print(self.knobs)
        print(self.pads)
