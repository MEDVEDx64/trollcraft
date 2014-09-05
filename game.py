import pygame
import sys

import player
import image
import layers
import blocks
import world
import gui

from glob import glob
from pygame.locals import *

class TrollGame:
	SCREEN_W = 800
	SCREEN_H = 512

	def startup(self):
		print('Starting up TROLOLOLOL 2D game')
		pygame.init()
		self.window = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))
		pygame.display.set_caption('TROLLCRAFT 2D')

		self.cam = image.Camera(self.SCREEN_W, self.SCREEN_H)
		global image_repo
		image_repo = image.ImageDB(self.cam)
		image.populate_image_db(image_repo, 'grafon/')
		image.populate_image_db(image_repo, 'grafon/etc/')
		self.blocks = image.ImageDB(self.cam)
		image.populate_image_db(self.blocks, 'grafon/blocks/')
		self.world = world.World(self.cam, self.blocks)
		self.bg = layers.Background(self.world, self.cam)
		self.fg = layers.Foreground(self.world, self.cam)

		# Player
		self.player = player.CreeperPlayer(self.cam, self.world)
		self.pc = player.CreeperPlayerController(self.player)
		self.player.spawn()

		self.clock = pygame.time.Clock()

		pygame.font.init()
		font = pygame.font.Font(glob('ttf/*.ttf')[0], 16)
		global dialog
		dialog = gui.DialogManager(font, self.cam)
		global cursor
		cursor = gui.CursorElement(font, self.cam)

		crate = blocks.InventoryBlock('inventory_white', strength = 250)
		crate.dict = {
			'blocks': blocks.known_blocks
		}
		self.world.drop_a_block(crate, self.player.pos_x/world.GRID_SIZE+2)

		self.gui_elements = []
		self.gui_elements.append(gui.FPSElement(font, self.cam, [self.clock]))
		self.gui_elements.append(cursor)

		self.final_fx = layers.FXStack()
		#self.final_fx.add_layer(layers.PixelateFX())

	def loop(self):
		events = pygame.event.get()
		for ev in events:
			if ev.type == QUIT:
				self.shutdown()

		if dialog.frame.active:
			dialog.frame.dispatch_events(events)
		else:
			self.pc.dispatch_events(events)
				
		self.bg.tick()
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
		if isinstance(self.player, player.DrawablePlayer):
			self.player.draw()

		self.world.draw()
		self.fg.draw()

		for element in self.gui_elements:
			element.draw()

		if dialog.frame.active:
			dialog.frame.draw()

		# Applying FX stack
		# screen = pygame.display.get_surface()
		# screen.blit(self.final_fx.process(screen), (0, 0))
		pygame.display.flip()

	def shutdown(self):
		self.bg.running = False
		pygame.font.quit()
		sys.exit(0)

	def __init__(self):
		self.startup()
		while True:
			self.loop()
			self.draw()
			self.clock.tick(60)
