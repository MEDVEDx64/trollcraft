import game
import gui

class Block(object):
	# Basic block class
	def __init__(self):
		self.name = 'pootis'

	def __init__(self, name):
		self.name = name

	def on_destroyed(self):
		pass

class InteractiveBlock(Block):
	def on_click(self):
		pass

class SolidBlock(Block):
	def __init__(self, name, strength = 16):
		super(SolidBlock, self).__init__(name)
		self.strength = strength

class LiquidBlock(Block):
	pass

class DictionaryBlock(Block):
	def __init__(self, name):
		super(DictionaryBlock, self).__init__(name)
		self.dict = {}

class InventoryBlock(InteractiveBlock, SolidBlock, DictionaryBlock):
	def on_click(self, player = None, world = None):
		game.dialog.show(gui.InventoryFrame, [player, world, self.dict])
