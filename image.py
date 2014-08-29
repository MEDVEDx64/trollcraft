import pygame

class ImageDB:
	def __init__(self, camera):
		self.camera = camera
		self.EXSTENSION = 'png'
		self.images = {}

	def add_image(self, name, prefix = ''):
		image = None
		try:
			image = pygame.image.load(prefix + name + '.' + self.EXSTENSION)
		except pygame.error:
			print("Image '" + name + "' couldn't be loaded")
			raise

		if name in self.images:
			print("Warning: replacing existent image '" +  name + "' with a new one")

		self.images[name] = image
		print("Registered image '" + name + "'")

	def draw_image(self, name, x, y):
		if name in self.images:
			if (x+self.camera.offset_x+self.images[name].get_width()) > 0 and (x+self.camera.offset_x) < self.camera.screen_w \
				and (y+self.camera.offset_y+self.images[name].get_height()) > 0 and (y+self.camera.offset_y) < self.camera.screen_h:
					screen = pygame.display.get_surface()
					screen.blit(self.images[name], (x + self.camera.offset_x, y + self.camera.offset_y))
		else:
			print("Warning: no such image '" +  name + "'")

class Camera:
	def __init__(self, screen_w, screen_h):
		self.offset_x = 0
		self.offset_y = 0
		self.screen_w = screen_w
		self.screen_h = screen_h

from glob import glob

def populate_image_db(target_db, path_prefix = 'grafon/'):
	for i in glob(path_prefix + '*.' + target_db.EXSTENSION):
		target_db.add_image(i.split('/')[-1].split('\\')[-1][:-(len(target_db.EXSTENSION)+1)], path_prefix)