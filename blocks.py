class Block(object):
	# Basic block class
	def __init__(self):
		self.name = 'pootis'

	def __init__(self, name):
		self.name = name

	def on_destroyed(self):
		pass

class SolidBlock(Block):
	def __init__(self, strength = 16, material = 'pootis'):
		super(SolidBlock, self).__init__()
		self.strength = strength
		self.material = material

	def __init__(self, name, strength = 16, material = 'pootis'):
		super(SolidBlock, self).__init__(name)
		self.strength = strength
		self.material = material