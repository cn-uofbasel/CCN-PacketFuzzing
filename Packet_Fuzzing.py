import argparse
import time
import random
from Connection.Sender import Sender
from Generation import PacketMaker
from Generation import Encode
import os
import sys
import thread
import logging
from Starter import StartParser as start


logging.basicConfig(level=logging.DEBUG)

def getPackage(packageArgs):
    if packageArgs is not None:
        if packageArgs == 'n':
            logging.debug("Selected Type: Name")
            return PacketMaker.makePackage[PacketMaker.Packages.Name]
        elif packageArgs == 'd':
            logging.debug("Selected Type: Data")
            return PacketMaker.makePackage[PacketMaker.Packages.Data]
        elif packageArgs == 'l':
            logging.debug("Selected Type: LinkObject")
            return PacketMaker.makePackage[PacketMaker.Packages.LinkObject]
        elif packageArgs == 'i':
            logging.debug("Selected Type: Interest")
            return PacketMaker.makePackage[PacketMaker.Packages.Interest]
    logging.debug("Selected Type: All")
    return PacketMaker.makePackage[random.choice(list(PacketMaker.Packages))]


if __name__ == '__main__':
    ccn = ['ccn', 'ccn-lite']
    pycn = ['py-cn', 'PyCN-lite']
    picn = ['picn','PiCN']
    parser = argparse.ArgumentParser(description='Packet fuzzer')
    parser.add_argument('parser', choices=ccn + pycn + picn, default='ccn', help="The parser which should be tested")
    parser.add_argument('path', help="Path to the parser on this machine")
    parser.add_argument('-f', '--fuzziness',help='Level of incorrectness',required=False, default=0,type=int,choices=[0,1,2])
    parser.add_argument('-p', '--packages', help='The package type to be sent', required=False, default=0, type=str, choices=['n','d','l','i'])
    args = parser.parse_args()
    Encode.setFuzziness(args.fuzziness)
    if (not os.path.exists(args.path)):
        errstring = "The path "+args.path+" does not exist on this machine"
        sys.exit(errstring)

    # TODO start parser (non-blocking)

    if args.parser in ccn:
        print("CCN invoked")
        print("with path ", args.path)
        thread.start_new_thread(start.startCCN,(args.path,))

    elif args.parser in pycn:
        print("PyCN invoked")
        print("with path ", args.path)
        thread.start_new_thread(start.startPyCN,(args.path,))

    elif args.parser in picn:
        print("PiCN invoked")
        print("with path ", args.path)
        thread.start_new_thread(start.startPiCN,(args.path,))

    time.sleep(5)

    # TODO Check if port 9000 is also used on PyCN-lite
    sender = Sender("127.0.0.1", 9000)
    history = []

    # TODO Check if parser is still running
    while (thread._count() > 0):
        package = getPackage(args.packages)
        bytes = Encode.encodePackage(package)
        sender.sendMessage(bytes.tobytes())
        history.append((package, bytes))
        print(package)
        print("Size: ", bytes.__len__())
        time.sleep(0.1)
        #print(history)