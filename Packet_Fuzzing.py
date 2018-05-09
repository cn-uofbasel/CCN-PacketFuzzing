import argparse
import time
from Connection.Sender import Sender
from Generation import PacketMaker
from Generation import Encode
import random
import os
import sys
import thread
from CCNStart import StartCCN as start
fuzziness = 1

if __name__ == '__main__':
    ccn = ['ccn', 'ccn-lite']
    pycn = ['py-cn', 'PyCN-lite']
    parser = argparse.ArgumentParser(description='Packet fuzzer')
    parser.add_argument('parser', choices=ccn + pycn, default='ccn', help="the parser which should be tested")
    parser.add_argument('path', help="path to the parser on this machine")
    args = parser.parse_args()

    if (not os.path.exists(args.path)):
        errstring = "The path "+args.path+" does not exist on this machine"
        sys.exit(errstring)

    # TODO start parser (non-blocking)

    if args.parser in ccn:
        print("ccn invoked")
        print("with path ", args.path)
        thread.start_new_thread(start.startCCN,(args.path,))

    elif args.parser in pycn:
        print("pycn invoked")
        print("with path ", args.path)

    time.sleep(5)

    # TODO Check if port 9000 is also used on PyCN-lite
    sender = Sender("127.0.0.1", 9000)
    history = []

    # TODO Check if parser is still running
    while (True):
        # loop
        package = PacketMaker.makePackage[random.choice(list(PacketMaker.Packages))]
        bytes = Encode.encodePackage(package)
        sender.sendMessage(bytes.tobytes())
        history.append((package, bytes))
        print(package)
        time.sleep(3)
        #print(history)

def getFuzziness():
    return fuzziness
