import pygame
import sys

from player import *
from pygame.locals import *
from image import *
from world import *
from layers import *

image_repo = None

class TrollGame:
	SCREEN_W = 800
	SCREEN_H = 512

	def startup(self):
		print('Starting up TROLOLOLOL 2D game')
		pygame.init()
		self.window = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))
		pygame.display.set_caption('TROLLCRAFT 2D')

		self.cam = Camera(self.SCREEN_W, self.SCREEN_H)
		global image_repo
		image_repo = ImageDB(self.cam)
		populate_image_db(image_repo, 'grafon/')
		populate_image_db(image_repo, 'grafon/etc/')
		self.blocks = ImageDB(self.cam)
		populate_image_db(self.blocks, 'grafon/blocks/')
		self.world = World(self.cam, self.blocks)
		self.bg = Background(self.world, self.cam)

		# Player
		self.player = CreeperPlayer(self.cam, self.world)
		self.pc = CreeperPlayerController(self.player)
		self.player.spawn()

		self.clock = pygame.time.Clock()

	def loop(self):
		events = pygame.event.get()
		self.pc.dispatch_events(events)
		self.bg.tick()
		for ev in events:
			if ev.type == QUIT:
				self.shutdown()
				
		self.player.loop()

	def cls(self):
		screen = pygame.display.get_surface()
		background = pygame.Surface(screen.get_size())
		background = background.convert()
		background.fill((0, 0, 0))
		screen.blit(background, (0, 0))

	def draw(self):
		self.cls()
		self.bg.draw()
		self.world.draw()
		if isinstance(self.player, DrawablePlayer):
			self.player.draw()
		pygame.display.flip()

	def shutdown(self):
		self.bg.running = False
		sys.exit(0)

	def __init__(self):
		self.startup()
		while True:
			self.loop()
			self.draw()
			self.clock.tick(60)
