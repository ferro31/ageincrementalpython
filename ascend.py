import pygame
import os
from button import Button
from timer import Timer
from tree import Tree
import random
from Notation import notate


class Ascend:
	def __init__(self, win, wh, game_state):
		self.font = pygame.font.Font(os.getcwd() + '/assets/font.ttf', 20)

		self.left_mouse_debounce = False

		self.win = win
		self.w, self.h = wh
		self.game_state = game_state
		self.shop_menu = self.game_state.shop_menu
		self.tree = Tree(self.font, self.win, (self.w / 2, self.h / 2 + 330), self.game_state)
		self.tree.load_pos()
		self.shop_menu.tree = self.tree

		self.button_group = pygame.sprite.Group()
		self.back_button = Button((950, self.h / 2 - 200), (10, 10), 'back', win, self.font, (2, 2), "Back")
		self.button_group.add(self.back_button)
		self.ascend_button = Button((self.w / 2, self.h / 2 - 30), (10, 10), 'ascend', win, self.font, (2, 2), "Ascend")
		self.button_group.add(self.ascend_button)

	def game_loop(self):
		self.game_state.display_text('Ascension', (255, 255, 255), (self.w / 2, self.h / 2 - 200))
		self.game_state.display_text('Ascension resets EVERYTHING, but gives you ap which you can spend on OP upgrades', (255, 255, 255), (self.w / 2, self.h / 2 - 150))
		self.game_state.display_text(f'You can ascend right now for', (255, 255, 255), (self.w / 2, self.h / 2 - 100))
		self.game_state.display_text(f'{notate(self.game_state.ap_gain, self.game_state.notation_list)} ap', (255, 255, 255), (self.w / 2, self.h / 2 - 70))
		self.game_state.display_text(f'Currently you have: {notate(self.game_state.ap, self.game_state.notation_list)} ap', (255, 255, 255), (self.w / 2, self.h / 2))
		for sprite in self.button_group.sprites():
			sprite.display_button()
			if sprite.check_button_collision():
				if sprite.index == 'back':
					self.game_state.current_menu = 'none'
				if sprite.index == 'ascend':
					self.game_state.ap += self.game_state.ap_gain
					self.game_state.life_points = 0
					self.game_state.committed_sudoku = True
					self.shop_menu.ascend()
		self.tree.points = self.game_state.ap
		self.tree.events = self.game_state.events
		self.tree.game_loop()
		pygame.draw.rect(self.win, (255, 255, 255), pygame.Rect(25, 420, self.w - 50, 370), width=1)

		self.game_state.mastery = 0.3
		self.game_state.mastery += self.tree.find_node('Mastery').level / 100
