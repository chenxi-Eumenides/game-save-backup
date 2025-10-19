from farm import *
from utils import find_data,sleep,get_empty_list
from utils import get_bp,print_item_change

def farm_cactus(water=0.75):
	types = []
	for i in range(farm_size):
		till_auto(Entities.Cactus)
		water_to(water)
		plant(Entities.Cactus)
		types.append(measure())
		move_line()
	return types
def swap_row():
	for y in range(get_world_size()):
		move_to(0,y)
		nums = get_empty_list()
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
		nums = get_empty_list()
		for y in range(get_world_size()):
			nums[y]=measure()
			move(North)
		for y in range(get_world_size()-1,0,-1):
			id = find_data(nums[0:y+1],max(nums[0:y+1]))
			if id != y:
				move_to(x,id)
				swap_to(x,y)
			nums.pop(id)

if __name__ == "__main__":
	water = -1
	clear()
	while check_cost(Entities.Cactus,farm_size):
		bp = get_bp()
		move_to(0,0)
		farm_cactus(water)
		swap_row()
		swap_col()
		move_to(get_world_size()-1,get_world_size()-1)
		while get_entity_type() and not can_harvest():
			sleep(100)
		harvest()
		print_item_change(bp,[Items.Cactus])