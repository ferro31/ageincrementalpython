import pygame
from gamestate import GameState

pygame.font.init()
pygame.mixer.init()

w, h = 1000, 800
win = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

age = 0

game = GameState(win, (w, h))
while True:
	clock.tick(60)
	game.events = pygame.event.get()
	game.game_loop()
	pygame.display.update()
