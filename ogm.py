from py2neo import Node, Relationship



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


def get_requests(item_name, tier=1, enchantment=0, quality=0):


	query = f'''
	MATCH (c:Character)-[r:request]->(i:Item)
	WHERE i.Group = {item_name}
	AND i.Tier = {tier}
	AND i.Enchantment = {enchantment}
	AND i.Quality = {quality}
	AND i.LastViewed - {datetime.now()} < 10000
	RETURN r
	ORDER BY r.UnitPriceSilver
	'''

