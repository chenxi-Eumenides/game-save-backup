from farm import *
from utils import *


# 检查是否位于指定位置
def check_pos(x,y):
	if x==get_pos_x() and y==get_pos_y():
		return True
	else:
		return False
# 需要农场大小为偶数
def farm_bone_stupid():
	clear()
	change_hat(Hats.Dinosaur_Hat)
	max=get_world_size()
	if max%2!=0:
		return False
	apples = 0
	next_x,next_y = measure()
	while True:
		for _ in range(get_farm_size()):
			x=get_pos_x()
			y=get_pos_y()
			if max%2==0 and x==1 and y==max-1:
				code = move(West)
			elif x==0 and y==0:
				code = move(East)
			elif x!=0 and x!=max-1 and y%2==0:
				code = move(East)
			elif x==max-1 and y%2==0:
				code = move(North)
			elif x>1 and y%2==1:
				code = move(West)
			elif x==1 and y%2==1:
				code = move(North)
			elif x==0 and y!=0:
				code = move(South)
			if not code:
				return False
			if get_pos_x()==next_x and get_pos_y()==next_y:
				apples += 1
				if apples == get_farm_size()-1:
					return True
				while measure() == None:
					pass
				next_x,next_y = measure()
# 玩一局贪吃蛇来收获骨头
def farm_bone():
	clear()
	change_hat(Hats.Dinosaur_Hat)
	game_status = True
	game_result = True
	while game_status:
		next_x,next_y = measure()
		game_result = move_to(next_x,next_y,False)
		game_status = game_result
	return game_result
def main():
	set_world_size(8)
	while check_cost(Entities.Apple,get_farm_size()):
		farm_bone_stupid()

if __name__ == "__main__":
	main()