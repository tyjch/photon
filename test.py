from kaitai import Photon
from decoder import Decoder
from scapy.all import sniff, raw
from py2neo import Graph, Node, Relationship
import json


decoder = Decoder()
graph   = Graph(password='password')


def preprocess_message(m):
    m = m.replace(b'true', b'True')
    m = m.replace(b'false', b'False')
    m = m.replace(b'null', b'None')
    return eval(m)


def handle_messages(messages):
    for m in messages:
        m = preprocess_message(m)

        if m['AuctionType'] == 'request':
            handle_request_message(m)

        elif m['AuctionType'] == 'offer':
            handle_offer_message(m)

        print(m)


def handle_request_message(m):
    item = Node(
        'Item',
        ItemTypeId=m['ItemTypeId'] + '&' + str(m['QualityLevel']),
        ItemGroupTypeId=m['ItemGroupTypeId'],
        Tier=m['Tier'],
        EnchantmentLevel=m['EnchantmentLevel'],
        QualityLevel=m['QualityLevel']
    )

    item.__primarylabel__ = "Item"
    item.__primarykey__ = 'ItemTypeId'

    market_request = Node(
        'Request',
        Id=m['Id'],
        Amount=m['Amount'],
        UnitPriceSilver=m['UnitPriceSilver'],
        Expires=m['Expires']
    )

    market_request.__primarylabel__ = 'Request'
    market_request.__primarykey__ = 'Id'

    character = Node(
        'Character',
        CharacterId=m['BuyerCharacterId'],
        Name=m['BuyerName']
    )

    character.__primarylabel__ = 'Character'
    character.__primarykey__ = 'CharacterId'

    request_by_character = PostedBy(market_request, character)
    item_of_request = HasItemType(market_request, item)
    subgraph = item_of_request | request_by_character

    graph.merge(subgraph)


def handle_offer_message(m):
    item = Node(
        'Item',
        ItemTypeId=m['ItemTypeId'] + '&' + str(m['QualityLevel']),
        ItemGroupTypeId=m['ItemGroupTypeId'],
        Tier=m['Tier'],
        EnchantmentLevel=m['EnchantmentLevel'],
        QualityLevel=m['QualityLevel']
    )

    item.__primarylabel__ = "Item"
    item.__primarykey__ = 'ItemTypeId'

    market_offer = Node(
        'Offer',
        Id=m['Id'],
        Amount=m['Amount'],
        UnitPriceSilver=m['UnitPriceSilver'],
        Expires=m['Expires']
    )

    market_offer.__primarylabel__ = 'Offer'
    market_offer.__primarykey__ = 'Id'

    character = Node(
        'Character',
        CharacterId=m['SellerCharacterId'],
        Name=m['SellerName']
    )

    character.__primarylabel__ = 'Character'
    character.__primarykey__ = 'CharacterId'

    offer_by_character = PostedBy(market_offer, character)
    item_of_offer = HasItemType(market_offer, item)
    subgraph = item_of_offer | offer_by_character

    graph.merge(subgraph)


def callback(packet):

    # Deconstruct the packet assuming it follows the Photon protocol
    p = Photon.from_bytes(raw(packet))

    # Iterate over the commands inside the Photons payload
    for command in p.command:

        # If a command is a ReliableFragment...
        if isinstance(command.data, Photon.ReliableFragment):
            fragment = command.data
            messages = decoder.add_fragment(fragment)

            # TODO: Need to check if the message is a market order or request
            if messages:
                handle_messages(messages)


if __name__ == '__main__':
    graph.delete_all()
    capture = sniff(filter='udp port 5056', prn=callback)




