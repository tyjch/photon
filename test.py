from kaitai.photon import Photon
from decoder import Decoder
from scapy.all import sniff, raw
from py2neo import Graph, Node, Relationship
from ogm import get_item, get_character
from datetime import datetime
from utility import convert_to_ts, alert
from items import item_dict
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
	        UnitPriceSilver=int(str(m['UnitPriceSilver'])[:-4]),
	        Expires=convert_to_ts(m['Expires']),
	        LastViewed=datetime.timestamp(datetime.now())
        )

        print(m)
        graph.merge(msg, m['AuctionType'], 'Id')
        get_profitable_trades(m, bankroll=150000)


def callback(packet):
    try:
        p = Photon.from_bytes(raw(packet))

        for command in p.command:
            if isinstance(command.data, Photon.ReliableFragment):
                fragment = command.data
                messages = decoder.add_fragment(fragment)

                if messages:
                    handle_messages(messages)
    except EOFError:
        print('Unable to parse packet')
    except ValueError:
        print('Packet is probably malformed')


def get_profitable_trades(m, after_ts=20000, bankroll=30000):
    current_ts = datetime.timestamp(datetime.now())
    item = get_item(m)

    query = f'''
    	MATCH (:Character)-[r:request]->(i:Item)<-[o:offer]-(:Character)
    	WHERE ({current_ts} - r.LastViewed) < {after_ts}
    	AND ({current_ts} - o.LastViewed) < {after_ts}
    	AND i.Group = '{m["ItemGroupTypeId"]}'
    	AND i.Tier = {m["Tier"]}
    	AND i.Enchantment = {m["EnchantmentLevel"]}
    	AND i.Quality = {m["QualityLevel"]}
    	AND (r.UnitPriceSilver - o.UnitPriceSilver) > 0 
    	AND (o.UnitPriceSilver < {bankroll})
    	RETURN i, r.UnitPriceSilver as sell_price, o.UnitPriceSilver as buy_price, (r.UnitPriceSilver - o.UnitPriceSilver) as profit
    	ORDER BY profit
    	LIMIT 1
    	'''

    response = graph.run(query)

    for r in response:
        data = r.data()
        item = data['i']

        buy_price = data['buy_price']
        sell_price = data['sell_price']
        profit = data['profit']

        if profit > 3000:
            item_name = item_dict[item['Group']]
            #alert(str(profit))

            print()
            print('__' * 20)
            print('>>> ', item_name)
            print('T: ', item['Tier'])
            print('E: ', item['Enchantment'])
            print('Q: ', item['Quality'])
            print('Buy for:  $', buy_price)
            print('Sell for: $', sell_price)
            print('PROFIT =  $', profit)
            print('__' * 20)



if __name__ == '__main__':

    capture = sniff(filter='udp port 5056', prn=callback)




