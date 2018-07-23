import logging
import time
import pathlib


def getLogger():
    logger = logging.getLogger("Packet Fuzzing")
    if len(logger.handlers) != 0:
        return logger
    logger.propagate = False
    pathlib.Path('Logfiles').mkdir(parents=True, exist_ok=True)
    fileformatting = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s,%(lineno)d:\t%(message)s',
                                       datefmt='%b %d %Y %H:%M:%S')
    consoleformatting = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    consolehandler = logging.StreamHandler()

    timestr = time.strftime("%Y%m%d-%H%M%S")
    filehandler = logging.FileHandler(filename="Logfiles/" + timestr + ".log")

    consolehandler.setFormatter(consoleformatting)
    filehandler.setFormatter(fileformatting)

    consolehandler.setLevel(logging.INFO)
    filehandler.setLevel(logging.DEBUG)

    # logger.setLevel(logging.DEBUG)
    logger.addHandler(consolehandler)
    logger.addHandler(filehandler)
    return logger
