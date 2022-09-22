import pygame
import random
import math
pygame.init()

# setup a class and then put these values as global
class DrawInformation:
	BLACK = 0, 0, 0
	WHITE = 255, 255, 255
	GREEN = 0, 255, 0
	RED = 255, 0, 0
	BACKGROUND_COLOR = WHITE
    # set a bunch of colors and the background color.
    
	GRADIENTS = [
		(128, 128, 128),
		(160, 160, 160),
		(192, 192, 192)
	] # this gradient has the variations of grey

	FONT = pygame.font.SysFont('comicsans', 20) # for fonts, pass a font type and font size
	LARGE_FONT = pygame.font.SysFont('comicsans', 30) # for large font

	SIDE_PAD = 100 # this is for a padding of 100pixels from the left and the right hand side
	TOP_PAD = 150 
 
    # initialization we pass the list that we want to sort.
	def __init__(self, width, height, lst):
		self.width = width
		self.height = height
        # while working with pygame we need to setup a screen or a window.
		self.window = pygame.display.set_mode((width, height)) # create awindow with the height and width
		pygame.display.set_caption("Sorting Algorithm Visualization") # set a caption for the window
		self.set_list(lst) # a method is called that is set_list which is defined below

	def set_list(self, lst):
		self.lst = lst
		self.min_val = min(lst) # gives the minimum in the list
		self.max_val = max(lst) # gives the maximum in the list
        # Now , calculate the width of the bars
		self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        # here block_width is the (width_of_the_screen- side_pad(100) )/len(list) ; len(list) is number of elements
		self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        # this is to get height of one unit of a block. here its floor and not round because in round we get values that are larger that what we need so we use floor.
		self.start_x = self.SIDE_PAD // 2
        # the coordinates in pygames is like the top left corner is x=y=0; as we go downwards y increases and as we go sideways x increases
        


def draw(draw_info, algo_name, ascending):
	draw_info.window.fill(draw_info.BACKGROUND_COLOR)

	title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.RED)
	draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

	controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
	draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))
    # in order to draw we need to draw a window and blit, we pass the controls ie the surface we want to blit and then set x and y coordinates
    # for x coordinate the math is the main_width/2 (or window width) - the controls_width/2
	sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 75))

	draw_list(draw_info)
	pygame.display.update()

#  draw_list is to draw the list in the window
def draw_list(draw_info, color_positions={}, clear_bg=False):
	lst = draw_info.lst 

	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
						draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

	for i, val in enumerate(lst): #enumerate gives the index and value of every single element in the list
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

		color = draw_info.GRADIENTS[i % 3] #we'll have three color gradients.

		if i in color_positions:
			color = color_positions[i] 
        #draw rectangle , pass the screen where we want to draw this (window), pass the color, then pass the rectangle ehich is going to be (x,y,block_width and the height/block_height)
		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

	if clear_bg:
		pygame.display.update()

# a function that generates the starting list. We need a starting list to actualy sort. takes n-number of elements
def generate_starting_list(n, min_val, max_val):
	lst = []

	for _ in range(n):
		val = random.randint(min_val, max_val) # here random.randint will generate random values that are inclusive of min and max vals
		lst.append(val)

	return lst

# below is the logic of bubble sort
def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
				# this above represents the draw list and pass draw info and then passcolor positions( ie: j will corespond to color green
    			# and j+1 will correspond to color red ) ,Inorder to see the updates in the background we use True.
				yield True 

	return lst

def insertion_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(1, len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			lst[i] = lst[i - 1]
			i = i - 1
			lst[i] = current
			draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
			yield True # we are yeilding true because we are doing a swap & everytime we are doing a swap we are yeilding true.

	return lst


def main():
	run = True
	clock = pygame.time.Clock()

	n = 50
	min_val = 0
	max_val = 100

	lst = generate_starting_list(n, min_val, max_val)
	draw_info = DrawInformation(700, 700, lst) # this creates a list with the height width and the list
	sorting = False
	ascending = True

	sorting_algorithm = bubble_sort
	sorting_algo_name = "Bubble Sort"
	sorting_algorithm_generator = None

	while run:
		clock.tick(60)
		# if we are sorting then try to call the next method . if this doesnt work or the generator is done then we raise the stop iteration method
		if sorting:
			try:
				next(sorting_algorithm_generator)
			except StopIteration:
				sorting = False
		else: #we call the draw fubction and pass the sorting algo name and ascending
			draw(draw_info, sorting_algo_name, ascending)

		for event in pygame.event.get():
			if event.type == pygame.QUIT: # this is the Close button which is used to quit.
				run = False
            # for not pressing any keydown we are going to continue.
			if event.type != pygame.KEYDOWN:
				continue
            # this is if key r is pressed, then we will reset the list. Make sure we write'event.type ' to understand the type of the event
			if event.key == pygame.K_r:
				lst = generate_starting_list(n, min_val, max_val)
				draw_info.set_list(lst)
				sorting = False
			elif event.key == pygame.K_SPACE and sorting == False: #if key is space then sorting starts and "sorting==false" means we cant sort if its already sorted
				sorting = True
				sorting_algorithm_generator = sorting_algorithm(draw_info, ascending) #generator object
			elif event.key == pygame.K_a and not sorting: #a for ascending
				ascending = True
			elif event.key == pygame.K_d and not sorting: #d for descending
				ascending = False
			elif event.key == pygame.K_i and not sorting:
				sorting_algorithm = insertion_sort
				sorting_algo_name = "Insertion Sort"
			elif event.key == pygame.K_b and not sorting:
				sorting_algorithm = bubble_sort
				sorting_algo_name = "Bubble Sort"


	pygame.quit()

# below line is to ensure we are running this module.
if __name__ == "__main__":
	main()