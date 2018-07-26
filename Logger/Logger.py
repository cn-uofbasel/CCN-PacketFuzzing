import logging

class Logger(logging.Logger):
    """
    Fuzzing Logger
    Simple Singelton Logger for file and stdout logging.
    """

    def __init__(self):
        super().__init__("Packet Fuzzing", logging.DEBUG)
        self.setLevel(logging.DEBUG)
        formatting = logging.Formatter('%(asctime)s - Packet Fuzzing \t %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatting)
        self.addHandler(handler)