from farm import *
from utils import get_bp, lct_id2xy, print_item_change, quick_sort, set2list, sleep


def farm_pumpkin_once(water=0.75):
	for i in range(get_farm_size()):
		till_auto(Entities.Pumpkin)
		water_to(water)
		plant(Entities.Pumpkin)
		move_snake()
def farm_pumpkin_check(empty,water=0.75):
	for i in range(get_farm_size()):
		# 等南瓜成熟或枯萎
		#while get_entity_type() == Entities.Pumpkin and not can_harvest():
		#	pass
		if get_entity_type() == Entities.Dead_Pumpkin:
			empty.add(i)
			water_to(water)
			plant(Entities.Pumpkin)
		elif get_entity_type() == Entities.Pumpkin and not can_harvest():
			empty.add(i)
			water_to(water)
		move_step()
	return empty
def farm_pumpkin_recheck(empty,water=0.75):
	rm = []
	temp = quick_sort(set2list(empty))
	for id in temp:
		move_to(id)
		if can_harvest() and get_entity_type() == Entities.Pumpkin:
			rm.append(id)
		elif get_entity_type() == Entities.Dead_Pumpkin:
			water_to(water)	
			plant(Entities.Pumpkin)
	for id in rm:
		empty.remove(id)
# 种南瓜
def farm_pumpkin(water=-1):
	move_to(0,0)
	farm_pumpkin_once(water)
	empty=set()
	farm_pumpkin_check(empty,water)
	while len(empty) !=0 and check_cost(Entities.Pumpkin,get_farm_size()):
		farm_pumpkin_recheck(empty,water)
	harvest()
def main():
	# 初始化
	water=-1
	all_items = [
		Items.Pumpkin,
		Items.Carrot
	]
	set_world_size(6)
	clear()
	while check_cost(Entities.Pumpkin,get_farm_size()):
		bp = get_bp()
		farm_pumpkin(water)
		print_item_change(bp,all_items)

if __name__ == "__main__":
	main()