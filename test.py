from kaitai import Photon
from decoder import Decoder
from scapy.all import sniff, raw
from py2neo import Graph, Node
import json

decoder = Decoder()
graph = Graph(password='password')


def handle_messages(messages):
    print()
    for m in messages:
        m = m.replace(b'true', b'True')
        m = m.replace(b'false', b'False')
        m = m.replace(b'null', b'None')
        m = eval(m)
        print(m)

        node = Node('Message',
                    Id                = m['Id'],
                    UnitPriceSilver   = m['UnitPriceSilver'],
                    TotalPriceSilver  = m['TotalPriceSilver'],
                    Amount            = m['Amount'],
                    Tier              = m['Tier'],
                    IsFinished        = m['IsFinished'],
                    AuctionType       = m['AuctionType'],
                    HasBuyerFetched   = m['HasBuyerFetched'],
                    HasSellerFetched  = m['HasSellerFetched'],
                    SellerCharacterId = m['SellerCharacterId'],
                    SellerName        = m['SellerName'],
                    BuyerCharacterId  = m['BuyerCharacterId'],
                    BuyerName         = m['BuyerName'],
                    ItemTypeId        = m['ItemTypeId'],
                    ItemGroupTypeId   = m['ItemGroupTypeId'],
                    EnchantmentLevel  = m['EnchantmentLevel'],
                    QualityLevel      = m['QualityLevel'],
                    Expires           = m['Expires'])
        print(node)
        graph.merge(node, 'Message', 'Id')



def callback(packet):

    # Deconstruct the packet assuming it follows the Photon protocol
    p = Photon.from_bytes(raw(packet))

    # Iterate over the commands inside the Photons payload
    for command in p.command:

        # If a command is a ReliableFragment...
        if isinstance(command.data, Photon.ReliableFragment):
            fragment = command.data
            messages = decoder.add_fragment(fragment)

            if messages:
                handle_messages(messages)


if __name__ == '__main__':
    capture = sniff(filter='udp port 5056', prn=callback)




