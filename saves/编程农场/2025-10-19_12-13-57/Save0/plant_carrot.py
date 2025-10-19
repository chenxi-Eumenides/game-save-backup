from farm import *
from utils import get_bp,print_item_change

def farm_carrot(water):
	if can_harvest():
		harvest()
	till_auto(Entities.Carrot)
	water_to(water)
	plant(Entities.Carrot)
	move_snake()

if __name__ == "__main__":
	# 初始化
	water = -1
	all_items = [
		Items.Carrot,
		Items.Hay,
		Items.Wood
	]
	clear()
	# 种植
	while check_cost(Entities.Carrot,farm_size):
		bp = get_bp()
		for _ in range(farm_size):
			farm_carrot(water)
		print_item_change(bp,all_items)