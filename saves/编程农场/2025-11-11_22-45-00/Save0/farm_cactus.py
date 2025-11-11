from farm import *
from utils import find_data, get_bp, get_list, print_item_change, sleep


def farm_cactus_once(water=0.75):
	types = []
	for i in range(get_farm_size()):
		till_auto(Entities.Cactus)
		water_to(water)
		plant(Entities.Cactus)
		types.append(measure())
		move_step()
	return types
def swap_row():
	for y in range(get_world_size()):
		move_to(0,y)
		nums = get_list()
		for x in range(get_world_size()):
			nums[x]=measure()
			move(East)
		for x in range(get_world_size()-1,0,-1):
			id = find_data(nums[0:x+1],max(nums[0:x+1]))
			if id != x:
				move_to(id,y)
				swap_to(x,y)
			nums.pop(id)
def swap_col():
	for x in range(get_world_size()):
		move_to(x,0)
		nums = get_list()
		for y in range(get_world_size()):
			nums[y]=measure()
			move(North)
		for y in range(get_world_size()-1,0,-1):
			id = find_data(nums[0:y+1],max(nums[0:y+1]))
			if id != y:
				move_to(x,id)
				swap_to(x,y)
			nums.pop(id)
# 种仙人掌
def farm_cactus(water=-1):
	move_to(0,0)
	farm_cactus_once(water)
	swap_row()
	swap_col()
	move_to(get_world_size()-1,get_world_size()-1)
	while get_entity_type() and not can_harvest():
		sleep(100)
	harvest()
	
def main():
	water = -1
	all_items = [
		Items.Cactus,
		Items.Pumpkin,
	]
	set_world_size(10)
	clear()
	while check_cost(Entities.Cactus,get_farm_size()):
		bp = get_bp()
		farm_cactus(water)
		print_item_change(bp,all_items)

if __name__ == "__main__":
	main()