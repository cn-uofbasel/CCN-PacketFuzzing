import logging
import time
import pathlib


def getLogger(consolelevel=logging.INFO, filelevel=logging.DEBUG):
    """
    Fuzzing Logger
    Simple Singelton Logger for file and stdout logging.
    """
    logger = logging.getLogger("Packet Fuzzing")
    if len(logger.handlers) != 0:
        return logger
    logger.propagate = False
    pathlib.Path('Logfiles').mkdir(parents=True, exist_ok=True)
    fileformatting = logging.Formatter('%(asctime)s.%(msecs)03d - %(levelname)s -\t %(filename)s,%(lineno)d:\t%(message)s',
                                       datefmt='%b %d %Y %H:%M:%S')
    consoleformatting = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    consolehandler = logging.StreamHandler()

    timestr = time.strftime("%Y%m%d-%H%M%S")
    filehandler = logging.FileHandler(filename="Logfiles/" + timestr + ".log")

    consolehandler.setFormatter(consoleformatting)
    filehandler.setFormatter(fileformatting)

    consolehandler.setLevel(consolelevel)
    filehandler.setLevel(filelevel)

    # logger.setLevel(logging.DEBUG)
    logger.addHandler(consolehandler)
    logger.addHandler(filehandler)
    return logger
