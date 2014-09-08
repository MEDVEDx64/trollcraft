from pygame.locals import *
from world import GRID_SIZE
import pygame
import player
import blocks
import image
import game
import copy

class Element(object):
	def __init__(self, font, camera, args = None):
		self.font = font
		self.camera = camera
		self.args = args

	def draw(self):
		pass

class FPSElement(Element):
	def draw(self):
		try:
			s = self.font.render('FPS: ' + str(round(self.args[0].get_fps(), 2)), True, \
				(255, 255, 255, 255), (0, 0, 0, 255))
			pygame.display.get_surface().blit(s, (4, self.camera.screen_h - 5 - s.get_height()))
		except IndexError:
			pass

class SlotsElement(Element):
	def draw(self):
		if len(self.args) < 1 or not isinstance(self.args[0], player.BuilderPlayer):
			return

		display = pygame.display.get_surface()
		start_x, start_y = 5, 5
		pygame.gfxdraw.rectangle(display, (start_x-1, start_y-1, \
			len(self.args[0].slots)*20+2, 22), (0, 0, 0, 255))

		for i in range(len(self.args[0].slots)):
			red = 32
			if i%2 == 0:
				red = 96

			pygame.gfxdraw.box(display, (start_x+i*20, start_y, 20, 20), (red, 64, 224, 160))
			if self.args[0].highlighted_slot == i:
				pygame.gfxdraw.rectangle(display, (start_x+i*20, start_y, 20, 20), (255, 255, 0, 255))
			if isinstance(self.args[0].slots[i], blocks.Block):
				s = pygame.transform.scale(self.args[1].images.images[self.args[0].slots[i].name], (16, 16))
				display.blit(s, (start_x+i*(20)+2, start_y+2))

class CursorElement(Element):
	def __init__(self, font, camera, args = None):
		super(CursorElement, self).__init__(font, camera, args)
		self.rect = (0, 0, 0, 0)
		self.digging = False

	def update(self, rect, digging = False):
		self.rect = rect
		self.digging = digging

	def draw(self):
		s = pygame.display.get_surface()
		pygame.gfxdraw.box(s, self.rect, (0xff, 0, 0, 0x60))
		if self.digging:
			game.image_repo.draw_image('pickaxe', self.rect[0]+1, self.rect[1]+1, True)

class Frame(Element):
	def __init__(self, font, camera, args = None):
		super(Frame, self).__init__(font, camera, args)
		self.active = False

	def draw(self):
		t = self.font.render('Sample dialog frame. Press ESC to leave.', True, (255,255,255,255), (0,0,0,255))
		d = pygame.display.get_surface()
		d.blit(t, (self.camera.screen_w/2-t.get_width()/2, self.camera.screen_h/2-t.get_height()/2))

	def dispatch_events(self, events):
		for e in events:
			if e.type == KEYDOWN and e.key == K_ESCAPE:
				self.active = False

class InventoryFrame(Frame):
	def __init__(self, font, camera, args = None):
		super(InventoryFrame, self).__init__(font, camera, args)
		self.curs_x, self.curs_y = 0, 0
		self.GRID_W, self.GRID_H = GRID_SIZE+4, GRID_SIZE+4
		self.items = {}

	def draw(self):
		d = pygame.display.get_surface()
		pygame.gfxdraw.box(d, (0, 0, self.camera.screen_w, self.camera.screen_h), (50, 65, 144, 150))
		t = self.font.render('Inventory Block', True, (255,255,255,255))
		d.blit(t, (self.camera.screen_w-t.get_width()-5, 4))

		color = [25, 65, 144, 150]
		x, y = 0, 1

		try:
			for item in self.args[2]['blocks']:
				if isinstance(item, blocks.Block):
					self.items[str(x) + '.' + str(y)] = item
					if self.curs_x == x and self.curs_y == y:
						pygame.gfxdraw.box(d, (x*self.GRID_W, y*self.GRID_H, self.GRID_W, \
							self.GRID_H), (255, 48, 0, 200))
					else:
						pygame.gfxdraw.box(d, (x*self.GRID_W, y*self.GRID_H, self.GRID_W, \
							self.GRID_H), tuple(color))
					self.args[1].images.draw_image(item.name, x*self.GRID_W+2, y*self.GRID_H+2, True)

					if color[0] == 25:
						color[0] = 125
					else:
						color[0] = 25

					x += 1
					if x >= self.camera.screen_w/self.GRID_W:
						x = 0
						y += 1
					if y >= self.camera.screen_h/self.GRID_H:
						break

					try:
						itemname = self.font.render(self.items[str(self.curs_x) + '.' \
							+ str(self.curs_y)].name, True, (255, 224, 0, 255))
						d.blit(itemname, (self.camera.screen_w - itemname.get_width() - 5, 21))
					except KeyError:
						pass

		except (IndexError, KeyError, TypeError):
			pass

	def dispatch_events(self, events):
		super(InventoryFrame, self).dispatch_events(events)
		for e in events:
			if e.type == MOUSEMOTION:
				self.curs_x = e.pos[0]/self.GRID_W
				self.curs_y = e.pos[1]/self.GRID_H
			if e.type == MOUSEBUTTONDOWN and e.button == 1:
				try:
					b = self.items[str(self.curs_x) + '.' + str(self.curs_y)]
					self.args[0].slots[self.args[0].highlighted_slot] = copy.copy(b)
					#self.active = False
				except (KeyError, TypeError):
					pass

			if e.type == KEYDOWN:
				if e.key == K_1: self.args[0].on_slot_change(0)
				if e.key == K_2: self.args[0].on_slot_change(1)
				if e.key == K_3: self.args[0].on_slot_change(2)
				if e.key == K_4: self.args[0].on_slot_change(3)
				if e.key == K_5: self.args[0].on_slot_change(4)

class DialogManager:
	def __init__(self, font, camera):
		self.font = font
		self.camera = camera
		self.frame = Frame(font, camera)

	def show(self, frm_class, frm_args = None):
		self.frame = frm_class(self.font, self.camera, frm_args)
		self.frame.active = True