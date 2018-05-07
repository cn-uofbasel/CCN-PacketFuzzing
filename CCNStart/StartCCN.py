import subprocess
from subprocess import PIPE,CalledProcessError,Popen
def startCCN(path):
    command = path+"/build/bin/ccn-lite-relay -v90 -u 9000"
    try:
        df = subprocess.check_call(command, stdout=PIPE,shell=True)
        output, err = df.communicate()
    except CalledProcessError as e:
        print("error")
        print(e)
