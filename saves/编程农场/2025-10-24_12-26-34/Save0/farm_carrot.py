from farm import *
from utils import get_bp, print_item_change


# 种一次
def farm_carrot_once(water):
	if can_harvest():
		harvest()
	till_auto(Entities.Carrot)
	water_to(water)
	plant(Entities.Carrot)
# 种胡萝卜
def farm_carrot(water=-1):
	move_to(0,0)
	for _ in range(get_farm_size()):
		farm_carrot_once(water)
		move_snake()
def main():
	# 初始化
	water = -1
	all_items = [
		Items.Carrot,
		Items.Hay,
		Items.Wood
	]
	set_world_size(10)
	clear()
	# 种植
	while check_cost(Entities.Carrot,get_farm_size()):
		bp = get_bp()
		farm_carrot(water)
		print_item_change(bp,all_items)

if __name__ == "__main__":
	main()