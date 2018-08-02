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
import binascii
import subprocess
import signal

"""
Main startpoint to invoke a fuzzer.
reads the args, starts the selected parser and opens connection via UDP to it.
Then random packets are generated and send. All reactions are stored into logfiles.
"""


protocolToList = {
    'NDN': PacketMaker.NDNPackages,
    'CCNx': PacketMaker.CCNxPackages
}


def getSelectedTypes(packageArgs, pakets):
    """
    extracts the selected pakettypes from the args
    :param packageArgs: args field containing the selected packages
    :param pakets: the selected packet format
    :return: tuple of a list containing the enums of the selected packages and a description string for logging
    """
    if packageArgs != 0:
        typeList = []
        outString = "Selected packages: \t"
        if pakets == 'NDN':
            if 'i' in packageArgs:
                typeList.append(PacketMaker.NDNPackages.Interest)
                outString += "Interest\t"
            if 'l' in packageArgs:
                typeList.append(PacketMaker.NDNPackages.LinkObject)
        elif pakets == 'CCNx':
            if 'i' in packageArgs:
                typeList.append(PacketMaker.CCNxPackages.Interest)
                outString += "Interest\t"
            if 'c' in packageArgs:
                typeList.append(PacketMaker.CCNxPackages.ContentOject)
                outString += "ContentObject\t"
        return typeList, outString
    else:
        return (protocolToList[pakets], "Selected packages: \tAll")


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


def check_proc_alive(proc):
    if proc is not None:
        return proc.poll() is None
    else:
        return False

if __name__ == '__main__':
    logger = Logger.getLogger()
    logger.debug("starting")
    logger.info("is starting")
    # setup argsparser
    ccn = ['ccn', 'ccn-lite']
    pycn = ['py-cn', 'PyCN-lite']
    picn = ['picn','PiCN']
    none = ['offline']
    parser = argparse.ArgumentParser(description='Packet fuzzer')
    parser.add_argument('parser', choices=ccn + pycn + picn + none, default='ccn',
                        help="The parser which should be tested")
    parser.add_argument('path', help="Path to the parser on this machine")
    parser.add_argument('-f', '--fuzziness',help='Level of incorrectness',required=False, default=0,type=int,choices=[0,1,2])
    parser.add_argument('-s', '--sleep', help='Milliseconds to sleep between the Packages', default=100, type=int,
                        choices=range(100, 2100, 100), metavar=[100 - 2000], required=False)
    parser.add_argument('-c', '--counter', help='Number of Packets to generate', type=check_positive, default=-1,
                        required=False)
    subparser = parser.add_subparsers(help='parses the protocoll options', dest='protocoll')
    ndnparser = subparser.add_parser("NDN")
    ndnparser.add_argument('-p', '--packages', help='The package type to be sent', nargs='+', required=False, default=0,
                           type=str, choices=['l', 'i'])
    ccnxparser = subparser.add_parser("CCNx")
    ccnxparser.add_argument('-p', '--packages', help='The package type to be sent', nargs='+', required=False,
                            default=0,
                            type=str, choices=['i', 'c'])
    args = parser.parse_args()
    # extract args and setup parser and connection
    for arg in vars(args):
        logger.info("%s set to %s", arg, args.__getattribute__(arg))
    Encode.setFuzziness(args.fuzziness)
    if args.protocoll is None:
        args.protocoll = "NDN"
    if not os.path.exists(args.path):
        logger.error("Path"+args.path+" doesn't exist. Please check for spelling mistakes")
        sys.exit(1)
    paktes = None
    if args.parser in ccn:
        logger.info("CCN invoked with path %s", args.path)
        proc = start.startCCN(args.path)

    elif args.parser in pycn:
        logger.info("PyCN invoked with path %s", args.path)
        proc = start.startPyCN(args.path)

    elif args.parser in picn:
        logger.info("PiCN invoked with path %s", args.path)
        proc = start.startPiCN(args.path)
    elif args.parser in none:
        logger.info("staring without parser")

    time.sleep(5)
    if (args.parser not in none) and (not check_proc_alive(proc)):
        logger.error("Looks like parser couldn't be started. Stopping")
        sys.exit(1)
    # TODO Check if port 9000 is also used on PyCN-lite
    if (args.parser not in none):
        sender = Sender("127.0.0.1", 9000)
    history = []
    try:
        (types, outString) = getSelectedTypes(args.packages, args.protocoll)
    except AttributeError:
        types = protocolToList[args.protocoll]
        outString = "Selected packages: \tAll"
    logger.debug(outString)

    packCount = 0
    # send packages
    while (args.counter == -1 or packCount < args.counter):
        if not (args.parser in none) and not check_proc_alive(proc):
            logger.warning("lost parser")
            break
        # loop
        while True:
            try:
                package = PacketMaker.makePackage[random.choice(list(types))]
                logger.info("Package n° %d \t %s", packCount, package)
                break
            except OverflowError:
                logger.warning("A package grew to large. Skipping it")
        if args.protocoll == "NDN":
            bytes = Encode.encodeNDNPackage(package)
        elif args.protocoll == "CCNx":
            bytes = Encode.encodeCCNxPackage(package)
        if (args.parser not in none):
            sender.sendMessage(bytes.tobytes())
        history.append((package, bytes))
        logger.info("Package no %d Size: %d", packCount, bytes.__len__())
        logger.info("Package no %d depth: %d", packCount, package.getDepth())
        time.sleep(args.sleep / 1000)
        # print(history)
        packCount += 1
    proc.kill()
    p = subprocess.Popen(['ps', '-A H'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
        print(line)
        # if 'iChat' in line:
        # pid = int(line.split(None, 1)[0])
        # os.kill(pid, signal.SIGKILL)
