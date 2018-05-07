import subprocess
from subprocess import PIPE,CalledProcessError,Popen
class StartCCN:
    def __init__(self,path):
        command = path+"/build/bin/ccn-lite-relay -v90 -u 9000"
        try:
            df = subprocess.check_call(command, stdout=PIPE,shell=True)
            output, err = df.communicate()
        except CalledProcessError as e:
            print("error")
            print(e)

if __name__=="__main__":
    start = StartCCN()
