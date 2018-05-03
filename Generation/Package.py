class Package:

    def __init__(self, name, type, len, rlen, subpackages=None):
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
        string = self.name + "(" + type + ")" + "\n" + "written length: " + len + "\n" + "real length: " + rlen + "\n"
        if self.subpackages != None:
            subpackages = str(self.subpackages)
            string += "with subpackages " + subpackages
        return string
