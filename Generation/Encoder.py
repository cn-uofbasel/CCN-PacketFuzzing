from Logger import Logger


class CCNxEncoder:
    def __init__(self, initialcapacity=8):
        self._buffer = bytearray(8)
        self._length = 0

    def writeNumberFixedSize(self, number, size):
        try:
            bytes = number.to_bytes(size, byteorder='big')
            newlength = self._length + size
            self.ensurelength(newlength)
            self._buffer[-newlength:-self._length] = bytes
            self._length = newlength
        except OverflowError:
            logger = Logger()
            logger.error("Number %d doesn't fit in size %d", number, size)

    def writeNumber(self, number):
        size = 1
        while True:
            try:
                bytes = number.to_bytes(size, byteorder='big')
                break
            except OverflowError:
                size += 1
        newlength = self._length + size
        self.ensurelength(newlength)
        for x in range(newlength - self._length):
            self._buffer[-newlength + x] = bytes[x]
        self._length = newlength
        print(self._buffer)

    def ensurelength(self, length):
        if (len(self._buffer) < length):
            newArray = bytearray(length)
            # Copy into newArray at offset.
            newArray[-len(self._buffer):] = self._buffer
            self._buffer = newArray
