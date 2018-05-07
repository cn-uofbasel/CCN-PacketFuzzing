import argparse
import os

if __name__ == '__main__':
    ccn = ['ccn', 'ccn-lite']
    pycn = ['py-cn', 'PyCN-lite']
    parser = argparse.ArgumentParser(description='Packet fuzzer')
    parser.add_argument('parser', choices=ccn + pycn, default='ccn', help="the parser which should be tested")
    parser.add_argument('path', help="path to the parser on this machine")
    args = parser.parse_args()
    if args.parser in ccn:
        print("ccn invoked")
        print("with path ", args.path)
    elif args.parser in pycn:
        print("pycn invoked")
        print("with path ", args.path)
