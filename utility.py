from scapy.all import *


def get_hexdump_str(packet):
    dump = linehexdump(packet, dump=True)
    dump = dump.split(sep='  ')
    return dump[0], dump[1]


if __name__ == '__main__':

    capture = sniff(filter='udp port 5056', count=5)

    for packet in capture:
        h, l = get_hexdump_str(packet)
        print(h)
        print(l)