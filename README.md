# CCN-PacketFuzzing
**Packet Fuzzer for CCN Packet Formats.**  
This fuzzer randomizes the TLV-Components of NDN and CCNx and can change the length values.
It is written in Python 3.6, runs on Linux and is able to test CCN-lite, PiCN and PyCN-lite.

## Setup

1.  Clone the Repository

  ```bash
  git clone https://github.com/cn-uofbasel/CCN-PacketFuzzing.git
  ```

2. Run setup.py

  ```bash
  cd CCN-PacketFuzzing
  python3.6 setup.py install
  ```

## Usage
#### Parsers
To test one of the supported parsers, you have to have it on your machine. Infos for Installation can be found here:
  - CCN-lite: https://github.com/cn-uofbasel/ccn-lite/blob/master/doc/README-unix.md
  - PiCN: https://github.com/cn-uofbasel/PiCN
  - PyCN-lite: https://github.com/cn-uofbasel/PyCN-lite

#### Run
```bash
python3.6 Packet_Fuzzing.py 'parser' 'path'
```
**Parser**: This indicates the program that should be tested.  
**Path**: The relative or absolute path to the main folder of the parser.

**Examples**
```bash
python3.6 Packet_Fuzzing.py picn ../PiCN

python3.6 Packet_Fuzzing ccn ~/MyTestfile/ccn-lite
```

## Options
The CCN-PacketFuzzer brings some command line options. For a quick help run the program with argument `-h` or `--help`
### Simple Optionals
#### Fuzziness Level
`-f` or `--fuzziness`
- 0: All length values are correct
- 1: The length values at deepest recursion level in the TLV's are wrong
- 2: All Length values are wrong

The default is 0

#### Sleep
`-s` or `--sleep`
This sets the timer between to packages in Milliseconds. It accepts values between 100 and 2000 both included. Default value is 100

#### Counter
Per default the Fuzzer is running until the parser crashes or it is interrupted.
This can be changed with `-c` or `--counter`. It declares how many packets should be send and accepts any positive number in integer range. If the parser crashes, the program is still stopped.

### Protocol
After all optional arguments there can be a protocol field.
`NDN` or `CCNx`. For command line help type:
```bash
python3 Packet_Fuzzing.py 'parser' 'path' 'protocoll' -h
```
This specifies the packet type the fuzzer is using. Default is NDN.
#### Protocol options
The protocols themselves have the option to specify which packet types should be send with `-p` or `--protocoll`. These are for
**NDN**:
- l: LinkObject
- i: Interest
- d: Data

**CCNx**:
- i: Interest
- c: ContentObject

All packet types can be combined.
**Examples**:
NDN packages without LinkObject.
```bash
python3.6 Packet_Fuzzing.py ccn ../ccn-lite NDN -p i d
```

### offline
There is the possibility to give `offline` as parser. This means no connection will be established and the fuzzer runs on its own. This is for debugging purpose

