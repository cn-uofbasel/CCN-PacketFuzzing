import subprocess
from subprocess import PIPE,CalledProcessError,Popen
from Logger import Logger
import pathlib
import time


logger = Logger.getLogger()

"""
Methods to start a subprocess with the matching parser.
"""
def startCCN(path):
    command = path+"/build/bin/ccn-lite-relay -v99 -u 9000"
    try:
        logger = Logger.getLogger()
        pathlib.Path('Logfiles/ccn-lite').mkdir(parents=True, exist_ok=True)
        f = open("Logfiles/ccn-lite/ " + time.strftime("%Y%m%d-%H%M%S") + ".log", mode="w+")
        proc = Popen(command, stderr=f,shell=True)
        return proc
        #logger.debug(output)
    except CalledProcessError as e:
        logger.error("Couldn't start CCN with path: " + path)
        logger.debug(e)
    except subprocess.TimeoutExpired as e:
        logger.debug(e)
    except Exception as e:
        logger.error("Exeption at starting ccn-lite")
        logger.error(e)

def startPiCN(path):
    command = path +"/starter/picn-relay --format ndntlv -l debug --port 9000"
    try:
        logger = Logger.getLogger()
        pathlib.Path('Logfiles/picn').mkdir(parents=True, exist_ok=True)
        f = open("Logfiles/picn/ " + time.strftime("%Y%m%d-%H%M%S") + ".log", mode="w+")
        proc = Popen(command, stderr=f, shell=True)
        return proc
    except CalledProcessError as e:
        logger.error("Couldn't start picn with path: " + path)
        logger.debug(e)
    except Exception as e:
        logger.error("Exeption starting PiCN.")
        logger.error(e)


def startPyCN(path):
    #TODO implement the starting command for
    command = path + "/pycn_lite/bin/srv_fwd.py 127.0.0.1:9000"
    try:
        logger = Logger.getLogger()
        pathlib.Path('Logfiles/pycn').mkdir(parents=True, exist_ok=True)
        f = open("Logfiles/pycn/ " + time.strftime("%Y%m%d-%H%M%S") + ".log", mode="w+")
        proc = Popen(command, stderr=f, shell=True)
        return proc
    except CalledProcessError as e:
        logger.error("Couldn't start PyCN with path: " + path)
        logger.debug(e)