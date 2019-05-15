from kaitai import Photon
from decoder import Decoder
from kaitaistruct import KaitaiStream, BytesIO
from scapy.all import sniff, raw
from pprint import pprint
import json


decoder = Decoder()


def handle_messages(messages):
    print()
    for m in messages:
        print(m)


def callback(packet):

    # Deconstruct the packet assuming it follows the Photon protocol
    p = Photon.from_bytes(raw(packet))

    # Iterate over the commands inside the Photons payload
    for command in p.command:

        if isinstance(command.data, Photon.ReliableFragment):
            fragment = command.data
            messages = decoder.add_fragment(fragment)

            if messages:
                handle_messages(messages)


if __name__ == '__main__':
    capture = sniff(filter='udp port 5056', prn=callback)




