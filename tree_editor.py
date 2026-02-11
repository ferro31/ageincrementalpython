import pygame
import os
import jsonpickle as pickle
import math

pygame.init()
screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()


def update_buyable_nodes(node, buyable_nodes):
	if node.cost <= points and node not in buyable_nodes and node.level < node.max_level:
		node.color = (0, 255, 0)
		buyable_nodes.append(node)
	elif node.cost > points and node in buyable_nodes and node.level < node.max_level:
		node.color = (170, 49, 86)
		buyable_nodes.remove(node)
	for child in node.children:
		buyable_nodes = update_buyable_nodes(child, buyable_nodes)
	return buyable_nodes


def sort_nodes(nodes):
	def node_sort_key(node):
		if node.is_mouse_over(*pygame.mouse.get_pos()):
			return 0
		else:
			return 1

	return sorted(nodes, key=node_sort_key)


def draw_node(node):
	list = []
	for child in node.children:
		list2 = []
		for item in all_nodes:
			list2.append(item.name)
		if child.name not in list2:
			all_nodes.append(child)
		list.append(child)
		pygame.draw.line(screen, child.color, (node.x, node.y + 10), (child.x, child.y - 10), 4)
	for child in list:
		draw_node(child)

	node_color = node.color
	if node.is_mouse_over(*pygame.mouse.get_pos()):
		if not node.parents_bigger_than_one:
			node_color = (255, 255, 153)

		if node.level < node.max_level:
			tooltip_text = font.render(f"Level: {node.level}/{node.max_level}\nCost: {node.cost}", True,
									   (255, 255, 255))
		else:
			tooltip_text = font.render(f"Level: {node.level}/{node.max_level}", True, (255, 255, 255))

		tooltip_text2 = font.render(f"Name: {node.name}", True, (255, 255, 255))
		tooltip_text3 = font.render(f"{node.description}", True, (255, 255, 255))

		tooltip_rect = max(tooltip_text.get_rect(), tooltip_text2.get_rect(), tooltip_text3.get_rect())
		tooltip_rect.center = (node.x, node.y - 85)
		tooltip_rect.width += 10
		tooltip_rect.height = 66
		pygame.draw.rect(screen, (0, 0, 0), tooltip_rect)
		pygame.draw.rect(screen, (255, 255, 255), tooltip_rect, 1)
		screen.blit(tooltip_text, (tooltip_rect.centerx - tooltip_text.get_width() // 2,
								   (tooltip_rect.centery - tooltip_text.get_height() // 2) - 21))
		screen.blit(tooltip_text2, (tooltip_rect.centerx - tooltip_text2.get_width() // 2, tooltip_rect.centery - 10))
		screen.blit(tooltip_text3, (tooltip_rect.centerx - tooltip_text3.get_width() // 2, tooltip_rect.centery + 10))

	pygame.draw.circle(screen, node_color, (node.x, node.y), 30)

	level_text = font.render(str(node.level) if node.level < node.max_level else "MAX", True, (200, 100, 200))
	level_text_rect = level_text.get_rect(center=(node.x, (node.y) if node.level < node.max_level else (node.y)))
	screen.blit(level_text, (level_text_rect.x, level_text_rect.y))


class UpgradeNode:
	def __init__(self, x, y, cost, children=None, max_level=0, name='', description='', level=0, scaling=1.5):
		if children is None:
			children = []
		self.x, self.y = x, y
		self.x_o, self.y_o = x, y
		self.cost = cost
		self.level = level
		self.color = (255, 255, 255)
		self.max_level = max_level
		self.children = children
		self.name = name
		self.description = description
		self.parents = []
		self.scaling = scaling

		self.parents_bigger_than_one = False

		self.selected = False

	def is_mouse_over(self, mouse_x, mouse_y):
		return math.sqrt((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2) <= 20


root = UpgradeNode(1000 / 2, 800 / 2 + 330, 0, max_level=0, level=1, name='root', description='This is the root')
branch1_node1 = UpgradeNode(250, 150, 100, [], max_level=5, name='up1', description='This is upgrade 1')
branch1_node2 = UpgradeNode(550, 150, 150, [branch1_node1], max_level=5, name='up2', description='This is upgrade 2')
branch2_node1 = UpgradeNode(100, 250, 200, [], max_level=5, name='up3', description='This is upgrade 3')
branch2_node2 = UpgradeNode(250, 250, 250, [], max_level=5, name='up4', description='This is upgrade 4')
branch2_node3 = UpgradeNode(400, 250, 300, [], max_level=5, name='up5', description='This is upgrade 5')
branch2_node4 = UpgradeNode(550, 250, 350, [], max_level=5, name='up6', description='This is upgrade 6')
root.children = []  # branch1_node1, branch1_node2, branch2_node1, branch2_node2, branch2_node3, branch2_node4]

all_nodes = []

connect_active = [False]

points = 0
buyable_nodes = [root]
font = pygame.font.Font(os.getcwd() + "/assets/font.ttf", 18)

time_elapsed = 0
target_time = 1000


def find_node(name):
	for child in root.children:
		if child.name == name:
			return child


def load_pos():
	global all_nodes
	with open(os.getcwd() + '/tree_pos.json', mode='r') as f:
		if not os.stat(os.getcwd() + '/tree_pos.json').st_size == 0:
			list = pickle.decode(f.read())
			all_nodes = []
			root.children = []
			for item in list:
				root.children.append(item)
load_pos()

delete = False
edit = False


def get_parents():
	for node in all_nodes:
		parents = []
		parents_names = []
		for node2 in all_nodes:
			if len(node2.children) == 0: continue
			children = node2.children
			for child in children:
				if child == node:
					parents.append(node2)
					parents_names.append(node2.name)
		node.parents = parents


def check_parents(node):
	if node.name == 'root':
		return True
	if not len(node.parents) == 0:
		for item in node.parents:
			if item.level >= 1:
				return True
			else:
				continue
	else:
		return True
	return False


while True:
	get_parents()
	# Handle events
	buyable_nodes = update_buyable_nodes(root, buyable_nodes)
	for node in root.children:
		node.parents_bigger_than_one = check_parents(node)
		if not node.parents_bigger_than_one: node.color = (197, 197, 197)
	root.parents_bigger_than_one = True
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if delete:
				for node in root.children:
					mouse_x, mouse_y = pygame.mouse.get_pos()
					if node.is_mouse_over(mouse_x, mouse_y):
						root.children.remove(node)
				break
			if edit:
				for node in root.children:
					mouse_x, mouse_y = pygame.mouse.get_pos()
					if node.is_mouse_over(mouse_x, mouse_y):
						node.cost, node.max_level, node.name, node.description, node.scaling = int(input('cost ')), int(input("max level ")), input("name "), input("description "), input("scaling ")
						print('*'*50)
				break
			if pygame.mouse.get_pressed()[0]:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				for node in buyable_nodes:
					if node.parents_bigger_than_one:
						if node.is_mouse_over(mouse_x, mouse_y):
							if points >= node.cost and node.level < node.max_level:
								time_elapsed = 0
						if points >= node.cost:
							node.color = (0, 255, 153)
						elif points < node.cost:
							node.color = (178, 179, 179)
						if node.level >= node.max_level:
							node.color = (204, 153, 0)
					else:
						node.color = (197, 197, 197)
			if pygame.mouse.get_pressed()[2]:
				for node in root.children:
					mouse_x, mouse_y = pygame.mouse.get_pos()
					if node.is_mouse_over(mouse_x, mouse_y):
						node.selected = not node.selected
			if pygame.mouse.get_pressed()[1]:
				for node in root.children:
					mouse_x, mouse_y = pygame.mouse.get_pos()
					if node.is_mouse_over(mouse_x, mouse_y):
						if not connect_active[0]:
							connect_active[0] = True
							connect_active.append(node)
						else:
							if not connect_active[1] in node.children:
								node.children.append(connect_active[1])
								connect_active[0] = False
								del connect_active[1]
							else:
								node.children.remove(connect_active[1])
								connect_active[0] = False
								del connect_active[1]
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_p:
				with open(os.getcwd() + '/tree_pos.json', mode='w') as f:
					json = pickle.encode(all_nodes, keys=True)
					json_string = str(json)
					f.write(json_string.replace('__main__', 'a'))
			if event.key == pygame.K_r:
				with open(os.getcwd() + '/tree_pos.json', mode='w') as f:
					f.write('')
				load_pos()
			if event.key == pygame.K_d and not edit:
				delete = not delete
			if event.key == pygame.K_e and not delete:
				edit = not edit
			if event.key == pygame.K_n:
				node = UpgradeNode(10, 10, cost=int(input('cost ')), children=[], max_level=int(input("max level ")), name=input("name "),
								   description=input("description "), scaling=input("scaling "))
				print('*' * 50)
				all_nodes.append(node)
				root.children.append(node)

	for node in root.children:
		if node.selected:
			node.x, node.y = pygame.mouse.get_pos()
	screen.fill((100, 200, 100))
	pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(25, 420, 1000 - 50, 370), width=3)
	draw_node(root)
	points_text = font.render(f"Points: {points}", True, (255, 255, 255))
	screen.blit(points_text, (10, 10))
	if time_elapsed >= target_time:
		points += 5000
		time_elapsed = 0

	if delete:
		text = pygame.font.Font(os.getcwd() + "/assets/font.ttf", 36).render("!! DELETE ACTIVE !!", True, (255, 0, 0))
		screen.blit(text, (345, 100))
	if edit:
		text = pygame.font.Font(os.getcwd() + "/assets/font.ttf", 36).render("!! EDIT ACTIVE !!", True, (255, 0, 0))
		screen.blit(text, (375, 100))

	pygame.display.update()

	time_elapsed += clock.tick(60)