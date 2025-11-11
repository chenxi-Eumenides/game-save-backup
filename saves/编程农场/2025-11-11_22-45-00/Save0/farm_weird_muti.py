from farm import *
from utils import drone_run


def split(id,_):
	return id,0,id,0
def farm_weird_once(water):
	till_auto(Entities.Grass)
	water_to(water)
	use_item(Items.Fertilizer)
	if can_harvest():
		harvest()
def farm_weird_part(data,arg):
	loop = arg[0]
	water = arg[1]
	x1,y1,x2,y2 = data["farm"]
	while loop>0:
		loop-=1
		move_to(x1,y1)
		farm_weird_once(water)
def farm_weird_muti(loop=10,water=0.95):
	drone_run(farm_weird_part,[loop,water],True,True,split)
def main():
	water=0.95
	loop=1000
	set_world_size(max_drones())
	clear()
	while num_items(Items.Fertilizer)>get_world_size()*loop:
		farm_weird_muti(loop,water)

if __name__ == "__main__":
	main()
	