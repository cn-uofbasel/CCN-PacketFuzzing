import argparse
import os
import time
from Connection.Sender import Sender
import socket
from Generation import PacketMaker
from Generation import Encode
import random
import os
import sys
from CCNStart import StartCCN

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

    # TODO start parser

    if args.parser in ccn:
        print("ccn invoked")
        print("with path ", args.path)
        start = StartCCN.StartCCN(args.path)

    elif args.parser in pycn:
        print("pycn invoked")
        print("with path ", args.path)

    time.sleep(5)

    # TODO Check if port 9000 is also used on PyCN-lite
    #sender = Sender("127.0.0.1", 9000)
    history = []

    # TODO Check if parser is still running
    while (True):
        # loop
        package = PacketMaker.makePackage[random.choice(list(PacketMaker.Packages))]
        bytes = Encode.encodePackage(package)
        sender.sendMessage(bytes)
        history.append((package, bytes.hex()))
        time.sleep(1)
        print(history)
