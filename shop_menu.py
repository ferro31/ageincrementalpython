import pygame
import os
from button import Button
from timer import Timer
import random
from Notation import notate


class ShopMenu:
	def __init__(self, win, wh, game_state):
		self.font = pygame.font.Font(os.getcwd() + '/assets/font.ttf', 20)

		self.left_mouse_debounce = False

		self.win = win
		self.w, self.h = wh

		self.aging_speed_buttons = {
			'1': [Button((100, 400), (10, 10), 'as1', win, self.font, (2, 2), "Buy",
						 color=[(255, 255, 255), (220, 220, 220), (200, 200, 200)]),
				  [(255, 255, 255), pygame.Rect(0, 300, 145, 300), 3, 5],
				  [self.font.render('Time warp', True, (255, 255, 255)), (35, 300)],
				  [self.font.render('Owned:', True, (200, 200, 200)), (60, 390)],
				  [self.font.render('0', True, (255, 255, 255)), (95, 410)],
				  [self.font.render('Cost:', True, (200, 200, 200)), (75, 450)],
				  [self.font.render('0 lp', True, (255, 255, 255)), (82, 470)],
				  [[self.font.render('Increases aging', True, (255, 255, 255)), (82, 520)],
				   [self.font.render('speed (+1 sec/s)', True, (255, 255, 255)), (82, 590)]],
				  [0, 5, 5],
				  [50, 90, 110, 150, 170, 220, 240]],
			'2': [Button((100, 400), (10, 10), 'as2', win, self.font, (2, 2), "Buy",
						 color=[(255, 255, 255), (220, 220, 220), (200, 200, 200)]),
				  [(255, 255, 255), pygame.Rect(0, 300, 145, 300), 3, 5],
				  [self.font.render('Age Accelerator', True, (255, 255, 255)), (35, 350)],
				  [self.font.render('Owned:', True, (200, 200, 200)), (60, 440)],
				  [self.font.render('0', True, (255, 255, 255)), (95, 460)],
				  [self.font.render('Cost:', True, (200, 200, 200)), (75, 500)],
				  [self.font.render('0 lp', True, (255, 255, 255)), (82, 520)],
				  [[self.font.render('Increases aging', True, (255, 255, 255)), (82, 570)],
				   [self.font.render('speed (+15 sec/s)', True, (255, 255, 255)), (82, 590)]],
				  [0, 75, 75],
				  [50, 90, 110, 150, 170, 220, 240]],
			'3': [Button((100, 400), (10, 10), 'as3', win, self.font, (2, 2), "Buy",
						 color=[(255, 255, 255), (220, 220, 220), (200, 200, 200)]),
				  [(255, 255, 255), pygame.Rect(0, 300, 145, 300), 3, 5],
				  [self.font.render('Time machine', True, (255, 255, 255)), (35, 350)],
				  [self.font.render('Owned:', True, (200, 200, 200)), (60, 440)],
				  [self.font.render('0', True, (255, 255, 255)), (95, 460)],
				  [self.font.render('Cost:', True, (200, 200, 200)), (75, 500)],
				  [self.font.render('0 lp', True, (255, 255, 255)), (82, 520)],
				  [[self.font.render('Increases aging', True, (255, 255, 255)), (82, 570)],
				   [self.font.render('speed (+3 min/s)', True, (255, 255, 255)), (82, 590)]],
				  [0, 500, 500],
				  [50, 90, 110, 150, 170, 220, 240]],
			'4': [Button((100, 400), (10, 10), 'as4', win, self.font, (2, 2), "Buy",
						 color=[(255, 255, 255), (220, 220, 220), (200, 200, 200)]),
				  [(255, 255, 255), pygame.Rect(0, 300, 145, 300), 3, 5],
				  [self.font.render('Time dilation', True, (255, 255, 255)), (35, 350)],
				  [self.font.render('Owned:', True, (200, 200, 200)), (60, 440)],
				  [self.font.render('0', True, (255, 255, 255)), (95, 460)],
				  [self.font.render('Cost:', True, (200, 200, 200)), (75, 500)],
				  [self.font.render('0 lp', True, (255, 255, 255)), (82, 520)],
				  [[self.font.render('Increases aging', True, (255, 255, 255)), (82, 570)],
				   [self.font.render('speed (+45 min/s)', True, (255, 255, 255)), (82, 590)]],
				  [0, 5_000, 5000],
				  [50, 90, 110, 150, 170, 220, 240]],
		}
		self.lifespan_buttons = {
			'1': [Button((100, 400), (10, 10), 'ls1', win, self.font, (2, 2), "Buy",
						 color=[(255, 255, 255), (220, 220, 220), (200, 200, 200)]),
				  [(255, 255, 255), pygame.Rect(0, 300, 145, 300), 3, 5],
				  [self.font.render('Vitality+', True, (255, 255, 255)), (35, 300)],
				  [self.font.render('Owned:', True, (200, 200, 200)), (60, 390)],
				  [self.font.render('0', True, (255, 255, 255)), (95, 410)],
				  [self.font.render('Cost:', True, (200, 200, 200)), (75, 450)],
				  [self.font.render('0 lp', True, (255, 255, 255)), (82, 470)],
				  [[self.font.render('Increases', True, (255, 255, 255)), (82, 520)],
				   [self.font.render('lifespan (+10 sec)', True, (255, 255, 255)), (82, 590)]],
				  [0, 5, 5],
				  [50, 90, 110, 150, 170, 220, 240]],
			'2': [Button((100, 400), (10, 10), 'ls2', win, self.font, (2, 2), "Buy",
						 color=[(255, 255, 255), (220, 220, 220), (200, 200, 200)]),
				  [(255, 255, 255), pygame.Rect(0, 300, 145, 300), 3, 5],
				  [self.font.render('Ageless', True, (255, 255, 255)), (35, 350)],
				  [self.font.render('Owned:', True, (200, 200, 200)), (60, 440)],
				  [self.font.render('0', True, (255, 255, 255)), (95, 460)],
				  [self.font.render('Cost:', True, (200, 200, 200)), (75, 500)],
				  [self.font.render('0 lp', True, (255, 255, 255)), (82, 520)],
				  [[self.font.render('Increases', True, (255, 255, 255)), (82, 570)],
				   [self.font.render('lifespan (+2 mins)', True, (255, 255, 255)), (82, 590)]],
				  [0, 75, 75],
				  [50, 90, 110, 150, 170, 220, 240]],
			'3': [Button((100, 400), (10, 10), 'ls3', win, self.font, (2, 2), "Buy",
						 color=[(255, 255, 255), (220, 220, 220), (200, 200, 200)]),
				  [(255, 255, 255), pygame.Rect(0, 300, 145, 300), 3, 5],
				  [self.font.render('Immortal', True, (255, 255, 255)), (35, 350)],
				  [self.font.render('Owned:', True, (200, 200, 200)), (60, 440)],
				  [self.font.render('0', True, (255, 255, 255)), (95, 460)],
				  [self.font.render('Cost:', True, (200, 200, 200)), (75, 500)],
				  [self.font.render('0 lp', True, (255, 255, 255)), (82, 520)],
				  [[self.font.render('Increases', True, (255, 255, 255)), (82, 570)],
				   [self.font.render('lifespan (+40 mins)', True, (255, 255, 255)), (82, 590)]],
				  [0, 500, 500],
				  [50, 90, 110, 150, 170, 220, 240]],
			'4': [Button((100, 400), (10, 10), 'ls4', win, self.font, (2, 2), "Buy",
						 color=[(255, 255, 255), (220, 220, 220), (200, 200, 200)]),
				  [(255, 255, 255), pygame.Rect(0, 300, 145, 300), 3, 5],
				  [self.font.render('Fountain of youth', True, (255, 255, 255)), (35, 350)],
				  [self.font.render('Owned:', True, (200, 200, 200)), (60, 440)],
				  [self.font.render('0', True, (255, 255, 255)), (95, 460)],
				  [self.font.render('Cost:', True, (200, 200, 200)), (75, 500)],
				  [self.font.render('0 lp', True, (255, 255, 255)), (82, 520)],
				  [[self.font.render('Increases', True, (255, 255, 255)), (82, 570)],
				   [self.font.render('lifespan (+3 hours)', True, (255, 255, 255)), (82, 590)]],
				  [0, 5000, 5000],
				  [50, 90, 110, 150, 170, 220, 240]],
		}
		self.upgrade_buttons = {
			'1': [Button((100, 400), (10, 10), 'up1', win, self.font, (2, 2), "Buy",
						 color=[(255, 255, 255), (220, 220, 220), (200, 200, 200)]),
				  [(255, 255, 255), pygame.Rect(0, 300, 145, 300), 3, 5],
				  [self.font.render('Autoaliver', True, (255, 255, 255)), (35, 300)],
				  [self.font.render('Owned:', True, (200, 200, 200)), (60, 390)],
				  [self.font.render('0/5', True, (255, 255, 255)), (95, 410)],
				  [self.font.render('Cost:', True, (200, 200, 200)), (75, 450)],
				  [self.font.render('0 lp', True, (255, 255, 255)), (82, 470)],
				  [[self.font.render('-1s delay/upgrade', True, (255, 255, 255)), (82, 520)],
				   [self.font.render('5s default', True, (255, 255, 255)), (82, 590)],
				   [self.font.render('DISABLED', True, (255, 255, 255)), (82, 590)]],
				  [0, 100, 5, 100],
				  [50, 90, 110, 150, 170, 220, 240]]
		}

		self.button_group = pygame.sprite.Group()
		self.back_button = Button((950, self.h / 2 - 200), (10, 10), 'back', win, self.font, (2, 2), "Back")
		self.button_group.add(self.back_button)

		self.tree = None

		self.lifespan_button_group = pygame.sprite.Group()
		self.aging_speed_button_group = pygame.sprite.Group()
		self.upgrade_button_group = pygame.sprite.Group()
		for value in self.aging_speed_buttons.values():
			self.aging_speed_button_group.add(value[0])
		for value in self.lifespan_buttons.values():
			self.lifespan_button_group.add(value[0])
		for value in self.upgrade_buttons.values():
			self.upgrade_button_group.add(value[0])

		self.nav_button_groups = pygame.sprite.Group()
		self.aging_speed_button_nav = Button((100, 710), (10, 10), 'aging_speed_nav', win, self.font, (2, 2),
											 "Aging Speed", color=[(200, 200, 255), (190, 190, 220), (170, 170, 200)])
		self.nav_button_groups.add(self.aging_speed_button_nav)
		self.lifespan_button_nav = Button((250, 710), (10, 10), 'lifespan_nav', win, self.font, (2, 2), "Lifespan",
										  color=[(200, 200, 255), (190, 190, 220), (170, 170, 200)])
		self.nav_button_groups.add(self.lifespan_button_nav)
		self.upgrade_button_nav = Button((390, 710), (10, 10), 'upgrades_nav', win, self.font, (2, 2), "Upgrades",
										 color=[(200, 200, 255), (190, 190, 220), (170, 170, 200)])
		self.nav_button_groups.add(self.upgrade_button_nav)
		self.current_nav = 'aging_speed'
		self.current_shop_menu = self.aging_speed_buttons
		self.current_shop_button_group = self.aging_speed_button_group

		self.game_state = game_state

		self.buy_amount_button_group = pygame.sprite.Group()
		buy_amount_button = Button((75, 200), (10, 10), 'buy_amount', win, self.font, (2, 2), "Amount: 1x", color=[(200, 200, 255), (190, 190, 220), (170, 170, 200)])
		self.buy_amount_button_group.add(buy_amount_button)
		self.buy_amount_curr = 0
		self.buy_amount = 0
		self.possible_buy_amount = [1, 5, 10, 25, 'max']

	def draw_menu_border(self):
		current_menu = ''
		if self.current_nav == 'aging_speed': current_menu = 'Aging Speed'
		elif self.current_nav == 'lifespan': current_menu = 'Lifespan'
		elif self.current_nav == 'upgrades': current_menu = 'Upgrades'
		shop_text = self.font.render(f'Shop - {current_menu}', True, (255, 255, 255))
		shop_rect = shop_text.get_rect()
		shop_rect.center = (self.w // 2, 200)
		self.win.blit(shop_text, shop_rect)

	def check_shop_item_width(self, first=False):
		if first:
			for key, value in self.aging_speed_buttons.items():
				list = []
				for ind, item in enumerate(self.aging_speed_buttons[key]):
					if ind == 7:
						for item2 in item:
							if not isinstance(item2[0], pygame.Surface): continue
							list.append(item2[0].get_width())
					if ind in [0, 1, 7, 8, 9]: continue
					list.append(item[0].get_width())
				self.aging_speed_buttons[key][1][1].width = max(list) + 20

			for key, value in self.lifespan_buttons.items():
				list = []
				for ind, item in enumerate(self.lifespan_buttons[key]):
					if ind == 7:
						for item2 in item:
							if not isinstance(item2[0], pygame.Surface): continue
							list.append(item2[0].get_width())
					if ind in [0, 1, 7, 8, 9]: continue
					list.append(item[0].get_width())
				self.lifespan_buttons[key][1][1].width = max(list) + 20

			for key, value in self.upgrade_buttons.items():
				list = []
				for ind, item in enumerate(self.lifespan_buttons[key]):
					if ind == 7:
						for item2 in item:
							if not isinstance(item2[0], pygame.Surface): continue
							list.append(item2[0].get_width())
					if ind in [0, 1, 7, 8, 9]: continue
					list.append(item[0].get_width())
				self.upgrade_buttons[key][1][1].width = max(list) + 20
		for key, value in self.current_shop_menu.items():
			list = []
			for ind, item in enumerate(self.current_shop_menu[key]):
				if ind == 7:
					for item2 in item:
						if not isinstance(item2[0], pygame.Surface): continue
						list.append(item2[0].get_width())
				if ind in [0, 1, 7, 8, 9]: continue
				list.append(item[0].get_width())
			self.current_shop_menu[key][1][1].width = max(list) + 20

	def check_button(self):
		if self.current_nav == 'aging_speed':
			self.current_shop_menu = self.aging_speed_buttons
			self.current_shop_button_group = self.aging_speed_button_group
			self.aging_speed_button_nav.color = [(255, 255, 255), (220, 220, 220), (200, 200, 200)]
			self.upgrade_button_nav.color = [(200, 200, 255), (190, 190, 220), (170, 170, 200)]
			self.lifespan_button_nav.color = [(200, 200, 255), (190, 190, 220), (170, 170, 200)]
		if self.current_nav == 'lifespan':
			self.current_shop_menu = self.lifespan_buttons
			self.current_shop_button_group = self.lifespan_button_group
			self.lifespan_button_nav.color = [(255, 255, 255), (220, 220, 220), (200, 200, 200)]
			self.aging_speed_button_nav.color = [(200, 200, 255), (190, 190, 220), (170, 170, 200)]
			self.upgrade_button_nav.color = [(200, 200, 255), (190, 190, 220), (170, 170, 200)]
		if self.current_nav == 'upgrades':
			self.current_shop_menu = self.upgrade_buttons
			self.current_shop_button_group = self.upgrade_button_group
			self.lifespan_button_nav.color = [(200, 200, 255), (190, 190, 220), (170, 170, 200)]
			self.aging_speed_button_nav.color = [(200, 200, 255), (190, 190, 220), (170, 170, 200)]
			self.upgrade_button_nav.color = [(255, 255, 255), (220, 220, 220), (200, 200, 200)]
		rect = pygame.Rect(0, 0, self.w - 50, 130)
		rect.left = 25
		rect.bottom = self.h - 20
		pygame.draw.rect(self.win, (100, 100, 200), rect, border_radius=50)
		for sprite in self.nav_button_groups.sprites():
			if sprite.check_button_collision():
				if sprite.index == 'aging_speed_nav':
					self.current_nav = 'aging_speed'
				if sprite.index == 'lifespan_nav':
					self.current_nav = 'lifespan'
				if sprite.index == 'upgrades_nav':
					self.current_nav = 'upgrades'
			if sprite.rect.collidepoint(pygame.mouse.get_pos()) and sprite.clicked:
				sprite.pos = (sprite.orig_pos[0], sprite.orig_pos[1] + 3)
				rect = pygame.Rect(0, 0, sprite.rect.width + 20, 45)
				rect.left = sprite.rect.left - 10
				rect.bottom = self.h - 57
				pygame.draw.rect(self.win, (50, 50, 100), rect, border_radius=50)
			else:
				sprite.pos = sprite.orig_pos
				rect = pygame.Rect(0, 0, sprite.rect.width + 20, 50)
				rect.left = sprite.rect.left - 10
				rect.bottom = self.h - 57
				pygame.draw.rect(self.win, (50, 50, 100), rect, border_radius=50)
			sprite.display_button()
		current_x = 18
		for ind2, ind in enumerate(self.current_shop_menu.keys()):
			self.current_shop_menu[ind][1][1].left = current_x + 10
			current_x = self.current_shop_menu[ind][1][1].right

			if self.game_state.life_points >= self.current_shop_menu[ind][8][1]:
				self.current_shop_menu[ind][0].color = [(200, 255, 200), (165, 220, 165), (145, 200, 145)]
			else:
				self.current_shop_menu[ind][0].color = [(255, 200, 200), (220, 165, 165), (200, 145, 145)]

	def check_all_vars(self):
		self.game_state.aging_speed = self.game_state.base_aging_speed
		self.game_state.aging_speed += self.aging_speed_buttons['1'][8][0] * self.game_state.convert_to_seconds('1 seconds')
		self.game_state.aging_speed += self.aging_speed_buttons['2'][8][0] * self.game_state.convert_to_seconds('15 seconds')
		self.game_state.aging_speed += self.aging_speed_buttons['3'][8][0] * self.game_state.convert_to_seconds('3 minute')
		self.game_state.aging_speed += self.aging_speed_buttons['4'][8][0] * self.game_state.convert_to_seconds('45 minute')
		self.game_state.aging_speed *= 1 + self.tree.find_node('Aging speed').level / 20
		self.game_state.max_span = self.game_state.base_max_span
		self.game_state.max_span += self.lifespan_buttons['1'][8][0] * self.game_state.convert_to_seconds('10 seconds')
		self.game_state.max_span += self.lifespan_buttons['2'][8][0] * self.game_state.convert_to_seconds('2 minutes')
		self.game_state.max_span += self.lifespan_buttons['3'][8][0] * self.game_state.convert_to_seconds('40 minutes')
		self.game_state.max_span += self.lifespan_buttons['4'][8][0] * self.game_state.convert_to_seconds('3 hours')

	def ascend(self):
		for ind in range(3):
			if ind == 0:
				for item in self.aging_speed_buttons.values():
					item[8][0] = 0
					item[8][1] = item[8][2]
			if ind == 1:
				for item in self.lifespan_buttons.values():
					item[8][0] = 0
					item[8][1] = item[8][2]
			if ind == 2:
				for item in self.upgrade_buttons.values():
					item[8][0] = 0
					item[8][1] = item[8][3]
		self.check_all_vars()

	def game_loop(self):
		self.game_state.display_text(f'Life points: {notate(self.game_state.life_points, self.game_state.notation_list)}', (177, 177, 177),
						  ('center', 175))
		for sprite in self.current_shop_button_group.sprites():
			for ind, value in enumerate(self.current_shop_menu[sprite.index[2:]]):
				if ind == 1:
					pygame.draw.rect(self.win, (50, 50, 50), value[1], 0, value[3])
					pygame.draw.rect(self.win, value[0], value[1], value[2], value[3])
					continue
				if isinstance(value, Button):
					if self.current_shop_menu == self.upgrade_buttons and \
							self.current_shop_menu[str(sprite.index[2:3])][8][0] >= \
							self.current_shop_menu[str(sprite.index[2:3])][8][2]:
						rect = value.rect
						rect.centerx = self.current_shop_menu[str(sprite.index[2:3])][1][1].centerx - value.size[
							0] / 2 + 6
						rect.centery = self.current_shop_menu[str(sprite.index[2:3])][1][1].top + 190
						value.pos = (rect.centerx, rect.centery)
						value.color = [(200, 200, 200), (200, 200, 200), (200, 200, 200)]
					else:
						rect = value.rect
						rect.centerx = self.current_shop_menu[str(sprite.index[2:3])][1][1].centerx - value.size[
							0] / 2 + 6
						rect.centery = self.current_shop_menu[str(sprite.index[2:3])][1][1].top + 190
						value.pos = (rect.centerx, rect.centery)
					continue
				if ind == 7:
					for ind2, item in enumerate(value):
						if type(item[0]) == int: continue
						rect = item[0].get_rect()
						rect.centerx = self.current_shop_menu[str(sprite.index[2:3])][1][1].centerx - rect.width / 2
						rect.centery = self.current_shop_menu[str(sprite.index[2:3])][1][1].top + 220 + (20 * ind2)
						self.current_shop_menu[str(sprite.index[2:3])][ind][ind2][1] = rect.center
						self.win.blit(item[0], item[1])
					continue
				if ind == 8: continue
				if ind == 9: continue
				if ind == 4:
					if self.current_shop_menu == self.upgrade_buttons:
						self.current_shop_menu[str(sprite.index[2:3])][ind][0] = self.font.render(
							f'{notate(self.current_shop_menu[str(sprite.index[2:3])][8][0], self.game_state.notation_list)}/{self.current_shop_menu[str(sprite.index[2:3])][8][2]}',
							True, (255, 255, 255))
					else:
						self.current_shop_menu[str(sprite.index[2:3])][ind][0] = self.font.render(
							f'{notate(self.current_shop_menu[str(sprite.index[2:3])][8][0], self.game_state.notation_list)}', True,
							(255, 255, 255))
				if ind == 6:
					if self.current_shop_menu == self.upgrade_buttons and \
							self.current_shop_menu[str(sprite.index[2:3])][8][0] >= \
							self.current_shop_menu[str(sprite.index[2:3])][8][2]:
						self.current_shop_menu[str(sprite.index[2:3])][ind][0] = self.font.render(
							f'MAX',
							True, (255, 255, 255))
					else:
						self.current_shop_menu[str(sprite.index[2:3])][ind][0] = self.font.render(
							f'{notate(self.current_shop_menu[str(sprite.index[2:3])][8][1], self.game_state.notation_list)} lp',
							True, (255, 255, 255))
				rect = value[0].get_rect()
				rect.centerx = self.current_shop_menu[str(sprite.index[2:3])][1][1].centerx - rect.width / 2
				rect.centery = self.current_shop_menu[str(sprite.index[2:3])][1][1].top + \
							   self.current_shop_menu[str(sprite.index[2:3])][9][ind] - 100
				self.current_shop_menu[str(sprite.index[2:3])][ind][1] = rect.center
				self.win.blit(value[0], value[1])
			if sprite.check_button_collision():
				if (sprite.index[0:2] == 'as' or sprite.index[0:2] == 'ls') and self.game_state.life_points >= self.current_shop_menu[str(sprite.index[2:3])][8][1] and not self.left_mouse_debounce:
					if self.buy_amount_curr != 'max':
						amount = 0
						while self.game_state.life_points >= self.current_shop_menu[str(sprite.index[2:3])][8][1]:
							amount += 1
							self.game_state.life_points -= self.current_shop_menu[str(sprite.index[2:3])][8][1]
							self.current_shop_menu[str(sprite.index[2:3])][8][0] += 1
							self.current_shop_menu[str(sprite.index[2:3])][8][1] = int(self.current_shop_menu[str(sprite.index[2:3])][8][1] * 1.2)
							if amount >= self.buy_amount_curr:
								break
					else:
						while self.game_state.life_points >= self.current_shop_menu[str(sprite.index[2:3])][8][1]:
							self.game_state.life_points -= self.current_shop_menu[str(sprite.index[2:3])][8][1]
							self.current_shop_menu[str(sprite.index[2:3])][8][0] += 1
							self.current_shop_menu[str(sprite.index[2:3])][8][1] = int(self.current_shop_menu[str(sprite.index[2:3])][8][1] * 1.2)
				if sprite.index[0:2] == 'up' and self.game_state.life_points >= self.current_shop_menu[str(sprite.index[2:3])][8][1] and not self.left_mouse_debounce and self.current_shop_menu[str(sprite.index[2:3])][8][0] < self.current_shop_menu[str(sprite.index[2:3])][8][2]:
					if self.buy_amount_curr != 'max':
						amount = 0
						while self.game_state.life_points >= self.current_shop_menu[str(sprite.index[2:3])][8][1] and self.current_shop_menu[str(sprite.index[2:3])][8][0] < self.current_shop_menu[str(sprite.index[2:3])][8][2]:
							self.game_state.life_points -= self.current_shop_menu[str(sprite.index[2:3])][8][1]
							self.current_shop_menu[str(sprite.index[2:3])][8][0] += 1
							self.game_state.autoalive_interval -= 1000
							self.game_state.autoalive_timer.duration = self.game_state.autoalive_interval
							self.current_shop_menu[str(sprite.index[2:3])][8][1] = int(
								self.current_shop_menu[str(sprite.index[2:3])][8][1] * 10)
							self.current_shop_menu[str(sprite.index[2:3])][7][2][0] = self.font.render(
								f'Currently: {self.game_state.autoalive_interval // 1000}s', True, (255, 255, 255))
							if amount >= self.buy_amount_curr:
								break
							amount += 1
					else:
						while self.game_state.life_points >= self.current_shop_menu[str(sprite.index[2:3])][8][1] and self.current_shop_menu[str(sprite.index[2:3])][8][0] < self.current_shop_menu[str(sprite.index[2:3])][8][2]:
							self.game_state.life_points -= self.current_shop_menu[str(sprite.index[2:3])][8][1]
							self.current_shop_menu[str(sprite.index[2:3])][8][0] += 1
							self.game_state.autoalive_interval -= 1000
							self.game_state.autoalive_timer.duration = self.game_state.autoalive_interval
							self.current_shop_menu[str(sprite.index[2:3])][8][1] = int(
								self.current_shop_menu[str(sprite.index[2:3])][8][1] * 10)
							self.current_shop_menu[str(sprite.index[2:3])][7][2][0] = self.font.render(
								f'Currently: {self.game_state.autoalive_interval // 1000}s', True, (255, 255, 255))
			sprite.display_button()
		for sprite in self.button_group.sprites():
			sprite.display_button()
			if sprite.check_button_collision():
				if sprite.index == 'back':
					self.game_state.current_menu = 'none'
		for sprite in self.buy_amount_button_group.sprites():
			sprite.display_button()
			if sprite.check_button_collision():
				if sprite.index == 'buy_amount':
					self.buy_amount += 1
					self.buy_amount_curr = self.possible_buy_amount[self.buy_amount % 5]
					sprite.text = f'Amount: {self.buy_amount_curr}{"x" if self.buy_amount_curr != "max" else ""}'
					print(self.buy_amount_curr)
