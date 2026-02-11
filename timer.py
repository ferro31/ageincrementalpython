import pygame


class Timer:
	def __init__(self, duration, func=None, loop=False):
		self.duration = duration
		self.func = func
		self.loop = loop
		self.start_time = 0
		self.active = False

	def activate(self):
		self.active = True
		self.start_time = pygame.time.get_ticks()

	def deactivate(self):
		self.active = False
		self.start_time = 0

	def update(self):
		current_time = pygame.time.get_ticks()
		if (current_time - self.start_time >= self.duration) and self.active:
			if self.func and self.start_time != 0:
				self.func()
			if not self.loop:
				self.deactivate()
			else:
				self.activate()
