from farm import *
from utils import lct_id2xy, quick_sort, set2list,drone_run


def split_func(id,_):
	max = get_world_size()
	n = (max+1)//7
	if id >= n**2:
		return (None,None,None,None)
	dx = id%n
	dy = id//n
	return dx*7,dy*7,dx*7+5,dy*7+5

def farm_pumpkin_once(x1,y1,x2,y2,water):
	for i in range(get_size(x1,y1,x2,y2)):
		till_auto(Entities.Pumpkin)
		water_to(water)
		plant(Entities.Pumpkin)
		move_snake(x1,y1,x2,y2)
def farm_pumpkin_check(empty,x1,y1,x2,y2,water):
	for i in range(get_size(x1,y1,x2,y2)):
		if get_entity_type() == Entities.Dead_Pumpkin:
			empty.add(i)
			water_to(water)
			plant(Entities.Pumpkin)
		elif get_entity_type() == Entities.Pumpkin and not can_harvest():
			empty.add(i)
			water_to(water)
		move_step(x1,y1,x2,y2)
	return empty
def farm_pumpkin_recheck(empty,x1,y1,x2,y2,water):
	rm = []
	temp = quick_sort(set2list(empty))
	for id in temp:
		x,y = lct_id2xy(id,x2-x1+1)
		move_to(x1+x,y1+y)
		if can_harvest() and get_entity_type() == Entities.Pumpkin:
			rm.append(id)
		elif get_entity_type() == Entities.Dead_Pumpkin:
			water_to(water)	
			plant(Entities.Pumpkin)
	for id in rm:
		empty.remove(id)
# 种南瓜
def farm_pumpkin_part(data,arg):
	loop = arg[0]
	water = arg[1]
	x1,y1,x2,y2 = data["farm"]
	while loop>0:
		loop-=1
		move_to(x1,y1)
		farm_pumpkin_once(x1,y1,x2,y2,water)
		empty=set()
		farm_pumpkin_check(empty,x1,y1,x2,y2,water)
		while len(empty) !=0 and check_cost(Entities.Pumpkin,get_farm_size()):
			farm_pumpkin_recheck(empty,x1,y1,x2,y2,water)
		harvest()
def farm_pumpkin_muti(loop=10,water=0.75):
	drone_run(farm_pumpkin_part,[loop,water],True,True,split_func)
def main():
	loop=1
	water=0.75
	set_world_size(-1)
	clear()
	while check_cost(Entities.Pumpkin,get_farm_size()*loop):
		farm_pumpkin_muti(loop,water)

if __name__ == "__main__":
	main()