import pygame
import time
import random
from math import sqrt, inf

pygame.init()

display_width = 700
display_height =700
grid = (50, 50)
fps = 100

black = (30,30,30)
gray = (150, 150, 150)
white = (255,255,255)
red = (255,0,0)
light_red = (255, 100, 100)
green = (0,200,0)
blue = (0,100,255)
purple = (200,0,200)

gameDisplay = pygame.display.set_mode((display_width + grid[0], display_height + grid[1]))
pygame.display.set_caption("Djikstra's algorithm")
clock = pygame.time.Clock()


class node(object):
	def __init__(self, id, pos, size, color=gray):
		self.id = id
		self.state = 0
		self.value = inf
		self.color = color
		self.position = pos
		self.x = self.position[0]
		self.y = self.position[1]
		self.size = size

	def set_state(self, state=None):
		if state == 1:
			self.state = 1
			self.color = black
			return state

		if self.state == 0:		# neutral
			self.state = state =  1
			self.color = black
		elif self.state == 1:	# obstacle
			self.state = state = 2
			self.color = blue
		elif self.state == 2:	# goal
			self.state = state = 3
			self.value = 0
			self.color = green
		elif self.state == 3:	# start
			self.state = state = 0
			self.value = inf
			self.color = gray
		return state

	def draw(self):
		pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.size[0], self.size[1]])
		
		#value = self.value
		#if value == 100_000_000: value = "#"
		display_text(self.value, 10, (self.x + self.size[0]/2, self.y + self.size[0]/2), black)


class graph(object):
	def __init__(self, graph_size):
		self.graph_size = graph_size
		self.node_size = (round(display_width / self.graph_size[0]), round(display_height / self.graph_size[1]))
		self.start = None
		self.goal = None
		self.obstacles = []
		self.nodes = []
		self.spawn()

	def spawn(self):
		position = [0, 0]
		for i in range(1, self.graph_size[0] * self.graph_size[1] + 1):
			self.nodes.append(node(id=i, pos=position, size=self.node_size))
			position[0] = position[0] + self.node_size[0] + 1

			if i == 0: continue
			elif i % self.graph_size[0] == 0:
				position[0] = 0
				position[1] = position[1] + self.node_size[1] + 1

	def draw(self):
		for node in self.nodes:
			node.draw()

	def randomize(self):
		# choose random nodes as obstacle
		random_nodes = random.sample(self.nodes, int(grid[0]*grid[1]*0.3))
		for node in random_nodes:
			node.set_state(1)

	def get_node_with_pos(self, pos):
		for node in self.nodes:
			if pos[0] >= node.x and pos[0] <= node.x + node.size[0] and pos[1] >= node.y and pos[1] <= node.y + node.size[1]:
				return node

	def get_node_with_id(self, id):
		for node in self.nodes:
			if node.id == id:
				return node
		return None

	def get_all_nodes(self):
		temp_nodes = []
		for node in self.nodes:
			if not node.state == 1:
				temp_nodes.append(node)
		return temp_nodes

	def get_neigbhours(self, node):
		id = node.id
		neighbours = []
		
		if id > grid[0]:
			neighbours.append(self.get_node_with_id(id - grid[0]))			# 2: top center
			'''
			if id % grid[0] != 1:
				neighbours.append(self.get_node_with_id(id - grid[0] - 1))		# 1: top left
			if id % grid[0] != 0:
				neighbours.append(self.get_node_with_id(id - grid[0] + 1))		# 3: top right
			'''
		if id % grid[0] != 1:
			neighbours.append(self.get_node_with_id(id - 1))				# 4: left
		if id % grid[0] != 0:
			neighbours.append(self.get_node_with_id(id + 1))				# 5: right
		
		if (id / grid[0]) < (grid[0] - 1):
			neighbours.append(self.get_node_with_id(id + grid[0]))			# 7: bottom center
			'''
			if id % grid[0] != 1:
				neighbours.append(self.get_node_with_id(id + grid[0] - 1))		# 6: bottom left
			if id % grid[0] != 0:
				neighbours.append(self.get_node_with_id(id + grid[0] + 1))		# 8: bottom right
			'''
		for neighbour in neighbours:
			try:
				if neighbour.state == 1:		# obstacle
					neighbours.remove(neighbour)
			except:
				pass
			#else:
			#	neighbour.color = red

		return neighbours

	def set_node_state(self, node):
		node.set_state()


def display_text(text, size, position, color=black):
	textFont = pygame.font.Font(pygame.font.get_default_font(), size)
	textSurface = textFont.render(str(text), True, color)
	textRect = textSurface.get_rect()
	textRect.center = position
	gameDisplay.blit(textSurface, textRect)

def game_loop():
	my_graph = graph(graph_size=grid)
	finished = False
	start_algorithm = False
	algorithm_done = False
	draw_path = False
	run_once = True
	run_once_2 = True
	ctrl_hold = False

	my_graph.randomize()
	gameDisplay.fill(white)
	my_graph.draw()
	current_node = None

	while not finished:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				finished = True

			if event.type == pygame.KEYDOWN:
				if event.key == 306:
					ctrl_hold = True

			if event.type == pygame.KEYUP:
				print(event.key)
				if event.key == 32:		# space
					start_algorithm = not start_algorithm
				if event.key == 306:
					ctrl_hold = False

			if pygame.mouse.get_pressed()[0]:
				if ctrl_hold:
					mouse_position = pygame.mouse.get_pos()
					node = my_graph.get_node_with_pos(mouse_position)
					state = node.set_state(1)
					my_graph.draw()
				elif algorithm_done:
					mouse_position = pygame.mouse.get_pos()
					node = my_graph.get_node_with_pos(mouse_position)
					current_node = node
					draw_path = True

				else:	
					mouse_position = pygame.mouse.get_pos()
					node = my_graph.get_node_with_pos(mouse_position)
					state = node.set_state()
					if state == 3:
						my_graph.start = node
						print("starting node id: {}".format(node.id))
					elif state == 2:
						my_graph.goal = node
						print("Goal node id: {}".format(node.id))
					my_graph.draw()
					#my_graph.get_neigbhours(node)

		# Djikstras algorithm
		if start_algorithm:
			if run_once:
				run_once = False
				if my_graph.start is None or my_graph.goal is None:
					start_algorithm = False
					print("Missing starting node or finishing node!")
					continue

				visited_nodes = []
				unvisited_nodes = my_graph.get_all_nodes()
				path = {}

				print("\nInitializing algorithm!")
				print("Starting node: {}\nGoal node: {}".format(my_graph.start.id, my_graph.goal.id))

			
			unvisited_nodes.sort(key=lambda x: x.value)
			current_node = unvisited_nodes[0]
			unvisited_nodes.remove(current_node)
			visited_nodes.append(current_node)

			#print("current_node: {}".format(current_node.id))

			current_node.color = light_red
			current_node.draw()
			#time.sleep(0.01)
			
			current_node_neighbours = my_graph.get_neigbhours(current_node)
			
			for neighbour_node in current_node_neighbours:
				if neighbour_node in visited_nodes:
					continue	
				try:
					if current_node.value + 1 < neighbour_node.value:
						neighbour_node.value = current_node.value + 1
						path[neighbour_node] = current_node

				except Exception as e:
					print(e)

			if current_node.id == my_graph.goal.id: 
				print("Done!")
				start_algorithm = False
				draw_path = True
				algorithm_done = True
		
		# draw shortest path from start node to goal node
		if draw_path:
			if run_once_2:
				run_once_2 = False
				
				current_node = my_graph.goal
				current_node.color = purple
				current_node.draw()

			try:
				current_node = path[current_node]
				current_node.color = purple
				current_node.draw()
			except:
				pass

			if current_node.id == my_graph.start.id:
				print("Done drawing path")
				draw_path = False

		#FPS
		#display_text("Fps: {}".format(round(clock.get_fps())), 20, (50, 10), black)
		#print(round(clock.get_fps()))
		pygame.display.update()
		clock.tick(fps)

game_loop()
pygame.quit()
quit()