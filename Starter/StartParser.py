import subprocess
from subprocess import PIPE,CalledProcessError,Popen
from Logger import Logger

logger = Logger()

"""
Methods to start a subprocess with the matching parser.
"""
def startCCN(path):
    command = path+"/build/bin/ccn-lite-relay -v99 -u 9000"
    try:
        df = subprocess.check_call(command, stdout=PIPE,shell=True)
        output, err = df.communicate()
    except CalledProcessError as e:
        logger.error("Couldn't start CCN with path: " + path)
        logger.debug(e)

def startPiCN(path):
    command = path +"/starter/picn-relay --format ndntlv -l debug --port 9000"
    try:
        df = subprocess.check_call(command, stdout=PIPE,shell=True)
        output, err = df.communicate()
    except CalledProcessError as e:
        logger.error("Couldn't start picn with path: " + path)
        logger.debug(e)


def startPyCN(path):
    #TODO implement the starting command for
    command = path + ""
    try:
        df = subprocess.check_call(command, stdout=PIPE,shell=True)
        output, err = df.communicate()
    except CalledProcessError as e:
        logger.error("Couldn't start PyCN with path: " + path)
        logger.debug(e)