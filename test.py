from kaitai.photon import Photon
from decoder import Decoder
from scapy.all import sniff, raw
from py2neo import Graph, Node, Relationship
from ogm import get_item, get_character
from datetime import datetime
from utility import convert_to_ts
import json

decoder = Decoder()
graph = Graph(password='password')


def preprocess_message(m):
    m = m.replace(b'true', b'True')
    m = m.replace(b'false', b'False')
    m = m.replace(b'null', b'None')
    return eval(m)


def handle_messages(messages):
    for m in messages:
        m    = preprocess_message(m)
        item = get_item(m)
        char = get_character(m)

        msg = Relationship(
	        char,
	        m['AuctionType'],
	        item,
	        Id=m['Id'],
	        Amount=m['Amount'],
	        UnitPriceSilver=m['UnitPriceSilver'],
	        Expires=convert_to_ts(m['Expires']),
	        LastViewed=datetime.timestamp(datetime.now())
        )

        print(msg)
        graph.merge(msg, m['AuctionType'], 'Id')



def callback(packet):
    p = Photon.from_bytes(raw(packet))

    for command in p.command:
        if isinstance(command.data, Photon.ReliableFragment):
            fragment = command.data
            messages = decoder.add_fragment(fragment)

            if messages:
                handle_messages(messages)


if __name__ == '__main__':
    capture = sniff(filter='udp port 5056', prn=callback)




