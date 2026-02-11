import pygame
import os
from button import Button
from timer import Timer
import random
from Notation import notate


class none:
	def __init__(self, win, wh, game_state):
		self.font = pygame.font.Font(os.getcwd() + '/assets/font.ttf', 20)

		self.left_mouse_debounce = False

		self.win = win
		self.w, self.h = wh
		self.game_state = game_state

		self.button_group = pygame.sprite.Group()
		self.shop_button = Button((self.w / 2 - 100, self.h / 2 - 100), (10, 10), 'shop', win, self.font, (2, 2), "Shop")
		self.button_group.add(self.shop_button)
		self.ascend_button = Button((self.w / 2 + 100, self.h / 2 - 100), (10, 10), 'ascend', win, self.font, (2, 2), "Ascend")
		self.button_group.add(self.ascend_button)
		self.ascend_button = Button((self.w / 2, self.h / 2), (10, 10), 'achievements', win, self.font, (2, 2), "Achievements")
		self.button_group.add(self.ascend_button)

	def game_loop(self):
		self.game_state.display_text('Select a menu', (255, 255, 255), (self.w / 2, self.h / 2 - 200))
		for sprite in self.button_group.sprites():
			sprite.display_button()
			if sprite.check_button_collision():
				if sprite.index == 'shop':
					self.game_state.current_menu = 'shop'
				if sprite.index == 'ascend':
					self.game_state.current_menu = 'ascend'
				if sprite.index == 'achievements':
					self.game_state.current_menu = 'achievements'
