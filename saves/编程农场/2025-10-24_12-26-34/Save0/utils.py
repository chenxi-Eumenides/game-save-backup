from farm import move_to
# 以默认属性测试文件
def test_file(sim_file="test",sim_speed=1):
	sim_items = dict()
	for item in Items:	
		sim_items[item]=1000000
	sim_globals = {
		"sim_status" : True
	}
	sim_unlocks = Unlocks
	sim_seed = -1
	
	run_time = simulate(sim_file,sim_unlocks,sim_items,sim_globals,sim_seed,sim_speed)
	return run_time
# 多无人机执行。
# f的第一个参数必须是drone_data
# drone_data={id:int,farm:(x1,y1,x2,y2),last_drone:drone}
# f必须要有第2个参数为传参，只能有1个
# split有两个参数，第一个为序号，第二个为最大序号
def drone_run(f,arg=None,self=True,wait=True,split=split_row):
	drones = []
	result = []
	res = None
	drone_num = max_drones()
	if not self:
		drone_num-=1
	for i in range(drone_num):
		x1,y1,x2,y2 = split(i,drone_num)
		if x1 == None:
			if num_drones()<max_drones():
				self = False
			continue
		drone_data = {
			"id": i,
			"farm": (x1,y1,x2,y2),
			"last_drone": None,
			"self":False
		}
		if len(drones) != 0:
			drone_data["last_drone"] = drones[-1]
		def drone_func():
			return f(drone_data,arg)
		move_to(x1,y1)
		if i < drone_num-1:
			new_drone = spawn_drone(drone_func)
			drones.append(new_drone)
		elif self:
			drone_data["self"]=True
			res = f(drone_data,arg)
	if wait:
		if self:
			num = num_drones()
		else:
			num = num_drones()-1
		for i in range(num):
			data = wait_for(drones[i])
			result.append(data)
	if self:
		result.append(res)
	return result
# 根据序号给出分割区域，横着
def split_row(id,all=max_drones()):
	if get_world_size()>all:
		n = get_world_size()/all//1
	else:
		n = 1
		all = get_world_size()
	a = get_world_size()-n*all
	x1=0
	x2=get_world_size()-1
	if a-id>0:
		y1=id*n+id
		y2=y1+(n-1)+1
	else:
		y1=id*n+a
		y2=y1+(n-1)
	return x1,y1,x2,y2
# 根据序号给出分割区域，竖着
def split_col(id,all=max_drones()):
	if get_world_size()>=all:
		n = get_world_size()/all//1
	else:
		n = 1
		all = get_world_size()
	a = get_world_size()-n*all
	y1=0
	y2=get_world_size()-1
	if a-id>0:
		x1=id*n+id
		x2=x1+(n-1)+1
	else:
		x1=id*n+a
		x2=x1+(n-1)
	return x1,y1,x2,y2
# 获取当前坐标
def get_pos():
	return get_pos_x(),get_pos_y()
# 等待
def hold_on():
	while True:
		pass
# 获取背包物品的数量
def get_bp():
	my_items=dict()
	for item in Items:
		my_items[item] = num_items(item)
	return my_items
# 获取背包物品的更改
def get_bp_change(d):
	changed=dict()
	for item in Items:
		if d[item] != num_items(item):
			changed[item] = num_items(item) - d[item]
	return changed
# 打印目标物品的变化
# history_item : 需要比较的物品数量字典
# item_list : 需要显示的物品列表
def print_item_change(history_item=dict(),item_list=list()):
	changed=dict()
	for item in Items:
		if history_item[item] != num_items(item):
			changed[item] = num_items(item) - history_item[item]
	all = False
	if len(item_list) < 1:
		all = True
	quick_print("物品变化:")
	for item in changed:
		if all:
			quick_print("  ",trans_zh[item],":",changed[item])
		elif item in item_list:
			quick_print("  ",trans_zh[item],":",changed[item])
	if len(changed) == 0:
		quick_print("  ","无")
	return True
# 获取列表
def get_list(long=get_world_size(),data=None):
	l=list()
	for _ in range(long):
		l.append(data)
	return l
# 获取基本农田列表
def get_base_farm_list(data=None):
	return get_list(get_world_size()**2,data)
# 获取空农田字典
def get_base_farm_dict(data=None):
	d=dict()
	max=get_world_size()
	for y in range(max):
		for x in range(max):
			d[x,y]=data
	return d
# 将坐标id转为坐标xz
def lct_id2xy(id=0,size=get_world_size()):
	x = id % size
	y = (id - x) // size
	return (x,y)
# 将坐标xy转为坐标id
def lct_xy2id(x=0,y=0,size=get_world_size()):
	id = y * size + x
	return id
# 将set转为list
def set2list(s):
	l=[]
	for i in s:
		l.append(i)
	return l
# 将list转为set
def list2set(l):
	s=set()
	for i in l:
		s.add(i)
	return s
# 获取搜索值的位置
def find_data(l,v):
	for i in range(len(l)):
		if l[i] == v:
			return i
	return -1
# 快速排序
def quick_sort(arr):
	if len(arr) <= 1:
		return arr
	pivot = arr[len(arr) // 2]
	left = []
	middle = []
	right = []
	for x in arr:
		if x < pivot:
			left.append(x)
		elif x > pivot:
			right.append(x)
		else:
			middle.append(x)
	result = quick_sort(left) + middle + quick_sort(right)
	return result
# 反转列表
def reverse_list(l):
	temp = l[len(l):0:-1]
	temp.append(l[0])
	return temp
# 延迟指定ticks，受加速升级影响
def sleep(t):
	t-=4
	pass
	while t>0:
		t-=2
# 延迟指定秒数
def sleep_sec(t):
	while t>0:
		t-=1
		do_a_flip()
# 返回自身坐标
def lct():
	return get_pos_x(),get_pos_y()
# 将整个田的数据列表打印成容易对照，容易看懂的形式
def print_data(l):
	max = get_world_size()
	lines=[]
	line=""
	for i in range(max**2):
		line=line+str(l[i])
		line+=" "
		if i%max==max-1:
			lines.append(line)
			line=""
	for line in reverse_list(lines):
		quick_print(line)
# 将整个田的数据字典打印成容易对照，容易看懂的形式
def print_dict(d):
	max = get_world_size()
	lines=[]
	line=""
	for i in range(max**2):
		line=line+str(d[lct_id2xy(i)])
		line+=" "
		if i%max==max-1:
			lines.append(line)
			line=""
	for line in reverse_list(lines):
		quick_print(line)
# 合并数据
def merge_list(lists,long=get_world_size()):
	res = []
	for i in range(len(lists[0])):
		for j in range(len(lists)):
			res.append(lists[j][i])
	return res
# 格式化数字
def format_num(num):
	c = ["","k","m","b"]
	res = ""
	for i in range(len(c)):
		if num < 1000**(i+1):
			res = str(num*100//1000**i/100) + c[i]
			return res
	res = str(num*100//1000**i/100) + c[i]
	return res
infinite=999999999
trans_zh={
	Entities.Apple:"苹果",
	Entities.Bush:"灌木丛",
	Entities.Cactus:"仙人掌",
	Entities.Carrot:"胡萝卜",
	Entities.Dinosaur:"骨龙",
	Entities.Grass:"草丛",
	Entities.Hedge:"x",
	Entities.Pumpkin:"南瓜",
	Entities.Dead_Pumpkin:"枯萎的南瓜",
	Entities.Sunflower:"太阳花",
	Entities.Treasure:"宝藏",
	Entities.Tree:"树木",
	Items.Hay:"干草",
	Items.Wood:"木头",
	Items.Carrot:"胡萝卜",
	Items.Pumpkin:"南瓜",
	Items.Cactus:"仙人掌",
	Items.Bone:"骨头",
	Items.Weird_Substance:"奇怪物质",
	Items.Gold:"黄金",
	Items.Water:"水桶",
	Items.Fertilizer:"肥料",
	Items.Power:"能量",
	Grounds.Grassland:"草地",
	Grounds.Soil:"耕地",
	North:"上方",
	East:"右侧",
	West:"左侧",
	South:"下方",
	Hats.Dinosaur_Hat:"骨龙帽",
	Hats.Straw_Hat:"农夫帽"
}