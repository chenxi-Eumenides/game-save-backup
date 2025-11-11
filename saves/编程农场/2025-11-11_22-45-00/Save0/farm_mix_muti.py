from farm import *
from utils import get_base_farm_dict,drone_run,print_dict
from utils import merge_list,find_data,sum,max_num,hold_on

def plant_test():
	farm_data = dict()
	for y in range(get_world_size()):
		for x in range(get_world_size()):
			farm_data[x,y]={
			"plant":None,
			"parents":dict(),
			"need":None,
			"need_lct":None,
		}
	while True:
		for x,y in farm_data:
			move_to(x,y)
			if farm_data[(x,y)]["plant"] == None:
				farm_data[(x,y)]["plant"] = Entities.Carrot
			p = farm_data[(x,y)]["plant"]
			while not can_harvest() and get_entity_type() != None:
				pass
			harvest()
			for px,py in farm_data[x,y]["parents"]:
				pass
			till_auto(p)
			plant(p)
			water_to()
			companion = get_companion()
			if companion == None:
				target,location = None,None
			else:
				target,location = companion
			if location != None:
				farm_data[location]["plant"] = target
				farm_data[location]["parents"][x,y] = p
			farm_data[(x,y)]["need"] = target
			farm_data[(x,y)]["need_lct"] = location
		#quick_print(x,y,p,"|",target,location)

def main():
	set_world_size(6)
	clear()
	plant_test()
	pet_the_piggy()
	hold_on()

if __name__ == "__main__":
	main()