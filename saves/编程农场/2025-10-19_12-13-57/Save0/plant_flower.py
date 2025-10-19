from farm import *
from utils import find_data,sleep
from utils import get_bp,print_item_change

def farm_flower(water = 0.75):
	power_list = []
	for i in range(farm_size):
		till_auto(Entities.Sunflower)
		water_to(water)
		plant(Entities.Sunflower)
		power_list.append(measure())
		move_line()
	return power_list
def harvest_flower(power_list):
	for i in range(farm_size):
		id = find_data(power_list,max(power_list))
		move_to(id)
		while get_entity_type() != None and not can_harvest():
			sleep(100)
		harvest()
		power_list[id]=-1

if __name__ == "__main__":
	water = -1
	all_items = [Items.Power,Items.Carrot]
	clear()
	while check_cost(Entities.Sunflower,farm_size):
		bp = get_bp()
		move_to(0,0)
		power_list = farm_flower(water)
		harvest_flower(power_list)
		print_item_change(bp,all_items)