from farm import *
from utils import drone_run


# 
def farm_carrot_part(data,arg):
	loop = arg[0]
	water = arg[1]
	x1,y1,x2,y2 = data["farm"]
	while loop>0:
		loop-=1
		move_to(x1,y1)
		for _ in range(get_size(x1,y1,x2,y2)):
			farm_carrot_once(water)
			move_snake(x1,y1,x2,y2)
# 种一次
def farm_carrot_once(water):
	if can_harvest():
		harvest()
	till_auto(Entities.Carrot)
	water_to(water)
	plant(Entities.Carrot)
def farm_carrot_muti(loop=10,water=0.75):
	drone_run(farm_carrot_part,[loop,water])
def main():
	loop = 10
	water = 0.75
	set_world_size(max_drones())
	clear()
	while check_cost(Entities.Carrot,get_farm_size()*loop):
		farm_carrot_muti(loop,water)

if __name__ == "__main__":
	main()
		