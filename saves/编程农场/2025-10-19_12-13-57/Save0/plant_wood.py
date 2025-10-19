from farm import *
from utils import get_bp,print_item_change

def farm_tree_buch(water):
	till_auto(Entities.Tree)
	water_to(water)
	if can_harvest():
		harvest()
	if get_entity_type() in [None,Entities.Grass]:
		if get_pos_x()%2==get_pos_y()%2:
			plant(Entities.Tree)
		else:
			plant(Entities.Bush)
	move_snake()

if __name__ == "__main__":
	# 初始化
	water = -1
	clear()
	# 种树
	while True:
		bp = get_bp()
		for _ in range(farm_size):
			farm_tree_buch(water)
		print_item_change(bp,[Items.Wood])