from py2neo import Graph, Node, Relationship
from datetime import datetime
from items import item_dict



def get_item(message):
	group       = message['ItemGroupTypeId']
	enchantment = message['EnchantmentLevel']
	quality     = message['QualityLevel']
	item_id     = f"{group}@{enchantment}&{quality}"

	item_node = Node(
		'Item',
		Id = item_id,
		Group = message['ItemGroupTypeId'],
		Tier = message['Tier'],
		Enchantment = enchantment,
		Quality = quality
	)

	item_node.__primarylabel__ = "Item"
	item_node.__primarykey__ = 'Id'

	return item_node


def get_character(message):
	if message['AuctionType'] == 'request':
		char_id = message['BuyerCharacterId']
		char_name = message['BuyerName']
	elif message['AuctionType'] == 'offer':
		char_id = message['SellerCharacterId']
		char_name = message['SellerName']

	char_node = Node(
		'Character',
		Id = char_id,
		Name = char_name
	)

	char_node.__primarylabel__ = 'Character'
	char_node.__primarykey__ = 'Id'

	return char_node


def get_requests(item_name, tier=1, enchantment=0, quality=0, after_ts=1000):
	graph = Graph(password='password')
	current_ts = datetime.timestamp(datetime.now())

	query = f'''
	MATCH (:Character)-[r:request]->(i:Item)<-[o:offer]-(:Character)
	WHERE i.Group = "{item_name}" 
	AND i.Tier = {tier}
	AND i.Enchantment = {enchantment}
	AND i.Quality = {quality}
	AND ({current_ts} - r.LastViewed) < {after_ts}
	AND ({current_ts} - o.LastViewed) < {after_ts}
	AND (r.UnitPriceSilver < o.UnitPriceSilver) 
	RETURN i, (r.UnitPriceSilver - o.UnitPriceSilver) as profit
	ORDER BY profit
	'''

	return graph.run(query)

def get_profitable_trades(after_ts=100000):
	graph = Graph(password='password')
	current_ts = datetime.timestamp(datetime.now())

	query = f'''
	MATCH (:Character)-[r:request]->(i:Item)<-[o:offer]-(:Character)
	WHERE ({current_ts} - r.LastViewed) < {after_ts}
	AND ({current_ts} - o.LastViewed) < {after_ts}
	AND (r.UnitPriceSilver - o.UnitPriceSilver) > 0 
	RETURN i, r.UnitPriceSilver as sell_price, o.UnitPriceSilver as buy_price, (r.UnitPriceSilver - o.UnitPriceSilver) as profit
	ORDER BY profit
	'''

	response = graph.run(query)


	for r in response:
		data = r.data()
		item = data['i']

		buy_price  = data['buy_price']
		sell_price = data['sell_price']
		profit     = data['profit']

		item_name = item_dict[item['Group']]

		print()
		print('__' * 20)
		print('>>> ', item_name)
		print('T: ', item['Tier'])
		print('E: ', item['Enchantment'])
		print('Q: ', item['Quality'])
		print('Buy for:  $', str(buy_price)[:-4])
		print('Sell for: $', str(sell_price)[:-4])
		print('PROFIT =  $', str(profit)[:-4])
		print('__' * 20)





if __name__ == '__main__':

	response = get_profitable_trades()
