from farm import *
from utils import find_data, get_list,drone_run,get_pos,split_row,split_col


def farm_cactus_once_part(data,water):
	x1,y1,x2,y2 = data["farm"]
	for i in range(get_size(x1,y1,x2,y2)):
		till_auto(Entities.Cactus)
		water_to(water)
		plant(Entities.Cactus)
		move_step(x1,y1,x2,y2)
def swap_row_part(data,_):
	x1,y1,x2,y2 = data["farm"]
	for y in range(y1,y2+1):
		move_to(x1,y)
		nums = get_list(x2-x1+1)
		for x in range(x2-x1+1):
			nums[x]=measure()
			move(East)
		for x in range(x2-x1,0,-1):
			id = find_data(nums[0:x+1],max(nums[0:x+1]))
			if id != x:
				move_to(id,y)
				swap_to(x,y)
			nums.pop(id)
def swap_col_part(data,_):
	x1,y1,x2,y2 = data["farm"]
	for x in range(x1,x2+1):
		move_to(x,y1)
		nums = get_list(y2-y1+1)
		for y in range(y2-y1+1):
			nums[y]=measure()
			move(North)
		for y in range(y2-y1,0,-1):
			id = find_data(nums[0:y+1],max(nums[0:y+1]))
			if id != y:
				move_to(x,id)
				swap_to(x,y)
			nums.pop(id)
def farm_cactus_part(data,arg):
	loop = arg[0]
	water = arg[1]
	x1,y1,x2,y2 = data["farm"]
	while loop>0:
		loop-=1
		move_to(x1,y1)
# 种仙人掌
def farm_cactus_muti(loop=10,water=0.75):
	move_to(0,0)
	while loop>0:
		loop-=1
		drone_run(farm_cactus_once_part,water)
		drone_run(swap_col_part,None,True,True,split_col)
		drone_run(swap_row_part,None,True,True,split_row)
		move_to(get_world_size()-1,get_world_size()-1)
		while get_entity_type() and not can_harvest():
			pass
		harvest()
def main():
	loop = 10
	water = 0.75
	set_world_size(max_drones())
	clear()
	while check_cost(Entities.Cactus,get_farm_size()*loop):
		farm_cactus_muti(loop,water)

if __name__ == "__main__":
	main()