import world
import game
import copy
import gui

class Block(object):
	# Basic block class
	def __init__(self, name = 'pootis'):
		self.name = name

	def tick(self, x, y, world):
		pass

	def on_destroyed(self):
		pass

class InteractiveBlock(Block):
	def on_click(self):
		pass

class SolidBlock(Block):
	def __init__(self, name = 'stone', strength = 16):
		super(SolidBlock, self).__init__(name)
		self.strength = strength

class LiquidBlock(Block):
	def __init__(self, name = 'water'):
		super(LiquidBlock, self).__init__(name)
		self.liquid_factor = 0
		self.LIQUID_FACTOR_MAX = 16

	def tick(self, x, y, world):
		if self.liquid_factor < self.LIQUID_FACTOR_MAX:
			self.liquid_factor += 1
			return

		nblock = copy.copy(world.the_map[x][y])
		nblock.liquid_factor = 0

		try:
			if world.the_map[x-1][y] == None or world.the_map[x+1][y] == None:
				world.the_map[x][y] = None
			else:
				world.the_map[x][y] = nblock
			
			if world.the_map[x][y+1] == None:
				world.the_map[x][y+1] = nblock

		except IndexError:
			world.the_map[x][y] = None

class DictionaryBlock(Block):
	def __init__(self, name):
		super(DictionaryBlock, self).__init__(name)
		self.dict = {}

class InventoryBlock(InteractiveBlock, SolidBlock, DictionaryBlock):
	def on_click(self, player = None, world = None):
		game.dialog.show(gui.InventoryFrame, [player, world, self.dict])

global known_blocks
known_blocks = [
	SolidBlock('dirtograss'),
	SolidBlock('stone', strength = 38),
	SolidBlock('dirt'),
	SolidBlock('bricks', strength = 40),
	SolidBlock('graybricks', strength = 40),
	SolidBlock('red_graphonium', strength = 64),
	LiquidBlock('water')
]