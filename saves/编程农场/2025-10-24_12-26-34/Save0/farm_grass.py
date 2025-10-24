from farm import *


# 测试最低水位
def test_best_water():
	best_water = 1
	water_to(best_water)
	while get_water() >= 0.25 and can_harvest():
		harvest()
		best_water = get_water()
	quick_print("best_water:",best_water)
	return best_water
# 种草
def farm_grass(water=-1):
	till_auto(Entities.Grass)
	water_to(water)
	if can_harvest():
		harvest()
def main():
	# 初始化
	clear()
	till_auto(Entities.Grass)
	best_water = test_best_water()
	# 单区块高速收获草
	while True:
		farm_grass(best_water)

if __name__ == "__main__":
	main()