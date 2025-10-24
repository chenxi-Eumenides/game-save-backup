plants=[Entities.Grass,
	Entities.Bush,
	Entities.Tree,
	Entities.Carrot,
	Entities.Pumpkin,
	Entities.Sunflower,
	Entities.Cactus]
# 获取农场格子数量
def get_farm_size():
	return get_world_size()**2
# 获取格子数量
def get_size(x1=0,y1=0,x2=get_world_size(),y2=get_world_size()):
	return abs(x2-x1+1)*abs(y2-y1+1)
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
# 按行移动一步
def move_step(x1=0,y1=0,x2=get_world_size()-1,y2=get_world_size()-1):
	x=get_pos_x()
	y=get_pos_y()
	max=get_world_size()
	if not (x1<=x<=x2<=max and y1<=y<=y2<=max):
		return False
	if x+1<=x2:
		res = move_to(x+1,y)
	elif y+1<=y2:
		res = move_to(x1,y+1)
	else:
		res = move_to(x1,y1)
	return res
# 蛇形移动一步
def move_snake(x1=0,y1=0,x2=get_world_size()-1,y2=get_world_size()-1):
	x=get_pos_x()
	y=get_pos_y()
	max=get_world_size()
	if not (x1<=x<=x2<=max and y1<=y<=y2<=max):
		return False
	if (y-y1)%2==0:
		if x==x2 and y==y2:
			res = move_to(x1,y1)
		elif x+1<=x2:
			res = move_to(x+1,y)
		else:
			res = move_to(x,y+1)
	else:
		if x==x1 and y==y2:
			res = move_to(x1,y1)
		elif x-1>=x1:
			res = move_to(x-1,y)
		else:
			res = move_to(x,y+1)
	return res
# 移动到指定位置，2个参数为xy坐标，1个参数为id坐标
def move_to(x,y=-1,cross=True):
	max = get_world_size()
	if y < 0:
		id = x
		x = id % max
		y = (id - x) // max
	dx = x-get_pos_x()
	dy = y-get_pos_y()
	half = max//2
	if cross:
		if dx > half:
			dx -= max
		elif dx < - half:
			dx += max
		if dy > half:
			dy -= max
		elif dy < - half:
			dy += max
	if dx > 0:
		for _ in range(dx):
			res = move(East)
			if not res:
				return False
	elif dx < 0:
		for _ in range(-dx):
			res = move(West)
			if not res:
				return False
	if dy > 0:
		for _ in range(dy):
			res = move(North)
			if not res:
				return False
	elif dy < 0:
		for _ in range(-dy):
			res = move(South)
			if not res:
				return False
	return True