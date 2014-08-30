from pygame.locals import *
import pygame

class Element(object):
	def __init__(self, font, camera):
		self.font = font
		self.camera = camera

	def draw(self):
		pass

class Frame(Element):
	def __init__(self, font, camera):
		super(Frame, self).__init__(font, camera)
		self.active = False

	def draw(self):
		t = self.font.render('Sample dialog frame. Press ESC to leave.', True, (255,255,255,255), (0,0,0,255))
		d = pygame.display.get_surface()
		d.blit(t, (self.camera.screen_w/2-t.get_width()/2, self.camera.screen_h/2-t.get_height()/2))

	def dispatch_events(self, events):
		for e in events:
			if e.type == KEYDOWN and e.key == K_ESCAPE:
				self.active = False

class DialogManager:
	def __init__(self, font, camera):
		self.font = font
		self.camera = camera
		self.frame = Frame(font, camera)

	def show(self, frm_class):
		self.frame = frm_class(self.font, self.camera)
		self.frame.active = True