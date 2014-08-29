# Some drawable stuff

import time
import pygame
import pygame.gfxdraw
import random

class Background():
	def __init__(self, world, camera):
		self.world = world
		self.camera = camera
		self.color = [150, 200, 220, 255]
		self.day = False
		self.skip = 250

	def tick(self):
		if self.skip > 0:
			self.skip -= 1
			return

		if self.day and self.color[3] > 252:
			self.day = False
			self.skip = 2000
			return
		elif not self.day and self.color[3] < 4:
			self.day = True
			self.skip = 1600
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

		self.skip = 10

	def draw_stars(self):
		random.seed(100500)
		screen = pygame.display.get_surface()
		for i in range(120):
			x = random.randint(0, self.camera.screen_w)
			y = random.randint(0, self.camera.screen_h)
			size = random.randint(0, 1)
			if size == 0:
				pygame.gfxdraw.pixel(screen, x, y, (255, 255, 255, 255))
			else:
				pygame.gfxdraw.box(screen, (x, y, 2, 2), (255, 255, 255, 255))

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