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
