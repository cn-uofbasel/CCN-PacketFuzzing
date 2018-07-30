import pyndn.encoding as enc
from Generation.Package import TLVPackage
import random
from enum import Enum

"""
Building functions for packets. Top level packets can be accessed through makePackage.
"""

class NDNPackages(Enum):
    Name = 0
    Interest = 1
    Data = 2
    LinkObject = 3


class CCNxPackages(Enum):
    Interest = 0
    ContentOject = 1


class PackageTypes(Enum):
    NDN = 0
    CCNx = 1


def _makeBasicTLVPackage(name, type):
    len = _randomLength()
    return TLVPackage(name, type, len)


def _makeGenericNameComponent():
    return _makeBasicTLVPackage("NameComponent", enc.Tlv.NameComponent)


def _makeImplicitSha256DigestComponent():
    return _makeBasicTLVPackage("ImplicitSha256DigestComponent", enc.Tlv.ImplicitSha256DigestComponent)


def _makeSignatureType():
    return _makeBasicTLVPackage("SignatureType", enc.Tlv.SignatureType)


def _makeSignatureInfo():
    len = _randomLength()
    stpackage = _makeSignatureType()
    return TLVPackage("SignatureInfo", enc.Tlv.SignatureInfo, len, [stpackage])


def _makeSignatureValue():
    return _makeBasicTLVPackage("SignatureValue", enc.Tlv.SignatureValue)


def _makeMetaInfo():
    return _makeBasicTLVPackage("MetaInfo", enc.Tlv.MetaInfo)


def _makePreference():
    return _makeBasicTLVPackage("Preference", enc.Tlv.Link_Preference)


def makeDelegation():
    subpackages = []
    ppackage = _makePreference()
    subpackages.append(ppackage)
    npackage = _makeNamePacket()
    subpackages.append(npackage)
    length = _randomLength(len(subpackages))
    return TLVPackage("Delegation", enc.Tlv.Link_Delegation, length, subpackages)


def _makeLinkContent():
    cpackage = makeDelegation()
    length = _randomLength(1)
    return TLVPackage("LinkContent", enc.Tlv.ContentType, length, [cpackage])

def _makeNamePacket():
    subpackages = []
    for x in range(random.randint(0, 8)):
        subpackages.append(_makeNameComponentPacket())
    length = _randomLength(len(subpackages))
    return TLVPackage("Name", enc.Tlv.Name, length, subpackages)


def _makeOtherTypeComponent():
    r = range(2, 8) + range(9, 65535)
    return _makeBasicTLVPackage("OtherTypeComponent", random.choice(r))


def _makeNameComponentPacket():
    rand = random.randint(0, 2)
    subpackages = []
    if rand == 0:
        subpackages.append(_makeGenericNameComponent())
    elif rand == 1:
        subpackages.append(_makeImplicitSha256DigestComponent())
    else:
        subpackages.append(_makeOtherTypeComponent())
    length = _randomLength(len(subpackages))
    npackage = TLVPackage("NameComponent", enc.Tlv.NameComponent, length, subpackages)
    return npackage


def _makeInterestPacket():
    subpackages = []
    npackage = _makeNamePacket()
    subpackages.append(npackage)
    length = _randomLength(len(subpackages))
    ipackage = TLVPackage("Interest", enc.Tlv.Interest, length, subpackages)
    return ipackage


def _makeDataPacket():
    subpackages = []
    npackage = _makeNamePacket()
    subpackages.append(npackage)
    mipackage = _makeMetaInfo()
    subpackages.append(mipackage)
    sipackage = _makeSignatureInfo()
    subpackages.append(sipackage)
    svpackage = _makeSignatureValue()
    subpackages.append(svpackage)
    length = _randomLength(len(subpackages))
    datpackage = TLVPackage("Data", enc.Tlv.Data, length, subpackages)
    return datpackage


def _makeLinkObject():
    subpackages = []
    npackage = _makeNamePacket()
    subpackages.append(npackage)
    mipackage = _makeMetaInfo()
    subpackages.append(mipackage)
    lcpackage = _makeLinkContent()
    subpackages.append(lcpackage)
    sipackage = _makeSignatureInfo()
    subpackages.append(sipackage)
    svpackage = _makeSignatureValue()
    subpackages.append(svpackage)
    length = _randomLength(len(subpackages))
    linkObject = TLVPackage("LinkObject", enc.Tlv.Data, length, subpackages)
    return linkObject


def _randomLength(subpackes=1):
    random.random()
    return random.randint(0, 40 * subpackes)


def _makeCCNxName():
    subpackages = []
    for x in range(random.randint(0, 8)):
        p = _makeBasicTLVPackage("Name Segment", 0x0001)
        subpackages.append(p)
    length = _randomLength(len(subpackages))
    return TLVPackage("Name", 0x0000, length, subpackages)


def _makeKeyIdRestriciton():
    return _makeBasicTLVPackage("KeyIdRestriction", 0x0002)


def _makeContentObjectHashRestriciton():
    return _makeBasicTLVPackage("ContentObjectHashRestriction", 0x0003)


def _makeCCNxInterest():
    subpackages = []
    namep = _makeCCNxName()
    subpackages.append(namep)
    x = random.randint(0, 3)
    if x % 2 is 1:
        kidp = _makeKeyIdRestriciton()
        subpackages.append(kidp)
    if x > 1:
        cohrp = _makeContentObjectHashRestriciton()
        subpackages.append(cohrp)
    length = _randomLength(len(subpackages))
    return TLVPackage("Interest", 0x0000, length, subpackages)


def _makePayloadType():
    return _makeBasicTLVPackage("Payload", 0x0005)


def _makeExpiriyTime():
    return TLVPackage("ExpiryTime", 0x0006, 8)


def _makeCCNxContentObject():
    subpackages = []
    namep = _makeCCNxName()
    subpackages.append(namep)
    x = random.randint(0, 3)
    if x % 2 is 1:
        ptp = _makePayloadType()
        subpackages.append(ptp)
    if x > 1:
        extp = _makeExpiriyTime()
        subpackages.append(extp)
    length = _randomLength(len(subpackages))
    return TLVPackage("ContentOject", 0x0002, length, subpackages)


makePackage = {NDNPackages.Name: _makeNamePacket(),
               NDNPackages.Data: _makeDataPacket(),
               NDNPackages.Interest: _makeInterestPacket(),
               NDNPackages.LinkObject: _makeLinkObject(),
               CCNxPackages.Interest: _makeCCNxInterest(),
               CCNxPackages.ContentOject: _makeCCNxContentObject()
               }
