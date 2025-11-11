from farm import *
from utils import find_data, get_bp, print_item_change


def farm_flower_once(power_list,water = 0.75):
	for i in range(get_farm_size()):
		till_auto(Entities.Sunflower)
		water_to(water)
		plant(Entities.Sunflower)
		power_list.append(measure())
		move_step()
	return power_list
def harvest_flower(power_list):
	for i in range(get_farm_size()):
		id = find_data(power_list,max(power_list))
		move_to(id)
		while get_entity_type() != None and not can_harvest():
			pass
		harvest()
		power_list[id]=-1
# 种花
def farm_flower(water=-1):
	move_to(0,0)
	power_list = []
	farm_flower_once(power_list,water)
	harvest_flower(power_list)
def main():
	water = -1
	all_items = [
		Items.Power,
		Items.Carrot
	]
	set_world_size(10)
	clear()
	while check_cost(Entities.Sunflower,get_farm_size()):
		bp = get_bp()
		farm_flower(water)
		print_item_change(bp,all_items)

if __name__ == "__main__":
	main()