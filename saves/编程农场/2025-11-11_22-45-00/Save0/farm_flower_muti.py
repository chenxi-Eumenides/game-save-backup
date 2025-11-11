from farm import *
from utils import drone_run,merge_list,find_data,print_data,sum,max_num


def farm_flower_once_part(data,water):
	x1,y1,x2,y2 = data["farm"]
	power_list=[]
	for i in range(get_size(x1,y1,x2,y2)):
		till_auto(Entities.Sunflower)
		water_to(water)
		plant(Entities.Sunflower)
		power_list.append(measure())
		move_step(x1,y1,x2,y2)
	return power_list
def harvest_flower_part(data,power_list):
	for _ in range(data["id"]):
		id = find_data(power_list,max_num(power_list))
		power_list[id]=-1
	id = find_data(power_list,max_num(power_list))
	if power_list[id]==-1:
		return []
	move_to(id)
	while get_entity_type() != None and not can_harvest():
		pass
	remove_id_list = [id]
	if data["last_drone"]:
		remove_id_list += wait_for(data["last_drone"])
	harvest()
	return remove_id_list
# 种花
def farm_flower_muti(loop=10,water=0.75):
	move_to(0,0)
	while loop>0:
		loop-=1
		data = drone_run(farm_flower_once_part,water)
		power_list = []
		for d in data:
			power_list += d
		num = min(get_world_size(),max_drones())
		while sum(power_list) != 0 - get_farm_size():
			data = drone_run(harvest_flower_part,power_list,True,False)
			for id in data[0]:
				power_list[id]=-1
def main():
	loop=10
	water=0.75
	set_world_size(max_drones())
	clear()
	while check_cost(Entities.Sunflower,get_farm_size()*loop):
		farm_flower_muti(loop,water)

if __name__ == "__main__":
	main()
		