# Some drawable stuff

import time
import world
import pygame
import pygame.gfxdraw
from random import randint, Random

class Layer(object):
	def __init__(self, world, camera):
		self.world = world
		self.camera = camera

	def tick(self): pass
	def draw(self): pass

class ComplexLayer(Layer):
	def __init__(self, world, camera):
		super(ComplexLayer, self).__init__(world, camera)
		self.layers = []

	def tick(self):
		for l in self.layers:
			l.tick()

	def draw(self):
		for l in self.layers:
			l.draw()

class ClassicBackground(Layer):
	def __init__(self, world, camera):
		super(ClassicBackground, self).__init__(world, camera)
		self.color = [150, 200, 220, 255]
		self.day = False
		self.skip = randint(0, 2000)

	def tick(self):
		if self.skip > 0:
			self.skip -= 1
			return

		if self.day and self.color[3] > 252:
			self.day = False
			self.skip = 4000
			return
		elif not self.day and self.color[3] < 4:
			self.day = True
			self.skip = 2600
			return

		if self.day:
			self.color[3] += 2
			self.color[2] += 2
			self.color[1] += 1
		else:
			self.color[3] -= 2
			self.color[2] -= 2
			self.color[1] -= 1

		for i in range(len(self.color)):
			if self.color[i] < 0:
				self.color[i] = 0
			elif self.color[i] > 255:
				self.color[i] = 255

		self.skip = 48

	def draw_stars(self):
		rnd = Random(100500)
		screen = pygame.display.get_surface()
		for i in range(120):
			x = rnd.randint(0, self.camera.screen_w)
			y = rnd.randint(0, self.camera.screen_h)
			size = rnd.randint(0, 1)

			alpha = (self.world.get_height()*world.GRID_SIZE+self.camera.offset_y-768)/4
			if alpha > 255: alpha = 255
			elif alpha < 0: alpha = 0

			if size == 0:
				pygame.gfxdraw.pixel(screen, x, y, (255, 255, 255, alpha))
			else:
				pygame.gfxdraw.box(screen, (x, y, 2, 2), (255, 255, 255, alpha))

	def draw_sky(self):
		screen = pygame.display.get_surface()
		color = self.color[:3]
		alpha = 255
		if self.camera.offset_y > -1024:
			if self.camera.offset_y > 0:
				alpha = 0
			else:
				alpha = (-self.camera.offset_y) / 4
				if alpha > self.color[3]:
					alpha = self.color[3]
			color.append(alpha)
		else:
			color.append(self.color[3])
		pygame.gfxdraw.box(screen, (0, 0, self.camera.screen_w, self.camera.screen_h), tuple(color))

	def draw(self):
		self.draw_stars()
		self.draw_sky()

class ClassicForeground(Layer):
	def draw(self):
		fading_step = 16
		the_initial = self.world.get_height()*world.GRID_SIZE-fading_step*112
		if self.camera.offset_y < -(the_initial):
			screen = pygame.display.get_surface()
			try:
				pygame.gfxdraw.box(screen, (0, 0, self.camera.screen_w, self.camera.screen_h), (0, 0, 0, -((the_initial+self.camera.offset_y)/fading_step)*2))
			except TypeError:
				pass

class FXLayer(object):
	def process(self, surface):
		return surface

class PixelateFX(FXLayer):
	def process(self, surface):
		s = pygame.transform.scale(surface, (surface.get_width()/8, surface.get_height()/8))
		return pygame.transform.scale(s, (surface.get_width(), surface.get_height()))

class GlitchFX(FXLayer):
	def process(self, surface):
		px = pygame.PixelArray(surface)
		step = 16
		shift = [0, 0, 0]
		dup = px[:][:]
		skip = True
		rnd = Random(round(time.time(), 1))

		for i in range(surface.get_height()):
			if i%step == 0:
				if rnd.randint(0, 100) > 99:
					skip = False
				else:
					skip = True

				for s in range(len(shift)):
					if rnd.randint(0, 8) > 4:
						shift[s] = 0
					else:
						shift[s] = rnd.randint(1, 32)

			if skip:
				continue

			for x in range(surface.get_width()):
				try:
					px[x][i] = (dup[x+shift[0]][i]&0xff0000) | (dup[x+shift[1]][i]&0xff00) | (dup[x+shift[2]][i]&0xff)
				except IndexError:
					pass

		retval = px.make_surface()
		del px
		return retval

class FXStack:
	def __init__(self):
		self.stack = []

	def add_layer(self, layer):
		self.stack.append(layer)

	def process(self, surface):
		cs = surface
		for layer in self.stack:
			cs = layer.process(cs)
		return cs

final_fx = FXStack()
single_fx = FXStack() # temporary stack, cleans up each tick