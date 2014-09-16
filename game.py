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
		image.populate_image_db(self.blocks, 'grafon/userblocks/')
		blocks.populate_blocks(self.blocks)
		image.populate_image_db(self.blocks, 'grafon/blocks/')
		self.world = world.ClassicThemedWorld(self.cam, self.blocks)

		# Player
		self.player = player.CreeperPlayer(self.cam, self.world)
		self.pc = player.CreeperPlayerController(self.player)
		self.player.spawn()

		self.bots = []
		test_bot_player = player.TestBotPlayer(self.cam, self.world)
		test_bot = {'player': test_bot_player, 'controller': player.TestBotPlayerController(test_bot_player)}
		self.bots.append(test_bot)
		self.bots[0]['player'].spawn()

		self.clock = pygame.time.Clock()

		pygame.font.init()
		font = pygame.font.Font(glob('ttf/*.ttf')[0], 16)
		global dialog
		dialog = gui.DialogManager(font, self.cam)
		global cursor
		cursor = gui.CursorElement(font, self.cam)

		self.gui_elements = []
		self.gui_elements.append(gui.FPSElement(font, self.cam, [self.clock]))
		self.gui_elements.append(cursor)
		self.gui_elements.append(gui.SlotsElement(font, self.cam, [self.player, self.world]))

		#layers.final_fx.add_layer(layers.PixelateFX())

	def loop(self):
		events = pygame.event.get()
		for ev in events:
			if ev.type == QUIT:
				self.shutdown()

		del layers.single_fx.stack[:]
		if dialog.frame.active:
			dialog.frame.dispatch_events(events)
		else:
			self.pc.dispatch_events(events)
				
		self.world.tick()
		for i in self.bots:
			i['controller'].dispatch_events(events)
			i['player'].loop()

		self.player.loop()

	def cls(self):
		screen = pygame.display.get_surface()
		background = pygame.Surface(screen.get_size())
		background = background.convert()
		background.fill((0, 0, 0))
		screen.blit(background, (0, 0))

	def draw(self):
		self.cls()
		self.world.bg.draw()

		for i in self.bots:
			if isinstance(i['player'], player.DrawablePlayer):
				i['player'].draw()			

		if isinstance(self.player, player.DrawablePlayer):
			self.player.draw()

		self.world.draw()
		self.world.fg.draw()

		for element in self.gui_elements:
			element.draw()

		if dialog.frame.active:
			dialog.frame.draw()

		# Applying FX stack
		screen = pygame.display.get_surface()
		if len(layers.final_fx.stack) > 0:
			screen.blit(layers.final_fx.process(screen), (0, 0))
		if len(layers.single_fx.stack) > 0:
			screen.blit(layers.single_fx.process(screen), (0, 0))
		pygame.display.flip()

	def shutdown(self):
		pygame.font.quit()
		sys.exit(0)

	def __init__(self):
		self.startup()
		while True:
			self.loop()
			self.draw()
			self.clock.tick(60)
