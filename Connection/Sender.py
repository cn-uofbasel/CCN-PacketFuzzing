import socket
import ipaddress
import logging

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
        try:
            #self.ip = ipaddress.ip_address('127.0.0.1')
            self.ip = "127.0.0.1"
        except ipaddress.AddressValueError:
            print(self.ip)
            self.ip = input("Please specify a correct IP address in form of \"127.0.0.1\"")

        logging.debug("Ip address set to %s" % str(self.ip))
        self.port = port
        logging.debug("Port set to %d" % self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        logging.debug("Socket created.")

    """
    Method that uses the UDP socket to send the given message. 
    
    @:parameter message     The message to be sent in bytes.
    """

    def sendMessage(self, message):
        self.socket.sendto(message, (self.ip, self.port))


if __name__ == "__main__":
    send = Sender("127.0.0.1", 9000)
