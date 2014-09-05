from random import randint
import blocks
import copy

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

	def gen_layer(self, block, height = 60, scale = 5, force = False):
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
					if c[y] == None or force:
						c[y] = copy.copy(block)
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
			print("""Oops, zat was not medicine! The world the_map is uninitialized,
				or there were very much invalid input values.""")

	def gen_pile(self, block, x, y):
		for ix in range(4):
			for iy in range(4):
				ok = True
				if ix == 0 or iy == 0 or ix == 3 or iy == 3:
					if randint(0, 6) > 2:
						ok = False
				if ok:
					try:
						self.the_map[ix+x][iy+y] = copy.copy(block)
					except IndexError:
						pass

	def gen_ores(self, block, height = 54, chance = 10):
		for x in range(0, self.get_width(), 8):
			for y in range(self.get_height()-height, self.get_height(), 6):
				if randint(0, 100) > (100-chance):
					rn = randint(0, 10)
					rx = x+randint(0, 6)
					ry = y+randint(0, 5)

					try:
						if rn > 6:
							self.gen_pile(block, rx, ry)
						elif rn > 3:
							self.the_map[rx][ry] = copy.copy(block)
							if randint(0, 4) > 2: self.the_map[rx+1][ry] = copy.copy(block)
							if randint(0, 4) > 2: self.the_map[rx+1][ry+1] = copy.copy(block)
							self.the_map[rx][ry+1] = copy.copy(block)
						else:
							self.the_map[rx][ry] = copy.copy(block)
					except IndexError:
						pass

	def generate(self, w = 240, h = 180):
		self.the_map = []
		self.initialize_map(w, h)
		self.gen_layer(blocks.SolidBlock('stone', 38))
		self.gen_layer(blocks.SolidBlock('dirt'), scale = 7)
		self.gen_layer(blocks.SolidBlock('dirtograss'), height = 65)

		self.gen_ores(blocks.SolidBlock('dirt'), chance = 25)
		self.gen_ores(blocks.SolidBlock('grafonium_crystal_type_a', strength = 100), height = 32)
		self.gen_ores(blocks.SolidBlock('grafonium_crystal_type_b', strength = 100), height = 22, chance = 5)

		self.gen_layer(blocks.SolidBlock('adminium', 100500), height = 7, scale = 3, force = True)

	def draw(self): # it also invokes tick method on blocks
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
				if isinstance(self.the_map[x][y], blocks.Block):
					self.the_map[x][y].tick(x, y, self)
				if isinstance(self.the_map[x][y], blocks.Block):
					self.images.draw_image(self.the_map[x][y].name, x*GRID_SIZE, y*GRID_SIZE)

	def get_width(self):
		return len(self.the_map)

	def get_height(self):
		return len(self.the_map[0])

	def drop_a_block(self, block, x = -1):
		fx = x
		if x < 0:
			fx = randint(0, self.get_width()-1)

		try:
			for y in range(self.get_height()):
				if not y == 0 and isinstance(self.the_map[fx][y], blocks.SolidBlock):
					self.the_map[fx][y-1] = block
					break
		except IndexError:
			print('Cannot drop a block outside the world.')