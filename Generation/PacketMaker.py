import pyndn.encoding as enc
from Generation.Package import TLVPackage
import random
from enum import Enum

"""
Building functions for packets. Top level packets can be accessed through makePackage.
"""


class NDNPackages(Enum):
    Interest = 0
    LinkObject = 1


class CCNxPackages(Enum):
    Interest = 0
    Data = 1
    ContentOject = 2


class PackageTypes(Enum):
    NDN = 0
    CCNx = 1


def _makeBasicTLVPackage(name, type, len=-1):
    if len == -1:
        len = _randomLength()
    return TLVPackage(name, type, len)


def _getOptional(makefunc, propability=0.5):
    rand = random.randint(0, 1 / propability)
    if rand == 1:
        return makefunc()
    else:
        return None


def _makeGenericNameComponent():
    return _makeBasicTLVPackage("NameComponent", enc.Tlv.NameComponent)


def _makeNonce():
    return _makeBasicTLVPackage("Nonce", enc.Tlv.Nonce, len=4)


def _makeInterestLifetime():
    return _makeBasicTLVPackage("InterestLifeTime", enc.Tlv.InterestLifetime)


def _makeHopLimit():
    return _makeBasicTLVPackage("HopLimit", 34, len=1)  # not in pyndn


def _makeParameters():
    return _makeBasicTLVPackage("Parameters", 35)  # not in pyndn


def _makeImplicitSha256DigestComponent():
    return _makeBasicTLVPackage("ImplicitSha256DigestComponent", enc.Tlv.ImplicitSha256DigestComponent)


def _makeSignatureType():
    return _makeBasicTLVPackage("SignatureType", enc.Tlv.SignatureType)


def _makeKeyDigest():
    return _makeBasicTLVPackage("KeyDigest", enc.Tlv.KeyLocatorDigest)


def _makeKeyLocator():
    subpackages = []
    r = random.randint(0, 1)
    if r == 0:
        subpackages.append(_makeNamePacket())
    else:
        subpackages.append(_makeKeyDigest())
    return TLVPackage("KeyLocator", enc.Tlv.KeyLocator, _randomLength(1), subpackages)


def _makeSignatureInfo():
    subpackages = []
    stpackage = _makeSignatureType()
    subpackages.append(stpackage)
    klPackage = _getOptional(_makeKeyLocator)
    if klPackage is not None:
        subpackages.append(klPackage)
    length = _randomLength(len(subpackages))
    return TLVPackage("SignatureInfo", enc.Tlv.SignatureInfo, length, subpackages)


def _makeSignatureValue():
    return _makeBasicTLVPackage("SignatureValue", enc.Tlv.SignatureValue)


def _makeContentType():
    return _makeBasicTLVPackage("ContentType", enc.Tlv.ContentType)


def _makeFreshnessPeriod():
    return _makeBasicTLVPackage("FreshnessPeriod", enc.Tlv.FreshnessPeriod)


def _makeFinalBlockId():
    ncpackage = _makeNameComponentPacket()
    return TLVPackage("FinalBlockId", enc.Tlv.FinalBlockId, _randomLength(1), [ncpackage])


def _makeContent():
    return _makeBasicTLVPackage("Content", enc.Tlv.Content)


def _makeMetaInfo():
    subpackages = []
    ctpackage = _getOptional(_makeContentType)
    if ctpackage is not None:
        subpackages.append(ctpackage)
    fppackage = _getOptional(_makeFreshnessPeriod)
    if (fppackage is not None):
        subpackages.append(fppackage)
    fbidpackage = _getOptional(_makeFinalBlockId)
    if (fbidpackage is not None):
        subpackages.append(fbidpackage)
    length = _randomLength(len(subpackages))
    return TLVPackage("MetaInfo", enc.Tlv.MetaInfo, length, subpackages)


def _makePreference():
    return _makeBasicTLVPackage("Preference", enc.Tlv.Link_Preference)


def _makeDelegation():
    subpackages = []
    ppackage = _makePreference()
    subpackages.append(ppackage)
    npackage = _makeNamePacket()
    subpackages.append(npackage)
    length = _randomLength(len(subpackages))
    return TLVPackage("Delegation", enc.Tlv.Link_Delegation, length, subpackages)


def _makeLinkContent():
    subpackages = []
    for x in range(1, 6):
        cpackage = _makeDelegation()
        subpackages.append(cpackage)
    length = _randomLength(len(subpackages))
    return TLVPackage("LinkContent", enc.Tlv.ContentType, length, subpackages)


def _makeMustBeFresh():
    return _makeBasicTLVPackage("MustBeFresh", enc.Tlv.MustBeFresh, len=0)


def _makeNamePacket():
    subpackages = []
    for x in range(random.randint(0, 8)):
        subpackages.append(_makeNameComponentPacket())
    length = _randomLength(len(subpackages))
    return TLVPackage("Name", enc.Tlv.Name, length, subpackages)


def _makeOtherTypeComponent():
    r = list(range(2, 65535))
    r.remove(8)
    return _makeBasicTLVPackage("OtherTypeComponent", random.choice(r))


def _makeNameComponentPacket():
    rand = random.randint(0, 2)
    if rand == 0:
        return _makeGenericNameComponent()
    elif rand == 1:
        return _makeImplicitSha256DigestComponent()
    else:
        return _makeOtherTypeComponent()


def _makeCanBePrefix():
    return _makeBasicTLVPackage("CanBePrefix", 33, len=0)  # not in pynndn encoding


def _makeInterestPacket():
    subpackages = []
    npackage = _makeNamePacket()
    subpackages.append(npackage)
    cbppackage = _getOptional(_makeCanBePrefix)
    if cbppackage is not None:
        subpackages.append(cbppackage)
    fhpackage = _getOptional(_makeForwardingHint)
    if fhpackage is not None:
        subpackages.append(fhpackage)
    mbfpackage = _getOptional(_makeMustBeFresh)
    if mbfpackage is not None:
        subpackages.append(mbfpackage)
    nopackage = _getOptional(_makeNonce)
    if nopackage is not None:
        subpackages.append(nopackage)
    ilpackage = _getOptional(_makeInterestLifetime)
    if ilpackage is not None:
        subpackages.append(ilpackage)
    hplpackage = _getOptional(_makeHopLimit)
    if hplpackage is not None:
        subpackages.append(hplpackage)
    ppackage = _getOptional(_makeParameters)
    if ppackage is not None:
        subpackages.append(ppackage)
    length = _randomLength(len(subpackages))
    ipackage = TLVPackage("Interest", enc.Tlv.Interest, length, subpackages)
    return ipackage


def _makeForwardingHint():
    subpackages = []
    for x in range(1, 6):
        subpackages.append(_makeDelegation())
    length = _randomLength(len(subpackages))
    return TLVPackage("ForwardingHint", enc.Tlv.ForwardingHint, length, subpackages)

def _makeDataPacket():
    subpackages = []
    npackage = _makeNamePacket()
    subpackages.append(npackage)
    mipackage = _getOptional(_makeMetaInfo)
    if mipackage is not None:
        subpackages.append(mipackage)
    cpackage = _getOptional(_makeContent)
    if cpackage is not None:
        subpackages.append(cpackage)
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


makePackage = {NDNPackages.Interest: _makeInterestPacket(),
               NDNPackages.LinkObject: _makeLinkObject(),
               NDNPackages.Data: _makeDataPacket(),
               CCNxPackages.Interest: _makeCCNxInterest(),
               CCNxPackages.ContentOject: _makeCCNxContentObject()
               }
