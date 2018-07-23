import logging
import time


class Logger(logging.Logger):
    "Fuzzing Logger"

    def __init__(self):
        super().__init__(__name__, logging.DEBUG)
        self.setLevel(logging.DEBUG)
        formatting = logging.Formatter('%(asctime)s - Packet Fuzzing \t %(message)s')
        consolehandler = logging.StreamHandler()
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filehandler = logging.FileHandler(filename="Logfiles/" + timestr + ".log")
        consolehandler.setFormatter(formatting)
        filehandler.setFormatter(formatting)
        consolehandler.setLevel(logging.INFO)
        filehandler.setLevel(logging.DEBUG)
        self.addHandler(consolehandler)
        self.addHandler(filehandler)
