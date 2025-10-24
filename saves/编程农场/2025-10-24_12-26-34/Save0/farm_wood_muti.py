from farm import *
from utils import drone_run


# 
def farm_tree_buch_muti(data,arg):
	loop = arg[0]
	water = arg[1]
	x1,y1,x2,y2 = data["farm"]
	while loop>0:
		loop-=1
		move_to(x1,y1)
		for _ in range(get_size(x1,y1,x2,y2)):
			farm_tree_buch(water)
			move_snake(x1,y1,x2,y2)
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
def farm_wood_muti(loop=10,water=0.75):
	drone_run(farm_tree_buch_muti,[loop,water])
def main():
	loop = 10
	water = 0.75
	set_world_size(max_drones())
	clear()
	while check_cost(Entities.Tree,get_farm_size()*loop):
		farm_wood_muti(loop,water)

if __name__ == "__main__":
	main()
		