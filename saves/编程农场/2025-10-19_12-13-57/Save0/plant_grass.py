from farm import *

def test_best_water():
	# 测试最低水位
	best_water = 1
	water_to(best_water)
	while get_water() >= 0.25 and can_harvest():
		harvest()
		best_water = get_water()
	quick_print("best_water:",best_water)
	return best_water
def farm_grass(best_water):
	water_to(best_water)
	if can_harvest():
		harvest()

if __name__ == "__main__":
	# 初始化
	clear()
	till_auto(Entities.Grass)
	best_water = test_best_water()
	# 单区块高速收获草
	while True:
		farm_grass(best_water)