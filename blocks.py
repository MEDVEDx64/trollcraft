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
	LiquidBlock('water'),
	SolidBlock('bricks_gray', strength = 40),
	SolidBlock('bricks_blue', strength = 40),
	SolidBlock('bricks_yellow', strength = 40),
	SolidBlock('bricks_red', strength = 40),
	SolidBlock('grafonium_red', strength = 120)
]

from random import randint

def gen_inventory_block(theme = 'white'):
	b = InventoryBlock('inventory_' + theme , strength = 250)
	if randint(0, 20) > 18:
		b.dict['blocks'] = copy.copy(known_blocks)
	else:
		b.dict['blocks'] = []
		count = randint(2, len(known_blocks)/2)
		if randint(0, 5) > 3:
			count = randint(2, len(known_blocks)-len(known_blocks)/4*3)
		flags = [False for i in known_blocks]
		while count > 0:
			n = randint(0, len(known_blocks)-1)
			if flags[n]:
				continue
			flags[n] = True
			b.dict['blocks'].append(known_blocks[n])
			count -= 1

	return b