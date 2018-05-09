import subprocess
from subprocess import PIPE,CalledProcessError,Popen

"""
Methods to start a subprocess with the matching parser.
"""
def startCCN(path):
    command = path+"/build/bin/ccn-lite-relay -v99 -u 9000"
    try:
        df = subprocess.check_call(command, stdout=PIPE,shell=True)
        output, err = df.communicate()
    except CalledProcessError as e:
        print("Error:\n")
        print(e)

def startPiCN(path):
    command = path +"/starter/picn-relay --format ndntlv -l debug --port 9000"
    try:
        df = subprocess.check_call(command, stdout=PIPE,shell=True)
        output, err = df.communicate()
    except CalledProcessError as e:
        print("Error!:\n")
        print(e)

def startPyCN(path):
    #TODO implement the starting command for
    command = path + ""
    try:
        df = subprocess.check_call(command, stdout=PIPE,shell=True)
        output, err = df.communicate()
    except CalledProcessError as e:
        print("Error:\n")
        print(e)