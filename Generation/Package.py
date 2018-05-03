class Package:

    def __init__(self, name, type, len, rlen, subpackages=None):
        """Represents a NDN Package with all necesary data to randomize length and value
            this class is for generation purpose and will be converted into a "real" NDN-Package

            name -- Name of the Package, for info
            type -- the number representing the package type in the tlv format
            len -- the length which will be written into the the packet
            rlen -- the real byte length of the package
            subpackages -- list of recursive subpackages this package should contain
            """
        if subpackages != None:
            self.rlen = 0
            for p in subpackages:
                self.rlen += p.rlen
        else:
            self.rlen = rlen
        self.name = name
        self.type = type
        self.len = len
        self.subpackages = subpackages

    def __repr__(self):
        type = str(self.type)
        len = str(self.len)
        rlen = str(self.rlen)
        string = self.name + "(" + type + ")" + "| written length: " + len + "| real length: " + rlen + "\n"
        if self.subpackages != None:
            subpackages = str(self.subpackages)
            string += "with subpackages " + subpackages
        return string
