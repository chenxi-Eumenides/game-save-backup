from farm import *
from utils import get_bp, print_item_change,trans_zh,format_num

from farm_grass_muti import farm_grass_muti
from farm_wood_muti import farm_wood_muti
from farm_carrot_muti import farm_carrot_muti
from farm_pumpkin_muti import farm_pumpkin_muti
from farm_cactus_muti import farm_cactus_muti
from farm_flower_muti import farm_flower_muti
from farm_weird_muti import farm_weird_muti
from farm_bone import farm_bone_stupid
from maze import run_maze_max


# item:[func,size,loop,water]
func_data = {
	Items.Hay:[farm_grass_muti,max_drones(),10000,0.95],
	Items.Wood:[farm_wood_muti,max_drones(),10,0.75],
	Items.Carrot:[farm_carrot_muti,max_drones(),10,0.75],
	Items.Pumpkin:[farm_pumpkin_muti,-1,10,0.75],
	Items.Cactus:[farm_cactus_muti,max_drones(),1,0.75],
	Items.Bone:[farm_bone_stupid,6,None,None],
	Items.Weird_Substance:[farm_weird_muti,max_drones(),10000,0.95],
	Items.Gold:[run_maze_max,4,100,None],
	Items.Power:[farm_flower_muti,max_drones()//2,1,0.75],
}
# item:[num_multiple,need_plant,num]
item_data = {
	Items.Hay:[10,Entities.Grass,],
	Items.Wood:[10,Entities.Tree,],
	Items.Carrot:[4,Entities.Carrot,],
	Items.Pumpkin:[4,Entities.Pumpkin,],
	Items.Cactus:[2,Entities.Cactus,],
	#Items.Bone:[1,Entities.Apple,],
	Items.Weird_Substance:[0.1,Entities.Grass,],
	Items.Gold:[0.2,Entities.Grass,],
	Items.Power:[-1,Entities.Sunflower,10000],
}
bp_data = dict()

def get_target():
	global bp_data
	for item in Items:
		bp_data[item]=num_items(item)
	target = None
	base_num = 1024
	while target == None:
		for item in item_data:
			if item_data[item][0] == -1 and bp_data[item] < item_data[item][2]:
				return item,item_data[item][2]
			elif bp_data[item] < base_num * item_data[item][0]:
				target = item
				return target,base_num * item_data[target][0]
		base_num = base_num*2
	return Items.Power,1000
def run_func(target_data):
	target = target_data[0]
	target_num = target_data[1]
	data = func_data[target]
	func = data[0]
	size = data[1]
	loop = data[2]
	water = data[3]
	set_world_size(size)
	clear()
	while num_items(target) < target_num and check_cost(item_data[target][1],get_farm_size()):
		if loop != None and water == None:
			func(loop)
		elif loop == None and water != None:
			func(water)
		elif loop != None and water != None:
			func(loop,water)
		else:
			func()

def main():
	while True:
		bp = get_bp()
		clear()
		target,target_num = get_target()
		quick_print("当前目标:",trans_zh[target],"->",format_num(target_num))
		run_func([target,target_num])
		print_item_change(bp)

if __name__ == "__main__":
	main()
