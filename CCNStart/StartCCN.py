import os

class StartCCN:
    def __init__(self):
        os.system("start cmd")
        os.chdir("C:\\Users\\timko\\Documents\\Github\\ccn-lite\\src")
        os.system("dir")

if __name__=="__main__":
    start = StartCCN()
