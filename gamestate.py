import pygame
import os
from button import Button
from timer import Timer
import random
from Notation import notate
from shop_menu import ShopMenu
from none import none
from ascend import Ascend
import jsonpickle as pickle
from achivements import Achievements


class GameState:
	def __init__(self, win, wh):
		self.current = 'normal'
		self.events = []
		self.font = pygame.font.Font(os.getcwd() + '/assets/font.ttf', 20)
		self.first_run = True
		self.last_current = ''

		self.left_mouse_debounce = False

		self.x_img = pygame.image.load(os.getcwd() + '/assets/X.png')
		self.x_img = pygame.transform.scale(self.x_img, (32, 32))
		self.check_img = pygame.image.load(os.getcwd() + '/assets/check.png')
		self.check_img = pygame.transform.scale(self.check_img, (32, 32))

		self.mastery = 0.3

		self.win = win
		self.w, self.h = wh
		self.age = 0
		self.age_timer = Timer(100, self.age_go_up, True)
		self.start_button = Button((self.w / 2, self.h / 2 - 350), (10, 10), 'start_button', win, self.font, (2, 2), "Start Life")
		self.sudoku_button = Button((self.w / 2, self.h / 2 - 350), (10, 10), 'sudoku_button', win, self.font, (2, 2), "Commit Sudoku", color=[(255, 180, 180), (220, 145, 145), (200, 125, 125)])

		self.autoaliver_button_group = pygame.sprite.Group()
		self.x_button = Button((self.w / 2 + 75, self.h / 2 - 345), (10, 10), 'x', win, self.font, (2, 2), img=self.x_img)
		self.checkmark_button = Button((self.w / 2 + 75, self.h / 2 - 345), (10, 10), 'check', win, self.font, (2, 2), img=self.check_img)
		self.autoaliver_button_group.add(self.x_button)
		self.autoaliver_button_group.add(self.checkmark_button)

		self.button_group = pygame.sprite.Group()
		self.button_group.add(self.start_button)
		self.button_group.add(self.sudoku_button)
		self.save_button = Button((100, 50), (10, 10), 'save', win, self.font, (2, 2), "Save Game")
		self.button_group.add(self.save_button)

		self.autoalive = False
		self.autoalive_interval = 6000

		self.max_span = 20
		self.base_max_span = 20
		self.aging_speed = 1
		self.base_aging_speed = 1
		self.increment_event = pygame.USEREVENT + 1
		self.max_increment_interval_ms = 50
		pygame.time.set_timer(self.increment_event, self.max_increment_interval_ms)
		self.current_lifespan = random.randint(int(self.max_span * 0.3), self.max_span)
		self.alive = False

		self.autoalive_timer = Timer(self.autoalive_interval, self.autoalivefunc, loop=True)
		self.autoalive_timer.activate()

		self.prev_time = pygame.time.get_ticks()

		self.life_points = 0 #int('9'*150)

		self.notation_list = ['K', 'M', 'B', 'T', 'Qd', 'Qn', 'Sx', 'Sp', 'Oc', 'No']

		self.current_menu = 'none'

		self.committed_sudoku = False

		self.shop_menu = ShopMenu(self.win, (self.w, self.h), self)
		self.shop_menu.check_shop_item_width(True)
		self.none = none(self.win, (self.w, self.h), self)
		self.ascend = Ascend(self.win, (self.w, self.h), self)
		self.achievements = Achievements(self.win, self.font, self)

		self.ap = 0
		self.ap_gain = 0

	def autoalivefunc(self):
		self.age = 0
		self.start_button.active = False
		self.alive = True
		self.prev_time = pygame.time.get_ticks()
		self.current_lifespan = random.randint(int(self.max_span * self.mastery), self.max_span)

	def age_go_up(self, dt):
		self.age += self.aging_speed * (dt / 1000)
		if self.age > self.max_span:
			self.age = self.max_span

	def convert_to_seconds(self, time_str):
		time_units = {
			'second': 1,
			'minute': 60,
			'hour': 60 * 60,
			'day': 60 * 60 * 24,
			'week': 60 * 60 * 24 * 7,
			'month': 60 * 60 * 24 * 30,
			'year': 60 * 60 * 24 * 365
		}
		total_seconds = 0
		words = time_str.split()
		i = 0
		while i < len(words):
			try:
				value = int(words[i])
				unit = words[i + 1].rstrip('s')
				if unit not in time_units:
					raise ValueError(f"Invalid unit of time: {unit}")
				total_seconds += value * time_units[unit]
				i += 2
			except (ValueError, IndexError):
				i += 1
				continue
		return total_seconds

	def format_time(self, seconds):
		intervals = (
			('years', 31536000),
			('months', 2592000),
			('weeks', 604800),
			('days', 86400),
			('hours', 3600),
			('minutes', 60),
			('seconds', 1)
		)
		result = []
		for name, count in intervals:
			value = seconds // count
			if value:
				seconds -= value * count
				if value == 1:
					name = name.rstrip('s')
				result.append(f"{notate(int(value), self.notation_list)} {name}")
		return result

	def format_time2(self, num):
		if num < 1:
			return '0 secondss'
		text = ''
		for i, item in enumerate(self.format_time(num)):
			if i >= 2:
				break
			text += f'{item} '
		return text

	def display_text(self, text, color, pos):
		text = self.font.render(text, True, color)
		rect = text.get_rect()
		rect.center = pos if pos[0] is not 'center' else (self.w / 2, self.h / 2 - pos[1])
		self.win.blit(text, rect)

	def shop_menu_func(self):
		self.shop_menu.draw_menu_border()
		self.shop_menu.check_shop_item_width(self.first_run)
		self.shop_menu.check_button()
		self.shop_menu.game_loop()

	def none_menu_func(self):
		self.none.game_loop()

	def ascend_menu_func(self):
		self.ascend.game_loop()

	def achievement_menu_func(self):
		self.achievements.game_loop()

	def check_button(self):
		for sprite in self.autoaliver_button_group.sprites():
			if self.shop_menu.upgrade_buttons['1'][8][0] >= 1:
				if sprite.index == 'x' and not self.autoalive and not self.alive:
					sprite.display_button()
				if sprite.index == 'check' and self.autoalive and not self.alive:
					sprite.display_button()
				if sprite.check_button_collision():
					if sprite.index == 'x' and not self.autoalive and not self.alive and not self.left_mouse_debounce:
						self.autoalive = True
						sprite.display_button()
						self.left_mouse_debounce = True
					if sprite.index == 'check' and self.autoalive and not self.alive and not self.left_mouse_debounce:
						self.autoalive = False
						sprite.display_button()
						self.left_mouse_debounce = True

	def save(self):
		with open(os.getcwd() + '/player_data.json', mode='w') as f:
			data = {
				'base_age': self.base_aging_speed,
				'base_span': self.base_max_span,
				'lp': self.life_points,
				'ap': self.ap,
				'mastery': self.mastery,
				'aging_speed_buttons': self.shop_menu.aging_speed_buttons,
				'lifespan_buttons': self.shop_menu.lifespan_buttons,
				'upgrade_buttons': self.shop_menu.upgrade_buttons,
				'auto_alive_things': [self.autoalive, self.autoalive_interval],
				'all_nodes': self.ascend.tree.get_levels()
			}
			f.write(pickle.encode(data))

	def load(self):
		with open(os.getcwd() + '/player_data.json', mode='r') as f:
			data = pickle.decode(f.read())
			self.base_aging_speed = data['base_age']
			self.base_max_span = data['base_span']
			self.life_points = data['lp']
			self.ap = data['ap']
			self.mastery = data['mastery']
			for index, item in enumerate(self.shop_menu.aging_speed_buttons.keys()):
				self.shop_menu.aging_speed_buttons[item][8][0] = data['aging_speed_buttons'][item][8][0]
				self.shop_menu.aging_speed_buttons[item][8][1] = data['aging_speed_buttons'][item][8][1]
			for index, item in enumerate(self.shop_menu.lifespan_buttons.keys()):
				self.shop_menu.lifespan_buttons[item][8][0] = data['lifespan_buttons'][item][8][0]
				self.shop_menu.lifespan_buttons[item][8][1] = data['lifespan_buttons'][item][8][1]
			for index, item in enumerate(self.shop_menu.upgrade_buttons.keys()):
				self.shop_menu.upgrade_buttons[item][8][0] = data['upgrade_buttons'][item][8][0]
				self.shop_menu.upgrade_buttons[item][8][1] = data['upgrade_buttons'][item][8][1]
			self.autoalive, self.autoalive_interval = data['auto_alive_things'][0], data['auto_alive_things'][1]
			self.autoalive_timer.duration = self.autoalive_interval
			self.shop_menu.upgrade_buttons['1'][7][2][0] = self.font.render(f'Currently: {self.autoalive_interval // 1000}s', True, (255, 255, 255))
			self.ascend.tree.load_levels(data['all_nodes'])

	def check_vars(self):
		self.ap_gain = max(0, int((self.life_points / 10000) ** 0.8))

	def game_loop(self):
		self.shop_menu.check_all_vars()
		if self.current != self.last_current:
			self.first_run = True
		else:
			self.first_run = False
		self.last_current = self.current
		for event in self.events:
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == self.increment_event and self.alive:
				current_time = pygame.time.get_ticks()
				dt = current_time - self.prev_time
				self.age_go_up(dt)
				self.prev_time = current_time
		if self.current == 'normal':
			if not self.alive and self.autoalive:
				self.autoalive_timer.update()
			else:
				self.autoalive_timer.start_time = pygame.time.get_ticks()
			if self.first_run:
				if not os.stat(os.getcwd() + '/player_data.json').st_size == 0:
					self.load()
			self.win.fill((0, 0, 0))
			pygame.draw.rect(self.win, (43, 54, 48), pygame.Rect(0, 0, self.w, 170))
			pygame.draw.rect(self.win, (43, 45, 54), pygame.Rect(0, 172, self.w, self.h))
			pygame.draw.line(self.win, (255, 255, 255), (0, 170), (self.w, 170), 3)
			self.display_text(f'Age: {self.format_time2(self.age)[:-1]}',
							  (255, 255, 255) if self.alive else (255, 100, 100), ('center', 300))
			self.display_text(f'+{self.format_time2(self.aging_speed)[:-1]}/sec',
							  (255, 255, 255) if self.alive else (255, 100, 100), ('center', 275))
			self.display_text(f'Lifespan: {self.format_time2(self.max_span * self.mastery)}~ {self.format_time2(self.max_span)}', (255, 255, 255) if self.alive else (255, 100, 100),
							  ('center', 250))
			if self.current_menu == 'none':
				self.none_menu_func()
			elif self.current_menu == 'shop':
				self.shop_menu_func()
			elif self.current_menu == 'ascend':
				self.ascend_menu_func()
			self.achievement_menu_func()
			self.check_button()
			self.check_vars()
			for sprite in self.button_group.sprites():
				if sprite.index == 'sudoku_button' and not self.alive: continue
				sprite.display_button()
				if sprite.check_button_collision():
					if sprite.index == 'start_button' and self.start_button.active and not self.left_mouse_debounce:
						self.age = 0
						self.age_timer.activate()
						self.start_button.active = False
						self.alive = True
						self.prev_time = pygame.time.get_ticks()
						self.current_lifespan = random.randint(int(self.max_span * 0.3), self.max_span)
						self.left_mouse_debounce = True
					if sprite.index == 'sudoku_button' and self.alive and not self.left_mouse_debounce:
						self.alive = False
						self.left_mouse_debounce = True
						self.committed_sudoku = True
					if sprite.index == 'save':
						self.save()

			if (self.age >= self.current_lifespan and self.alive) or self.committed_sudoku:
				self.alive = False
				self.age_timer.deactivate()
				self.start_button.active = True
				self.life_points += round((self.age / 10) * (1 + (self.achievements.owned / 100)))
				self.committed_sudoku = False

			if not pygame.mouse.get_pressed()[0]:
				self.left_mouse_debounce = False
