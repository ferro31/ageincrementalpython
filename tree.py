import pygame
import os
import jsonpickle as pickle
import math
from a import UpgradeNode
from Notation import notate

pygame.init()


class Tree:
	def __init__(self, font, win, root_xy, game_state):
		self.events = []

		self.root = UpgradeNode(root_xy[0], root_xy[1], 0, max_level=1, name='root', level=1,
								description='This is the root of the tree.')
		self.branch1_node1 = UpgradeNode(250, 150, 100, [], max_level=5, name='up1', description='This is upgrade 1')
		self.branch1_node2 = UpgradeNode(550, 150, 150, [self.branch1_node1], max_level=5, name='up2',
										 description='This is upgrade 2')
		self.branch2_node1 = UpgradeNode(100, 250, 200, [], max_level=5, name='up3', description='This is upgrade 3')
		self.branch2_node2 = UpgradeNode(250, 250, 250, [], max_level=5, name='up4', description='This is upgrade 4')
		self.branch2_node3 = UpgradeNode(400, 250, 300, [], max_level=5, name='up5', description='This is upgrade 5')
		self.branch2_node4 = UpgradeNode(550, 250, 350, [], max_level=5, name='up6', description='This is upgrade 6')
		self.root.children = []  # branch1_node1, branch1_node2, branch2_node1, branch2_node2, branch2_node3, branch2_node4]

		self.all_nodes = []

		self.connect_active = [False]
		self.buyable_nodes = [self.root]
		self.font = font
		self.win = win

		self.points = 0

		self.game_state = game_state

	def get_levels(self):
		list = []
		for child in self.root.children:
			list.append(child.level)
		return list

	def load_levels(self, list):
		for ind, child in enumerate(self.root.children):
			child.level = list[ind]

	def update_buyable_nodes(self, node, buyable_nodes):
		if node.cost <= self.points and node not in buyable_nodes and node.level < node.max_level:
			node.color = (0, 255, 0)
			buyable_nodes.append(node)
		elif node.cost > self.points and node in buyable_nodes and node.level < node.max_level:
			node.color = (170, 49, 86)
			buyable_nodes.remove(node)
		for child in node.children:
			buyable_nodes = self.update_buyable_nodes(child, buyable_nodes)
		return buyable_nodes

	def sort_nodes(self, nodes):
		def node_sort_key(node):
			if node.is_mouse_over(*pygame.mouse.get_pos()):
				return 0
			else:
				return 1

		return sorted(nodes, key=node_sort_key)

	def update_colors(self):
		self.root.color = (204, 153, 0)
		for node in self.root.children:
			if self.points >= node.cost and node.level < node.max_level:
				pygame.draw.circle(self.win, (0, 200, 0), (node.x, node.y), 35)
			if node.level >= node.max_level:
				node.color = (204, 153, 0)
			else:
				node.color = (197, 197, 197)


	def draw_node(self, node):
		list = []
		for child in node.children:
			list2 = []
			for item in self.all_nodes:
				list2.append(item.name)
			if child.name not in list2:
				self.all_nodes.append(child)
			list.append(child)
			pygame.draw.line(self.win, child.color, (node.x, node.y + 10), (child.x, child.y - 10), 4)
		for child in list:
			self.draw_node(child)

		node_color = node.color
		if node.is_mouse_over(*pygame.mouse.get_pos()):
			if not node.parents_bigger_than_one:
				node_color = (255, 255, 153)

			if node.level < node.max_level:
				tooltip_text = self.font.render(f"Level: {node.level}/{node.max_level}\nCost: {notate(node.cost, self.game_state.notation_list)}", True,
												(255, 255, 255))
			else:
				tooltip_text = self.font.render(f"Level: {node.level}/{node.max_level}", True, (255, 255, 255))

			tooltip_text2 = self.font.render(f"Name: {node.name}", True, (255, 255, 255))
			tooltip_text3 = self.font.render(f"{node.description}", True, (255, 255, 255))

			tooltip_rect = max(tooltip_text.get_rect(), tooltip_text2.get_rect(), tooltip_text3.get_rect())
			tooltip_rect.center = (node.x, node.y - 85)
			tooltip_rect.width += 10
			tooltip_rect.height = 66
			pygame.draw.rect(self.win, (0, 0, 0), tooltip_rect)
			pygame.draw.rect(self.win, (255, 255, 255), tooltip_rect, 1)
			self.win.blit(tooltip_text, (tooltip_rect.centerx - tooltip_text.get_width() // 2,
										 (tooltip_rect.centery - tooltip_text.get_height() // 2) - 21))
			self.win.blit(tooltip_text2,
						  (tooltip_rect.centerx - tooltip_text2.get_width() // 2, tooltip_rect.centery - 10))
			self.win.blit(tooltip_text3,
						  (tooltip_rect.centerx - tooltip_text3.get_width() // 2, tooltip_rect.centery + 10))

		pygame.draw.circle(self.win, node_color, (node.x, node.y), 30)

		level_text = self.font.render(str(node.level) if node.level < node.max_level else "MAX", True, (200, 100, 200))
		level_text_rect = level_text.get_rect(center=(node.x, (node.y) if node.level < node.max_level else (node.y)))
		self.win.blit(level_text, (level_text_rect.x, level_text_rect.y))

	def load_pos(self):
		with open(os.getcwd() + '/tree_pos.json', mode='r') as f:
			if not os.stat(os.getcwd() + '/tree_pos.json').st_size == 0:
				list = pickle.decode(f.read())
				all_nodes = []
				self.root.children = []
				for item in list:
					self.root.children.append(item)

	def find_node(self, name):
		for child in self.root.children:
			if child.name == name:
				return child

	def get_parents(self):
		for node in self.all_nodes:
			parents = []
			parents_names = []
			for node2 in self.all_nodes:
				if len(node2.children) == 0: continue
				children = node2.children
				for child in children:
					if child == node:
						parents.append(node2)
						parents_names.append(node2.name)
			node.parents = parents


	def check_parents(self, node):
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

	def game_loop(self):
		self.get_parents()
		buyable_nodes = self.update_buyable_nodes(self.root, self.buyable_nodes)
		for node in self.root.children:
			node.parents_bigger_than_one = self.check_parents(node)
			if not node.parents_bigger_than_one: node.color = (197, 197, 197)
		self.root.parents_bigger_than_one = True
		for event in self.events:
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed()[0]:
					mouse_x, mouse_y = pygame.mouse.get_pos()
					for node in buyable_nodes:
						if node.parents_bigger_than_one:
							if node.is_mouse_over(mouse_x, mouse_y):
								if self.points >= node.cost and node.level < node.max_level:
									self.game_state.ap -= node.cost
									node.level += 1
									node.cost = math.ceil(node.cost * float(node.scaling))
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					with open(os.getcwd() + '/tree_pos.json', mode='w') as f:
						json = pickle.encode(self.all_nodes)
						f.write(json)
				if event.key == pygame.K_r:
					with open(os.getcwd() + '/tree_pos.json', mode='w') as f:
						f.write('')
					self.load_pos()
				if event.key == pygame.K_n:
					node = UpgradeNode(10, 10, 350, [], max_level=int(input("max level ")), name=input("name "),
									   description=input("description "))
					self.all_nodes.append(node)
					self.root.children.append(node)
		self.update_colors()
		for node in self.root.children:
			if node.selected:
				node.x, node.y = pygame.mouse.get_pos()
		self.draw_node(self.root)
