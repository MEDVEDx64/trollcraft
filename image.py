import pygame
import os.path

class ImageDB(object):
	def __init__(self, camera):
		self.camera = camera
		self.EXSTENSION = 'png'
		self.images = {}

	def add_image(self, name, prefix = ''):
		image = None
		if os.path.isdir(prefix + name + '.' + self.EXSTENSION):
			image = Animation(self.camera)
			populate_image_db(image, prefix + name + '.' + self.EXSTENSION + '/')
		else:
			try:
				image = pygame.image.load(prefix + name + '.' + self.EXSTENSION)
			except pygame.error:
				print("Image '" + name + "' couldn't be loaded")
				raise

		if name in self.images:
			print("Warning: replacing existent image '" +  name + "' with a new one")

		self.images[name] = image
		print("Registered image '" + name + "'")

	def draw_image(self, name, x, y, ignore_camera = False):
		if name in self.images:
			image = None
			if isinstance(self.images[name], Animation):
				image = self.images[name].images[str(self.images[name].frame)]
				self.images[name].tick()
			else:
				image = self.images[name]

			cam_x = self.camera.offset_x
			cam_y = self.camera.offset_y
			if ignore_camera:
				self.camera.offset_x = 0
				self.camera.offset_y = 0

			if (x+self.camera.offset_x+image.get_width()) > 0 and (x+self.camera.offset_x) < self.camera.screen_w \
				and (y+self.camera.offset_y+image.get_height()) > 0 and (y+self.camera.offset_y) < self.camera.screen_h:
					screen = pygame.display.get_surface()
					screen.blit(image, (x + self.camera.offset_x, y + self.camera.offset_y))

			if ignore_camera:
				self.camera.offset_x = cam_x
				self.camera.offset_y = cam_y
				
		else:
			print("Warning: no such image '" +  name + "'")

class Animation(ImageDB):
	def __init__(self, camera):
		super(Animation, self).__init__(camera)
		self.frame = 0
		self.skip = 4
		self.skip_cur = self.skip

	def tick(self):
		if self.skip_cur > 0:
			self.skip_cur -= 1
			return
		else:
			self.skip_cur = self.skip
			self.frame += 1
		if self.frame >= len(self.images):
			self.frame = 0

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