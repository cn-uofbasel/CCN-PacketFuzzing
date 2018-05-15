## Results

CCN-Lite:

900 Packages sent, incorrectness level 0,1,2 --> packages will be ignored if not interpretable

-> works fine.

Future test: 
    -remove non-optional packages from ndn packet
    -also send only a sublevel packet

PiCN:

Bug: MetaInfo optional since NDN packet version 0.3, but PiCN tries to decode meta info even if no meta info is in the
packet --> error not caught --> parser crashes, following packages will be received but not longer decoded.

If MetaInfo is added to protocol, the parser crashes when the length value exeed the buffer length or the subpackges doesn't sum up to the bufferlength. Following packages will be recieved but not longer decoded.

Name Packages are always dropped. Unknown Packet Type

Interestpackages: 900 Packages sent, correctly ignored false info, no errors raised (Fuzziness 0,1)
DataPackes: Fuzziness
LinkObject: TLV Length exceeds the Buffer Length even at fuzziness level 0, where all lengths are correct


