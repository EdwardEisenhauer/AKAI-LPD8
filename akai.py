import mido


class Akai:
    """
    AKAI-LPD8 representation.
    """
    def __init__(self):
        """
        TODO:
         - Do something with this choose input shit
         - Introduce a good (self describing!) AKAI model
         - Introduce an extrapolating method
        """
        input_list = mido.get_input_names()
        for input_name in enumerate(input_list):
            print(input_name)
        input_name = input_list[int(input("Choose input: "))]

        self.port = input_name

        self.knobs = [0, 0, 0]

    def listen(self, verbose=False):
        """
        Listen for the MIDI messages and set the knobs values.

        TODO:
         - Try different mido functions (pool etc.)

        :param verbose: If True prints the content of the MIDI message.
        :return:
        """
        with mido.open_input(self.port) as inport:
            for msg in inport:
                if verbose: print(msg)
                if msg.type == 'control_change':
                    if msg.control in range(1, 4):
                        self.knobs[msg.control-1] = msg.value

    def set_knobs(self, red, green, blue):
        self.knobs = [red, green, blue]

    def get_knobs(self):
        return self.knobs
