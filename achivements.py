import pygame
from button import Button

pygame.init()


class Achievement:
	def __init__(self, name, description, goals, variables, game_state):
		self.name = name
		self.description = description
		self.goals = goals
		self.progress = 0
		self.earned = False
		self.x = 0
		self.y = 0
		self.variables = variables
		self.game_state = game_state

	def check_progress(self):
		self.progress = [getattr(self.game_state, variable) >= self.goals[ind] for ind, variable in enumerate(self.variables)]
		if self.name == 'Second Achievement':
			print(self.progress, self.name)
		if all(self.progress) and not self.earned:
			self.earned = True

	def draw(self, screen):
		box_color = (0, 255, 0) if self.earned else (255, 0, 0)
		pygame.draw.rect(screen, box_color, (self.x, self.y, 50, 50))

	def set_position(self, x, y):
		self.x = x
		self.y = y

	def is_hovered(self, mouse_pos):
		return self.x <= mouse_pos[0] <= self.x + 50 and self.y <= mouse_pos[1] <= self.y + 50

	def draw_tooltip(self, screen, font):
		tooltip_text2 = font.render(f"{self.name}", True, (255, 255, 255))
		tooltip_text3 = font.render(f"{self.description}", True, (255, 255, 255))
		tooltip_rect = max(tooltip_text2.get_rect(), tooltip_text3.get_rect())
		tooltip_rect.center = (self.x + 25, self.y - 45)
		tooltip_rect.width += 10
		tooltip_rect.height = 44
		if tooltip_rect.left < 0:
			tooltip_rect.left = 10
		if tooltip_rect.right > 1000:
			tooltip_rect.right = 990
		pygame.draw.rect(screen, (0, 0, 0), tooltip_rect)
		pygame.draw.rect(screen, (255, 255, 255), tooltip_rect, 1)
		screen.blit(tooltip_text2, (tooltip_rect.centerx - tooltip_text2.get_width() // 2, tooltip_rect.centery - 22))
		screen.blit(tooltip_text3, (tooltip_rect.centerx - tooltip_text3.get_width() // 2, tooltip_rect.centery - 1))


class Achievements:
	def __init__(self, screen, font, game_state):
		self.screen = screen
		self.font = font
		self.game_state = game_state
		self.achievements = [Achievement(f"10 is a lot, y'know", f"Earn 10 lp", [10], ['life_points'], self.game_state),
							 Achievement(f"Nice", f"Earn 69 lp", [69], ['life_points'], self.game_state),
							 Achievement(f"100? That's nothin'", f"Earn 100 lp", [100], ['life_points'], self.game_state),
							 Achievement(f"Nice^2", f"Earn 420 lp", [420], ['life_points'], self.game_state),
							 Achievement(f"That's rookie numbers", f"Earn 1000 lp", [1000], ['life_points'], self.game_state),
							 Achievement(f"Now we're talking!", f"Earn 10k lp", [10_000], ['life_points'], self.game_state),
							 Achievement(f"Nice^3", f"Earn 69,420 lp", [69_420], ['life_points'], self.game_state),
							 Achievement(f"10^5", f"Earn 100k lp", [100_000], ['life_points'], self.game_state),
							 Achievement(f"Better than bitcoin in 2021!", f"Earn 20m lp", [20_000_000], ['life_points'], self.game_state),
							 Achievement(f"Lp to the moon!", f"Earn 1b lp", [750_000_000], ['life_points'], self.game_state),

							 Achievement(f"Aging a bit", f"Earn 10sec/sec aging speed", [10], ['aging_speed'], self.game_state),
							 Achievement(f"Gettin' old real quick", f"Earn 5min/sec aging speed", [self.game_state.convert_to_seconds('5 minutes')], ['aging_speed'], self.game_state),
							 Achievement(f"Super sanic speed", f"Earn 1h/sec aging speed", [self.game_state.convert_to_seconds('1 hour')], ['aging_speed'], self.game_state),
							 Achievement(f"Slow and steady", f"Earn 12h/sec aging speed", [self.game_state.convert_to_seconds('12 hour')], ['aging_speed'], self.game_state),
							 Achievement(f"Faster than average", f"Earn 2d/sec aging speed", [self.game_state.convert_to_seconds('2 days')], ['aging_speed'], self.game_state),
							 Achievement(f"Lightning fast", f"Earn 1 week/sec aging speed", [self.game_state.convert_to_seconds('1 week')], ['aging_speed'], self.game_state),
							 Achievement(f"Ageless wonder", f"Earn 2 month/sec aging speed", [self.game_state.convert_to_seconds('2 months')], ['aging_speed'], self.game_state),

							 Achievement(f"Newborn", f"Get max 1 min lifespan", [self.game_state.convert_to_seconds('1 minute')], ['max_span'], self.game_state),
							 Achievement(f"Infant", f"Get max 1 hour lifespan", [self.game_state.convert_to_seconds('1 hour')], ['max_span'], self.game_state),
							 Achievement(f"Baby", f"Get max 1 day lifespan", [self.game_state.convert_to_seconds('1 day')], ['max_span'], self.game_state),
							 Achievement(f"Teenager", f"Get max 1 week lifespan", [self.game_state.convert_to_seconds('1 week')], ['max_span'], self.game_state),
							 Achievement(f"Adult", f"Get max 1 year lifespan", [self.game_state.convert_to_seconds('1 year')], ['max_span'], self.game_state),
							 Achievement(f"Centenarian", f"Get max 100 years lifespan", [self.game_state.convert_to_seconds('100 year')], ['max_span'], self.game_state),
							 Achievement(f"Immortal", f"Get max 500 years lifespan", [self.game_state.convert_to_seconds('500 year')], ['max_span'], self.game_state),
							 Achievement(f"Fountain of youth", f"Get max 1k years lifespan", [self.game_state.convert_to_seconds('1000 year')], ['max_span'], self.game_state),
							 Achievement(f"Eternal", f"Get max 10k years lifespan", [self.game_state.convert_to_seconds('10000 year')], ['max_span'], self.game_state)]
		self.button_group = pygame.sprite.Group()
		self.back_button = Button((950, 800 / 2 - 200), (10, 10), 'back', self.game_state.win, self.game_state.font, (2, 2), "Back")
		self.button_group.add(self.back_button)
		self.owned = 0

	def get_owned(self):
		self.owned = 0
		for achievement in self.achievements:
			if all(achievement.progress):
				self.owned += 1

	def check_pos(self):
		x = 50
		y = 300
		for achievement in self.achievements:
			achievement.set_position(x, y)
			achievement.draw(self.screen)
			if achievement.is_hovered(pygame.mouse.get_pos()):
				achievement.draw_tooltip(self.screen, self.font)
			x += 70
			if x > 950:
				x = 50
				y += 70

	def game_loop(self):
		for achievement in self.achievements:
			achievement.check_progress()
		if self.game_state.current_menu == 'achievements':
			self.game_state.display_text('Achievements', (255, 255, 255), ('center', 200))
			self.game_state.display_text('Each achievement gives 1% multi to your life points gain.', (255, 255, 255), ('center', 180))
			self.get_owned()
			self.game_state.display_text(f'Currently: {(self.owned / 100) + 1}x', (255, 255, 255), ('center', 160))
			self.check_pos()
			for sprite in self.button_group.sprites():
				sprite.display_button()
				if sprite.check_button_collision():
					if sprite.index == 'back':
						self.game_state.current_menu = 'none'
