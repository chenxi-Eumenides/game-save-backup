from farm import *
from utils import get_bp, print_item_change


# 根据坐标种数或灌木
def farm_tree_buch(water):
	till_auto(Entities.Tree)
	water_to(water)
	if can_harvest():
		harvest()
	if get_entity_type() in [None, Entities.Grass]:
		if get_pos_x() % 2 == get_pos_y() % 2:
			plant(Entities.Tree)
		else:
			plant(Entities.Bush)


# 种木头
def farm_wood(water=-1):
	move_to(0, 0)
	for _ in range(get_farm_size()):
		farm_tree_buch(water)
		move_snake()


def main():
	# 初始化
	water = -1
	set_world_size(10)
	clear()
	# 种树
	while True:
		bp = get_bp()
		farm_wood(water)
		print_item_change(bp, [Items.Wood])


if __name__ == "__main__":
	main()
