from farm import move_to,till_auto
from utils import get_base_farm_dict,get_pos,lct_id2xy,reverse_list,infinite,get_list
from utils import get_bp, print_item_change,print_dict


def print_map(map):
	lines = get_list()
	for i in range(get_world_size()):
		lines[i] = get_list()
	for x,y in map:
		lines[get_world_size()-y-1][x]=map[(x,y)]["a*"]
	for line in lines:
		quick_print(line)
def distance(x1,y1,x2,y2):
	return abs(x2-x1)+abs(y2-y1)
def get_around(x,y):
	return {(x,y+1),(x,y-1),(x-1,y),(x+1,y)}
def update_around(map,x,y):
	self = map[(x,y)]
	pos = [(x,y+1),(x,y-1),(x-1,y),(x+1,y)]
	res = []
	if pos in map and map[pos] != infinite and map[pos] in [map[(x,y)]+1,map[(x,y)]-1,infinite]:
		res.append(pos)
	return res
def check_move(map,pos=get_pos()):
	return map[pos]["can_move"]
def find_way():
	self = get_pos()
	pos = {
		East:(self[0]+1,self[1]),
		West:(self[0]-1,self[1]),
		North:(self[0],self[1]+1),
		South:(self[0],self[1]-1),
	}
	ways = []
	for d in pos:
		if can_move(d):
			ways.append(pos[d])
	return ways
def update_map(map,target):
	map[target]["a*"]=0
	max_distance=0
	edge = get_world_size()-1
	for i,j in [(0,0),(0,1),(1,1),(1,0)]:
		d = distance(target[0],target[1],edge*i,edge*j)
		max_distance=max(max_distance,d)
	searched = set()
	need_search = {target}
	for i in range(max_distance+1):
		temp = set(need_search)
		need_search = set()
		for pos in temp:
			searched.add(pos)
			wait_search = get_around(pos[0],pos[1])
			for p in wait_search:
				if p in need_search or p in searched:
					continue
				elif 0<=p[0]<get_world_size() and 0<=p[1]<get_world_size():
					if map[p]["a*"] == -1:
						map[p]["a*"] = i+1
					else:
						map[p]["a*"] = min(i+1,map[p]["a*"])
					need_search.add(p)
def create_map(long=get_world_size()):
	data = {
		"item":None, # 物品，默认为None
		"a*":-1, # 到目标的距离，未初始化为-1
		"can_move":[], # 可移动的相邻坐标
		"body":0, # 身体，头为1，非身体为0
 	}
	map = dict()
	for i in range(long):
		for j in range(long):
			map[(i,j)]=dict(data)
	return map
def maze_a_star(map):
	while map[get_pos()]["a*"] != 0:
		ways = find_way()
		new_value = []
		for way in ways:
			new_value.append(map[way]["a*"]+1)
		map[get_pos()]["a*"]=min(new_value)
		for way in ways:
			if map[way]["a*"] < map[get_pos()]["a*"]:
				move_to(way[0],way[1])
				break
	map[get_pos()]["a*"]=-1
def start():
	clear()
	move_to(get_world_size()//2,get_world_size()//2)
	till_auto(Entities.Bush)
	plant(Entities.Bush)
	use_num = get_world_size()*2**(num_unlocked(Unlocks.Mazes)-1)
	use_item(Items.Weird_Substance, use_num)
	return use_num
def next(use_num):
	if get_entity_type() == Entities.Treasure:
		use_item(Items.Weird_Substance, use_num)
def end():
	if get_entity_type() == Entities.Treasure:
		harvest()
def run_maze_max(max_loop=300):
	clear()
	num = start()
	loop = 1
	map = create_map()
	while loop<=max_loop and num_items(Items.Weird_Substance)>num*loop:
		target = measure()
		update_map(map,target)
		maze_a_star(map)
		if loop==max_loop:
			end()
		else:
			next(num)
		loop+=1
def run_maze_once():
	clear()
	start()
	maze_a_star()
def main():
	set_world_size(8)
	while True:
		bp = get_bp()
		run_maze_max()
		print_item_change(bp)

if __name__ == "__main__":
	main()