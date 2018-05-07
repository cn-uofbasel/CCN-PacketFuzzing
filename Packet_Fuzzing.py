import argparse
import os
import time
from Connection.Sender import Sender
import socket
from Generation import PacketMaker
from Generation import Encode
import random

if __name__ == '__main__':
    ccn = ['ccn', 'ccn-lite']
    pycn = ['py-cn', 'PyCN-lite']
    parser = argparse.ArgumentParser(description='Packet fuzzer')
    parser.add_argument('parser', choices=ccn + pycn, default='ccn', help="the parser which should be tested")
    parser.add_argument('path', help="path to the parser on this machine")
    args = parser.parse_args()

    # TODO start parser
    if args.parser in ccn:
        print("ccn invoked")
        print("with path ", args.path)
    elif args.parser in pycn:
        print("pycn invoked")
        print("with path ", args.path)

    time.sleep(5)

    # TODO Check if port 9000 is also used on PyCN-lite
    sender = Sender(socket.gethostbyname(socket.gethostname()), 9000)
    history = []

    # TODO Check if parser is still running
    while (True):
        # loop
        package = PacketMaker.makePackage[random.choice(list(PacketMaker.Packages))]
        bytes = Encode.encodePackage(package)
        history.append((package, bytes.hex()))
        time.sleep(1)
        print(history)
