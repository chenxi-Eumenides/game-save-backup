from farm import move_to
from utils import get_bp,print_item_change

if __name__ == "__main__":
	low,high = 500,5500
	flag = False
	maze_size = 2
	maze_level = 2
	clear()
	bp = get_bp()
	while True:
		if num_items(Items.Weird_Substance)>high:
			print_item_change(bp)
			bp = get_bp()
			flag = True
		elif num_items(Items.Weird_Substance)<low:
			print_item_change(bp)
			bp = get_bp()
			flag = False
		if flag:
			move_to(0,0)
			plant(Entities.Bush)
			use_item(Items.Weird_Substance, maze_size*maze_level)
			if get_entity_type() == Entities.Treasure:
				harvest()
				continue
			res = move(North)
			if res and get_entity_type() == Entities.Treasure:
				harvest()
				continue
			res = move(East)
			if res and get_entity_type() == Entities.Treasure:
				harvest()
				continue
			harvest()
		else:
			use_item(Items.Fertilizer)
			harvest()