import pyndn.encoding as enc
from Generation.Package import Package
import random
from enum import Enum


class Packages(Enum):
    Name = 0
    Interest = 1
    Data = 2
    LinkObject = 3


def makeBasicPackage(name, type):
    len = randomLength()
    return Package(name, type, len)


def makeGenericNameComponent():
    return makeBasicPackage("NameComponent", enc.Tlv.NameComponent)


def makeImplicitSha256DigestComponent():
    return makeBasicPackage("ImplicitSha256DigestComponent", enc.Tlv.ImplicitSha256DigestComponent)


def makeSignatureType():
    return makeBasicPackage("SignatureType", enc.Tlv.SignatureType)


def makeSignatureInfo():
    len = randomLength()
    stpackage = makeSignatureType()
    return Package("SignatureInfo", enc.Tlv.SignatureInfo, len, [stpackage])


def makeSignatureValue():
    return makeBasicPackage("SignatureValue", enc.Tlv.SignatureValue)


def makeMetaInfo():
    return makeBasicPackage("MetaInfo", enc.Tlv.MetaInfo)


def makePreference():
    return makeBasicPackage("Preference", enc.Tlv.Link_Preference)

def makeMetaInfo():
    return makeBasicPackage("MetaInfo",enc.Tlv.MetaInfo)


def makeDelegation():
    subpackages = []
    ppackage = makePreference()
    subpackages.append(ppackage)
    npackage = makeNamePacket()
    subpackages.append(npackage)
    length = randomLength(len(subpackages))
    return Package("Delegation", enc.Tlv.Link_Delegation, length, subpackages)


def makeLinkContent():
    cpackage = makeDelegation()
    len = randomLength(1)
    return Package("LinkContent", enc.Tlv.ContentType, len, [cpackage])

def makeNamePacket():
    gncpackage = makeGenericNameComponent()
    isdpackage = makeImplicitSha256DigestComponent()
    length = randomLength(2)
    npackage = Package("Name", enc.Tlv.Name, length, [gncpackage, isdpackage])
    return npackage


def makeInterestPacket():
    subpackages = []
    npackage = makeNamePacket()
    subpackages.append(npackage)
    length = randomLength(len(subpackages))
    ipackage = Package("Interest", enc.Tlv.Interest, length, subpackages)
    return ipackage


def makeDataPacket():
    subpackages = []
    npackage = makeNamePacket()
    subpackages.append(npackage)
    mipackage = makeMetaInfo()
    subpackages.append(mipackage)
    sipackage = makeSignatureInfo()
    subpackages.append(sipackage)
    svpackage = makeSignatureValue()
    subpackages.append(svpackage)
    length = randomLength(len(subpackages))
    datpackage = Package("Data", enc.Tlv.Data, length, subpackages)
    return datpackage


def makeLinkObject():
    subpackages = []
    npackage = makeNamePacket()
    subpackages.append(npackage)
    mipackage = makeMetaInfo()
    subpackages.append(mipackage)
    lcpackage = makeLinkContent()
    subpackages.append(lcpackage)
    sipackage = makeSignatureInfo()
    subpackages.append(sipackage)
    svpackage = makeSignatureValue()
    subpackages.append(svpackage)
    length = randomLength(len(subpackages))
    linkObject = Package("LinkObject", enc.Tlv.Data, length, subpackages)
    return linkObject


def randomLength(subpackes=1):
    random.random()
    return random.randint(0, 20 * subpackes)


makePackage = {Packages.Name: makeNamePacket(),
               Packages.Data: makeDataPacket(),
               Packages.Interest: makeInterestPacket(),
               Packages.LinkObject: makeLinkObject()
               }
