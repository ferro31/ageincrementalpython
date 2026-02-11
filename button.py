import pygame
pygame.font.init()


class Button(pygame.sprite.Sprite):
	def __init__(self, pos, size, index, win, font=pygame.font.Font(None, 30), shadow=(0, 0), text='', img=None, color=[(255, 255, 255), (220, 220, 220), (200, 200, 200)]):
		super().__init__()
		self.pos = pos
		self.orig_pos = pos
		self.size = size
		self.text = text
		self.img = img
		self.shadow = shadow
		self.rect = pygame.Rect(0, 0, 0, 0)
		self.color = color
		self.current_color = color[0]

		self.win = win
		self.font = font

		self.index = index
		self.clicked = False

		self.active = True

	def display_button(self):
		if self.active:
			if self.img is None:
				text_surf = self.font.render(self.text, True, 'Black')
				text_rect = text_surf.get_rect(center=self.pos)
				self.rect = text_rect.inflate(self.size)
				pygame.draw.rect(self.win, 'Black', text_rect.inflate(self.size[0] + self.shadow[0], self.size[1] + self.shadow[1]), 0, 20)
				pygame.draw.rect(self.win, self.current_color, self.rect, 0, 20)
				self.win.blit(text_surf, text_rect)
			else:
				img_rect = self.img.get_rect(center=self.pos)
				self.rect = img_rect.inflate(self.size)
				self.win.blit(self.img, self.rect)

	def check_button_collision(self):
		if self.rect.collidepoint(pygame.mouse.get_pos()):
			self.current_color = self.color[1]
			if pygame.mouse.get_pressed()[0]:
				self.current_color = self.color[2]
			if pygame.mouse.get_pressed()[0] and not self.clicked:
				self.clicked = True
				return True
			elif not pygame.mouse.get_pressed()[0] and self.clicked:
				self.clicked = False
		else:
			self.current_color = self.color[0]
