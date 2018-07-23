import argparse
import time
import random
from Logger import Logger
from Connection.Sender import Sender
from Generation import PacketMaker
from Generation import Encode
import os
import sys
import _thread
from Starter import StartParser as start


def getSelectedTypes(packageArgs):
    if packageArgs != 0:
        typeList = []
        outString = "Selected packages: \t"
        if 'n' in packageArgs:
            typeList.append(PacketMaker.Packages.Name)
            outString += "Name\t"
        if 'd' in packageArgs:
            typeList.append(PacketMaker.Packages.Data)
            outString += "Data\t"
        if 'i' in packageArgs:
            typeList.append(PacketMaker.Packages.Interest)
            outString += "Interest\t"
        if 'l' in packageArgs:
            typeList.append(PacketMaker.Packages.LinkObject)
        return (typeList,outString)
    else:
        return (list(PacketMaker.Packages),"Selected packages: \tAll")


if __name__ == '__main__':
    logger = Logger.getLogger()
    logger.debug("starting")
    logger.info("is starting")
    ccn = ['ccn', 'ccn-lite']
    pycn = ['py-cn', 'PyCN-lite']
    picn = ['picn','PiCN']
    parser = argparse.ArgumentParser(description='Packet fuzzer')
    parser.add_argument('parser', choices=ccn + pycn + picn, default='ccn', help="The parser which should be tested")
    parser.add_argument('path', help="Path to the parser on this machine")
    parser.add_argument('-f', '--fuzziness',help='Level of incorrectness',required=False, default=0,type=int,choices=[0,1,2])
    parser.add_argument('-p', '--packages', help='The package type to be sent',nargs='+', required=False, default=0, type=str, choices=['n','d','l','i'])
    args = parser.parse_args()
    Encode.setFuzziness(args.fuzziness)
    if not os.path.exists(args.path):
        errString = "The path "+args.path+" does not exist on this machine"
        sys.exit(errString)

    if args.parser in ccn:
        logger.info("CCN invoked with path %s", args.path)
        _thread.start_new_thread(start.startCCN,(args.path,))

    elif args.parser in pycn:
        logger.info("PyCN invoked with path %s", args.path)
        _thread.start_new_thread(start.startPyCN,(args.path,))

    elif args.parser in picn:
        logger.info("PiCN invoked with path %s", args.path)
        _thread.start_new_thread(start.startPiCN,(args.path,))

    time.sleep(5)

    # TODO Check if port 9000 is also used on PyCN-lite
    sender = Sender("127.0.0.1", 9000)
    history = []

    # TODO Check if parser is still running

    (types,outString) = getSelectedTypes(args.packages)
    logger.debug(outString)

    packCount = 0
    while (_thread._count() > 0):
        # loop
        package = PacketMaker.makePackage[random.choice(list(types))]
        bytes = Encode.encodePackage(package)
        sender.sendMessage(bytes.tobytes())
        history.append((package, bytes))
        logger.debug("Package n° %d \n %s", packCount,package)
        logger.debug("Package %d Size: %d",packCount, bytes.__len__())
        time.sleep(0.1)
        #print(history)
        packCount+=1

