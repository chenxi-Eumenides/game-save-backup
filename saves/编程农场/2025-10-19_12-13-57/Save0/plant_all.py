from farm import *
from utils import get_bp,print_item_change

def prepare_farm():
	for i in range(farm_size):
		till_auto(plants[plants_id[i]])
		water_to(water)
		move_line()
def farm_all():
	for i in range(farm_size):
		if can_harvest():
			harvest()
		water_to(water)
		plant(plants[plants_id[i]])
		move_line()

if __name__ == "__main__":
	# 初始化
	plants_id = create_plant_id_list()
	water = 0.5
	all_items = [
		Items.Hay,
		Items.Wood,
		Items.Carrot,
		Items.Pumpkin,
		Items.Power
	]
	# 清理块
	clear()
	prepare_farm()
	while True:
		bp = get_bp()
		farm_all()
		print_item_change(bp,all_items)