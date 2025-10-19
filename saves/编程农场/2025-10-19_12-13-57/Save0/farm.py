plants=[Entities.Grass,
	Entities.Bush,
	Entities.Tree,
	Entities.Carrot,
	Entities.Pumpkin,
	Entities.Sunflower,
	Entities.Cactus]
farm_size=get_world_size()**2
# 创建一个混合种植的植物列表
def create_plant_id_list():
	temp_list = [] # 0g,1b,2t,3c,4p,5f
	pn = 2
	s = get_world_size()
	for i in range(s**2):
		y = i//s
		x = i%s
		# g,g,g,g,g
		# c,c,c,f,f
		# c,c,c,f,f
		# p,p,b,t,b
		# p,p,t,b,t
		if x<pn and y<pn:
			temp_list.append(4) # pumpkin
		elif x%2==y%2 and y<pn:
			temp_list.append(2) # tree
		elif x%2!=y%2 and y<pn:
			temp_list.append(1) # buch
		elif y>=pn and y<s-2 and x<s-pn-1:
		#elif y>=pn and y<get_world_size()-2:
			temp_list.append(3) # carrot
		elif y>=pn and y<s-2 and x>=s-pn-1:
			temp_list.append(5) # flower
		elif y>=s-2:
			temp_list.append(0) # grass
		else:
			temp_list.append(0) # grass
	return temp_list
# 浇水到指定水位以上
def water_to(level=0.75):
	for _ in range((level-get_water())//0.25+1):
		use_item(Items.Water)
# 检查库存
def check_cost(plant,n=1):
	cost = get_cost(plant)
	m=999999999
	for item in cost:
		if num_items(item) < cost[item]*n:
			quick_print(item, num_items(item), cost[item]*n)
			return 0
		else:
			temp = num_items(item) // (cost[item]*n)
			m = min(m, temp)
	return m
# 根据植物类型自动犁地
def till_auto(plant):
	grass = [Entities.Grass,Entities.Bush,Entities.Tree]
	if plant in grass and get_ground_type() != Grounds.Grassland:
		till()
	elif plant not in grass and get_ground_type() != Grounds.Soil:
		till()
# 移动到指定位置，2个参数为xy坐标，1个参数为id坐标
def swap_to(x,y=-1):
	max = get_world_size()
	if y < 0:
		id = x
		x = id % max
		y = (id - x) // max
	dx = x-get_pos_x()
	dy = y-get_pos_y()
	if dx > 0:
		for _ in range(dx):
			swap(East)
			move(East)
	elif dx < 0:
		for _ in range(-dx):
			swap(West)
			move(West)
	if dy > 0:
		for _ in range(dy):
			swap(North)
			move(North)
	elif dy < 0:
		for _ in range(-dy):
			swap(South)
			move(South)
# 移动到指定位置，2个参数为xy坐标，1个参数为id坐标
def move_to(x,y=-1,cross=True):
	max = get_world_size()
	if y < 0:
		id = x
		x = id % max
		y = (id - x) // max
	mx = x-get_pos_x()
	my = y-get_pos_y()
	half = max//2
	if cross:
		if mx > half:
			mx -= max
		elif mx < - half:
			mx += max
		if my > half:
			my -= max
		elif my < - half:
			my += max
	if mx > 0:
		for _ in range(mx):
			res = move(East)
			if not res:
				return False
	elif mx < 0:
		for _ in range(-mx):
			res = move(West)
			if not res:
				return False
	if my > 0:
		for _ in range(my):
			res = move(North)
			if not res:
				return False
	elif my < 0:
		for _ in range(-my):
			res = move(South)
			if not res:
				return False
	return True
# 蛇形移动一步
def move_snake():
	x=get_pos_x()
	y=get_pos_y()
	max=get_world_size()
	if x==0 and y==max-1 and y%2!=0:
		move(North)
	elif x==max-1 and y==max-1 and y%2==0:
		move(North)
		move(East)
	elif (x==max-1 and y%2==0) or (x==0 and y%2!=0):
		move(North)
	elif y%2==0:
		move(East)
	else:
		move(West)
# 按行移动一步
def move_line():
	x=get_pos_x()
	y=get_pos_y()
	max=get_world_size()
	if x==max-1:
		move(North)
		move(East)
	else:
		move(East)