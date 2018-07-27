import socket
import ipaddress
import logging
import binascii
from Logger import Logger

logging.basicConfig(level=logging.DEBUG)

"""
Class to initialize a UDP connection to a specific port and ip address to later on send messages.
"""


class Sender:

    """
    Constructor of the sender which requires an ipv4 address and a port to be specified

    @:param ip      The ip address in the format of "127.0.0.1"
    @:param port    The port as an integer
    """
    def __init__(self, ip, port):
        logger = Logger.getLogger()
        try:
            #self.ip = ipaddress.ip_address('127.0.0.1')
            self.ip = "127.0.0.1"
        except ipaddress.AddressValueError:
            logger.debug(self.ip)
            self.ip = input("Please specify a correct IP address in form of \"127.0.0.1\"")

        logger.debug("Ip address set to %s" % str(self.ip))
        self.port = port
        logger.debug("Port set to %d" % self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        logger.debug("Socket created.")
        logger.info("opened connection")

    """
    Method that uses the UDP socket to send the given message. 
    
    @:parameter message     The message to be sent in bytes.
    """

    def sendMessage(self, message):
        logger = Logger.getLogger()
        logger.debug("Message in Bytes: \t %a",binascii.hexlify(message))
        self.socket.sendto(message, ('localhost', 9000))
