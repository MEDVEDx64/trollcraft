import game

from image import *
from blocks import *
from random import randint

class Player(object):
	# Dummy camera movement 'player'
	def __init__(self, camera, world):
		self.camera = camera
		self.world = world

		self.pos_x = 0
		self.pos_y = 0
		self.speed = 5
		self.width = 0
		self.height = 0
		self.walking = False
		self.last_speed = self.speed
		self.last_moved_right = True

	def loop(self):
		self.sync_camera()
		self.walking = False

	def sync_camera(self):
		self.camera.offset_x = -self.pos_x
		self.camera.offset_y = -self.pos_y

	def spawn(self):
		attempts = 10
		while attempts > 0:
			attempts -= 1
			r = randint(0, self.world.get_width())
			for i in range(self.world.get_height()):
				if isinstance(self.world.the_map[r][i], SolidBlock):
					if i == 0:
						continue

					self.pos_x = r*GRID_SIZE
					self.pos_y = i*GRID_SIZE-self.height
					return

		print("Oopz, can't place player: not enough space.")


	# Std. player's methods

	def on_walk(self, right = True):
		self.walking = True
		self.last_moved_right = right

		if right:
			self.pos_x += self.speed
		else:
			self.pos_x -= self.speed

	def on_jump(self):
		self.pos_y -= self.speed

	def on_crouch(self):
		self.pos_y += self.speed

	def on_sprint(self, entered = True):
		if self.speed > 0:
			if entered:
				self.last_speed = self.speed
				self.speed = 12
			else:
				self.speed = self.last_speed

class DrawablePlayer(Player):
	def draw(self):
		pass

class AnimatedPlayer(DrawablePlayer):
	def __init__(self, camera, world):
		super(AnimatedPlayer, self).__init__(camera, world)
		self.frames = ImageDB(self.camera)

	def initialize_animation(self, sprites_path = 'grafon/player/pootis/'):
		populate_image_db(self.frames, sprites_path)
		self.current = 0
		self.length = len(self.frames.images)/2+1
		if self.length == 0 or not '0' in self.frames.images:
			print('AnimatedPlayer warning: no initial sprite were loaded')
		else:
			self.width = self.frames.images['0'].get_width()
			self.height = self.frames.images['0'].get_height()

	def animation_tick(self):
		if self.length < 2:
			return

		if self.walking:
			self.current += 1
			if self.current >= self.length:
				self.current = 1
		else:
			self.current = 0

	def loop(self):
		self.animation_tick()
		super(AnimatedPlayer, self).loop()

	def draw(self):
		if self.current == 0:
			self.frames.draw_image(str(self.current), self.pos_x, self.pos_y)
		else:
			if self.last_moved_right:
				self.frames.draw_image('r' + str(self.current), self.pos_x, self.pos_y)
			else:
				self.frames.draw_image('l' + str(self.current), self.pos_x, self.pos_y)

from world import GRID_SIZE

class PhysicalPlayer(Player):
	STATE_GROUND = 0
	STATE_FELL = 1
	STATE_FALLING = 2
	STATE_LANDED = 3

	def __init__(self, camera, world):
		super(PhysicalPlayer, self).__init__(camera, world)
		self.MAX_FALL_SPEED = 8
		self.fall_speed = 0
		self.fall_state = self.STATE_GROUND

	def sync_camera(self):
		self.camera.offset_x = -self.pos_x + self.camera.screen_w/2
		self.camera.offset_y = -self.pos_y + self.camera.screen_h/2

		if self.width > 0 and self.height > 0:
			self.camera.offset_x -= self.width/2
			self.camera.offset_y -= self.height/2

		try:
			cam_bound_x = self.camera.screen_w/2 - self.width/2
			cam_bound_y = self.camera.screen_h/2 - self.height/2
			cam_bound1_x = self.world.get_width() * GRID_SIZE - self.camera.screen_w/2 - self.width/2
			cam_bound1_y = self.world.get_height() * GRID_SIZE - self.camera.screen_h/2 - self.height/2

			if self.pos_x < cam_bound_x:
				self.camera.offset_x -= cam_bound_x-self.pos_x
			if self.pos_y < cam_bound_y:
				self.camera.offset_y -= cam_bound_y-self.pos_y
			if self.pos_x > cam_bound1_x:
				self.camera.offset_x += self.pos_x - self.world.get_width()*GRID_SIZE \
					+ self.camera.screen_w/2 + self.width/2
			if self.pos_y > cam_bound1_y:
				self.camera.offset_y += self.pos_y - self.world.get_height()*GRID_SIZE \
					+ self.camera.screen_h/2 + self.height/2

		except ZeroDivisionError:
			pass

	def fall_state_tick(self):
		if self.fall_state == self.STATE_FELL:
			self.fall_state = self.STATE_FALLING
		if self.fall_state == self.STATE_LANDED:
			self.fall_state = self.STATE_GROUND

		if self.fall_state == self.STATE_GROUND and not self.is_on_surface():
			self.fall_state = self.STATE_FELL
		if self.fall_state == self.STATE_FALLING and self.is_on_surface():
			self.fall_state = self.STATE_LANDED

	def in_collision(self):
		# returns true when player crossed with world's collision
		if self.pos_x < 0 or self.pos_y < 0 or \
			(self.pos_x+self.width-1)/GRID_SIZE >= self.world.get_width() or \
			(self.pos_y+self.height-1)/GRID_SIZE >= self.world.get_height():
				return True

		if (self.width == 0 or self.height == 0) and \
			isinstance(self.world.the_map[self.pos_x/GRID_SIZE][self.pos_y/GRID_SIZE], SolidBlock):
				return True

		for i in range(self.width):
			if isinstance(self.world.the_map[(self.pos_x+i)/GRID_SIZE][self.pos_y/GRID_SIZE], SolidBlock) \
				or isinstance(self.world.the_map[(self.pos_x+i)/GRID_SIZE][(self.pos_y+self.height-1)/GRID_SIZE], SolidBlock):
					return True

		for i in range(self.height):
			if isinstance(self.world.the_map[self.pos_x/GRID_SIZE][(self.pos_y+i)/GRID_SIZE], SolidBlock) \
				or isinstance(self.world.the_map[(self.pos_x+self.width-1)/GRID_SIZE][(self.pos_y+i)/GRID_SIZE], SolidBlock):
					return True

		return False

	def move(self, direction, speed):
		if speed > 0:
			for i in range(speed):
				if direction == 'up':
					self.pos_y -= 1
					if self.in_collision():
						self.pos_y += 1
						break
				elif direction == 'down':
					self.pos_y += 1
					if self.in_collision():
						self.pos_y -= 1
						break
				elif direction == 'right':
					self.pos_x += 1
					if self.in_collision():
						self.pos_x -= 1
						break
				elif direction == 'left':
					self.pos_x -= 1
					if self.in_collision():
						self.pos_x += 1
						break
		elif speed < 0:
			for i in range(speed*-1):
				if direction == 'down':
					self.pos_y -= 1
					if self.in_collision():
						self.fall_speed = 0
						self.pos_y += 1
						break
				elif direction == 'up':
					self.pos_y += 1
					if self.in_collision():
						self.pos_y -= 1
						break
				elif direction == 'left':
					self.pos_x += 1
					if self.in_collision():
						self.pos_x -= 1
						break
				elif direction == 'right':
					self.pos_x -= 1
					if self.in_collision():
						self.pos_x += 1
						break

	def loop(self):
		super(PhysicalPlayer, self).loop()
		self.fall_state_tick()
		if self.fall_state == self.STATE_FELL and self.fall_speed > 0:
			self.fall_speed = 0

		if not self.is_on_surface():
			if self.fall_speed < self.MAX_FALL_SPEED:
				self.fall_speed += 1
			if self.fall_speed > self.MAX_FALL_SPEED:
				self.fall_speed = self.MAX_FALL_SPEED

		self.move('down', speed = self.fall_speed)

	def is_on_surface(self):
		self.pos_y += 1
		result = self.in_collision()
		self.pos_y -= 1
		return result

	def on_jump(self):
		if self.is_on_surface():
			self.fall_speed = -12

	def on_walk(self, right = True):
		self.walking = True
		self.last_moved_right = right
		
		if right:
			self.move('right', self.speed)
		else:
			self.move('left', self.speed)

	def on_crouch(self):
		pass

class BuilderPlayer(PhysicalPlayer, AnimatedPlayer):
	def __init__(self, camera, world):
		super(BuilderPlayer, self).__init__(camera, world)
		self.curs_x = 0 # screen-relative
		self.curs_y = 0
		self.digging = False
		self.placing = False
		self.highlighted_block = None

	def on_digging_start(self):
		self.digging = True

	def on_digging_end(self):
		self.digging = False

	def on_placing_start(self):
		if isinstance(self.highlighted_block, InteractiveBlock):
			self.highlighted_block.on_click()
		else:
			self.placing = True

	def on_placing_end(self):
		self.placing = False

	def loop(self):
		super(BuilderPlayer, self).loop()
		try:
			self.highlighted_block = self.world.the_map[(self.curs_x-self.camera.offset_x)/GRID_SIZE] \
				[(self.curs_y-self.camera.offset_y)/GRID_SIZE]
		except IndexError:
				return

		if self.digging:
			if isinstance(self.highlighted_block, SolidBlock):
				if self.highlighted_block.strength == 0:
					self.highlighted_block.on_destroyed()
					self.world.the_map[(self.curs_x-self.camera.offset_x)/GRID_SIZE] \
						[(self.curs_y-self.camera.offset_y)/GRID_SIZE] = None
					return
				self.highlighted_block.strength -= 1

		if self.placing:
			if self.highlighted_block == None:
				self.world.the_map[(self.curs_x-self.camera.offset_x)/GRID_SIZE] \
					[(self.curs_y-self.camera.offset_y)/GRID_SIZE] = TestBlock(name = 'adminium')

	def draw(self):
		super(BuilderPlayer, self).draw()
		s = pygame.display.get_surface()
		x = (self.curs_x-self.camera.offset_x)/GRID_SIZE*GRID_SIZE+self.camera.offset_x
		y = (self.curs_y-self.camera.offset_y)/GRID_SIZE*GRID_SIZE+self.camera.offset_y
		pygame.gfxdraw.box(s, (x, y, GRID_SIZE, GRID_SIZE), (0xff, 0, 0, 0x60))
		if self.digging:
			game.image_repo.draw_image('pickaxe', x+1, y+1, True)

class CreeperPlayer(BuilderPlayer):
	def __init__(self, camera, world):
		super(CreeperPlayer, self).__init__(camera, world)
		self.initialize_animation(sprites_path = 'grafon/player/creeper/')

	def boom(self):
		print('boom!')

import pygame
from pygame.locals import *

class PlayerController(object):
	def __init__(self, player):
		self.player = player
		self.km = KeyboardManager()

	def dispatch_events(self, events):
		self.km.process_events(events)
		if self.km.get_key_state(K_LEFT) == KS_PRESSED or self.km.get_key_state(K_LEFT) == KS_DOWN:
			self.player.on_walk(False)
		if self.km.get_key_state(K_RIGHT) == KS_PRESSED or self.km.get_key_state(K_RIGHT) == KS_DOWN:
			self.player.on_walk()
		if self.km.get_key_state(K_SPACE) == KS_PRESSED or self.km.get_key_state(K_SPACE) == KS_DOWN:
			self.player.on_jump()
		if self.km.get_key_state(K_DOWN) == KS_PRESSED or self.km.get_key_state(K_DOWN) == KS_DOWN:
			self.player.on_crouch()

class BuilderPlayerController(PlayerController):
	def dispatch_events(self, events):
		super(BuilderPlayerController, self).dispatch_events(events)
		for e in events:
			if e.type == MOUSEMOTION or e.type == MOUSEBUTTONDOWN or e.type == MOUSEBUTTONUP:
				self.player.curs_x = e.pos[0]
				self.player.curs_y = e.pos[1]
			if e.type == MOUSEBUTTONDOWN:
				if e.button == 1:
					self.player.on_digging_start()
				elif e.button == 3:
					self.player.on_placing_start()
			elif e.type == MOUSEBUTTONUP:
				if e.button == 1:
					self.player.on_digging_end()
				elif e.button == 3:
					self.player.on_placing_end()

class CreeperPlayerController(BuilderPlayerController):
	def dispatch_events(self, events):
		super(CreeperPlayerController, self).dispatch_events(events)
		if self.km.get_key_state(K_b) == KS_PRESSED:
			self.player.boom()

KS_UP = 0
KS_PRESSED = 1
KS_DOWN = 2
KS_RELEASED = 3

class KeyboardManager:
	def __init__(self):
		self.key_states = {}

	def process_events(self, events):
		for k in self.key_states:
			if self.key_states[k] == KS_PRESSED:  self.key_states[k] = KS_DOWN
			if self.key_states[k] == KS_RELEASED: self.key_states[k] = KS_UP

		for e in events:
			if e.type == KEYDOWN:
				self.key_states[e.key] = KS_PRESSED
			elif e.type == KEYUP:
				self.key_states[e.key] = KS_RELEASED

	def get_key_state(self, key):
		try:
			return self.key_states[key]
		except KeyError:
			return KS_UP
