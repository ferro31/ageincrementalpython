import jsonpickle as pickle
import os
import math


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


def load_pos():
	with open(os.getcwd() + '/tree_pos.json', mode='r') as f:
		if not os.stat(os.getcwd() + '/tree_pos.json').st_size == 0:
			return pickle.decode(f.read())
