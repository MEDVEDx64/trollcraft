from random import randint
from blocks import *

GRID_SIZE = 32

class World(object):
	def __init__(self, camera, image_db):
		self.the_map = []
		self.images = image_db
		self.camera = camera
		self.generate()

	def initialize_map(self, w, h):
		for i in range(w):
			c = []
			for i in range(h):
				c.append(None)
			self.the_map.append(c)

	def gen_layer(self, block_class = SolidBlock, block_args = ['stone'], height = 60, scale = 5):
		cur_scale = scale/2
		h = height
		if height < scale:
			h = scale
		elif height > len(self.the_map[0]) - scale:
			h = len(self.the_map[0]) - scale

		step_len = 4
		step_tick = 0

		try:
			for c in self.the_map:
				for y in range(len(c)-(h-cur_scale), len(c)):
					while c[y] == None:
						c[y] = block_class(*block_args)
				step_tick += 1
				if step_tick >= step_len:
					step_tick = 0
					step_len = randint(2, 8)
					if(randint(0, 10) > 5):
						if cur_scale < scale:
							cur_scale += 1
						else:
							cur_scale -= 2
					else:
						if cur_scale > 0:
							cur_scale -= 1
						else:
							cur_scale += 3

		except IndexError:
			print("""Lololo! Shi*t happened! The world the_map is uninitialized,
				or there were very much invalid input values.""")

	def generate(self, w = 240, h = 180):
		self.the_map = []
		self.initialize_map(w, h)
		self.gen_layer(SolidBlock, ['adminium', 100500], height = 7, scale = 3)
		self.gen_layer(SolidBlock, ['stone', 38])
		self.gen_layer(SolidBlock, ['dirtograss'], height = 65)

	def draw(self):
		range_x = [self.camera.offset_x/-GRID_SIZE, 1+self.camera.offset_x/-GRID_SIZE+self.camera.screen_w/GRID_SIZE]
		range_y = [self.camera.offset_y/-GRID_SIZE, 1+self.camera.offset_y/-GRID_SIZE+self.camera.screen_h/GRID_SIZE]
		if self.camera.offset_x >= 0:
			range_x[0] = 0
		if self.camera.offset_y >= 0:
			range_y[0] = 0
		if range_x[1] > self.get_width():
			range_x[1] = self.get_width()
		if range_y[1] > self.get_height():
			range_y[1] = self.get_height()

		for x in range(*range_x):
			for y in range(*range_y):
				if isinstance(self.the_map[x][y], Block):
					self.images.draw_image(self.the_map[x][y].name, x*GRID_SIZE, y*GRID_SIZE)

	def get_width(self):
		return len(self.the_map)

	def get_height(self):
		return len(self.the_map[0])