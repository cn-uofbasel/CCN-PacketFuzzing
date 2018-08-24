from Logger import Logger

"""
Module for custom encoders.

An encoder is considered a byte buffer with special functions to support the creation of a specific protocol package.
"""

class CCNxEncoder:
    """
    The encoder for CCNx packages. This encoder is designed as a dynamic bytearraybuffer which is filled back to front and grows in bytes.
    The design is made like the pyndn TLVEncoder in minimal form.
    """
    def __init__(self, initialcapacity=8):
        """
        creates a new encoder with a buffer for 8 bytes as this is the size for a fixed header without any payload
        :param initialcapacity: the initalsize of the internal bytearray. Grows dynamically
        """
        self._buffer = bytearray(8)
        self._length = 0

    def writeNumberFixedSize(self, number, size):
        """
                writes a number into the buffer and adds padding for the given size.
                :param number: the value to write
                :param size: size in bytes
                """
        bytes = number.to_bytes(size, byteorder='big')
        newlength = self._length + size
        self._ensurelength(newlength)
        for x in range(newlength - self._length):
            self._buffer[-newlength + x] = bytes[x]
        self._length = newlength


    def writeNumber(self, number):
        """
        writes a number like writeNumberFixedSize but the size is adjusted to the minimal bytesize needed.
        :param number: the value to write
        """
        size = 1
        while True:
            try:
                bytes = number.to_bytes(size, byteorder='big')
                break
            except OverflowError:
                size += 1
        newlength = self._length + size
        self._ensurelength(newlength)
        for x in range(newlength - self._length):
            self._buffer[-newlength + x] = bytes[x]
        self._length = newlength

    def _ensurelength(self, length):
        """
        dynamically extends the bytearray to the fit the given length
        :param length: the new length
        """
        if (len(self._buffer) < length):
            newArray = bytearray(length)
            newArray[-len(self._buffer):] = self._buffer
            self._buffer = newArray

    def writeByteArray(self, bytes):
        """
        writes another bytearray into the buffer
        :param bytes: bytearray to copy
        """
        newlength = self._length + len(bytes)
        self._ensurelength(newlength)
        for x in range(newlength - self._length):
            self._buffer[-newlength + x] = bytes[x]
        self._length = newlength

    def writeMemoryView(self, view):
        """
        copies a memoryview of a bytearray into the buffer
        :param view: memoryview of a bytearray

        this method is used to add
        """
        newlength = self._length + len(view.obj)
        self._ensurelength(newlength)
        for x in range(newlength - self._length):
            self._buffer[-newlength + x] = view.obj[x]
        self._length = newlength

    def __len__(self):
        return self._length


    def getOutput(self):
        return memoryview(
            self._buffer)[self._length:]
