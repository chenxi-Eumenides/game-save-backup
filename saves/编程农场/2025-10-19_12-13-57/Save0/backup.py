def is_pumpkin(x,y):
	return x<pn and y<pn
def is_tree(x,y):
	return x%2==y%2 and y<pn
def is_buch(x,y):
	return x%2==y%2 and y>=pn
def is_carrot(x,y):
	return y>=pn and y<get_world_size()-1 and x<get_world_size()-pn
def is_flower(x,y):
	return y>=pn and y<get_world_size()-1 and x>=get_world_size()-pn
def is_grass(x,y):
	return y==get_world_size()-1