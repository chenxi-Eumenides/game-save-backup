from farm import *
from utils import lct_id2xy,sleep,set2list,quick_sort
from utils import get_bp,print_item_change

def farm_pumpkin_once(water=0.75):
	#global farm_size
	for i in range(farm_size):
		till_auto(Entities.Pumpkin)
		water_to(water)
		plant(Entities.Pumpkin)
		move_snake()
def farm_pumpkin_check(water=0.75):
	empty=set()
	for i in range(farm_size):
		if get_entity_type() != Entities.Pumpkin:
			empty.add(i)
			water_to(water)
			plant(Entities.Pumpkin)
		move_line()
	return empty
def farm_pumpkin_loop(empty,water=0.75):
	rm = []
	temp = quick_sort(set2list(empty))
	for id in temp:
		move_to(id)
		if can_harvest():
			rm.append(id)
		else:
			water_to(water)
			plant(Entities.Pumpkin)
	for id in rm:
		empty.remove(id)

if __name__ == "__main__":
	# 初始化
	water=-1
	wait_time=6*400
	all_items = [
		Items.Pumpkin,
		Items.Carrot
	]
	clear()
	while check_cost(Entities.Pumpkin,farm_size):
		bp = get_bp()
		move_to(0,0)
		farm_pumpkin_once(water)
		empty=farm_pumpkin_check(water)
		while len(empty) !=0:
			farm_pumpkin_loop(empty,water)
		if get_entity_type() != Entities.Pumpkin and not can_harvest():
			sleep(100)
		sleep(wait_time)
		harvest()
		print_item_change(bp,all_items)