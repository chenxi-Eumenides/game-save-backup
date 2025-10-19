from farm import *
from utils import *

if __name__ == "__main__":
	while True:
		clear()
		change_hat(Hats.Dinosaur_Hat)
		
		next_x,next_y = measure()
		res = move_to(next_x,next_y,False)
		while res:
			next_x,next_y = measure()
			res = move_to(next_x,next_y,False)