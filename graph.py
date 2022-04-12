import csv
from node import Node
from edge import Edge

class Graph:
  def __init__(self, nodes_filepath, edges_filepath):
    self.nodes = {}
    self.number_of_nodes = 0
    self.number_of_edges = 0
    self.add_nodes_from_csv(nodes_filepath)
    self.add_edges_from_csv(edges_filepath)

  def add_node(self, node):
    if node in self.nodes:
      print("This node already exists")
    else: 
      self.nodes[node] = Node()
      self.number_of_nodes += 1

  def add_edge(self, origin, destiny, weight):
    if origin not in self.nodes or destiny not in self.nodes:
      print("Node does not exist")
    else:
      self.nodes[origin].neighbors[destiny] = Edge(weight = int(weight))
      self.nodes[destiny].neighbors[origin] = Edge(weight = int(weight))
      self.number_of_edges += 1
  
  def add_directed_edge(self, origin, destiny, weight):
    if origin not in self.nodes or destiny not in self.nodes:
      print("Node does not exist")
    else:
      self.nodes[origin].neighbors[destiny] = Edge(weight = int(weight))
      self.number_of_edges += 1

  def add_nodes_from_csv(self, nodes_filepath):
    with open(nodes_filepath, newline='') as csvfile:
      reader = csv.reader(csvfile)
      for row in reader:
        self.add_node(row[0])

  def add_edges_from_csv(self, edges_filepath):
    with open(edges_filepath, newline='') as csvfile:
      reader = csv.reader(csvfile)
      for row in reader:
        self.add_edge(origin = row[0], destiny = row[1], weight = row[2])

  def print_graph(self):
    for node in self.nodes:
      print(node, "-> ", end = '')
      self.nodes[node].print_edges()

  def has_edge(self, node1, node2):
    if node1 not in self.nodes or node2 not in self.nodes:
      return False
    if node1 == node2:
      return True
    return self.nodes[node1].is_adjacent(node2)

  def is_complete(self):
    from math import comb
    return self.number_of_edges == comb(self.number_of_nodes, 2)

  def remove_edge(self, node1, node2):
    if node1 not in self.nodes or node2 not in self.nodes:
      print("Node does not exist")
    else:
      self.nodes[node1].neighbors.pop(node2)
      self.nodes[node2].neighbors.pop(node1)
      self.number_of_edges -= 1

  def reset_visited_nodes(self):
    for node in self.nodes:
      self.nodes[node].reset_node()
  
  def dfs_count_from_node(self, node):
    visited_nodes = 1
    self.nodes[node].was_visited = True
    for neighbor in self.nodes[node].neighbors:
      if not self.nodes[neighbor].was_visited:
        visited_nodes += self.dfs_count_from_node(neighbor)
    return visited_nodes
  
  def bfs_spanning_tree_from_node(self, source_node):
    spanning_tree = Graph('nodes.csv', 'no_edges.csv')
    self.reset_visited_nodes()
    
    from collections import deque
    queue = deque([])

    queue.append(source_node)
    spanning_tree.nodes[source_node].steps = 0
    spanning_tree.nodes[source_node].was_visited = True

    while queue:
      current = queue.popleft()

      for neighbor in self.nodes[current].neighbors:
        if not spanning_tree.nodes[neighbor].was_visited:
          queue.append(neighbor)
          spanning_tree.nodes[neighbor].was_visited = True
          spanning_tree.nodes[neighbor].steps = spanning_tree.nodes[current].steps + 1
          spanning_tree.nodes[neighbor].predecessor = current
          spanning_tree.add_directed_edge(current, neighbor, weight = 1)
    return spanning_tree
  
  def BFS(self, node):
    self.reset_visited_nodes()
    
    from collections import deque
    queue = deque([])

    queue.append(node)
    self.nodes[node].was_visited = True
    self.nodes[node].steps = 0

    while queue:
      current = queue.popleft()

      for neighbor in self.nodes[current].neighbors:
        if not self.nodes[neighbor].was_visited:
          queue.append(neighbor)
          self.nodes[neighbor].was_visited = True
          self.nodes[neighbor].steps = self.nodes[current].steps + 1
          self.nodes[neighbor].predecessor = current
  
  def print_path_to_node(self, node):
    predecessor = self.nodes[node].predecessor
    if predecessor:
      self.print_path_to_node(predecessor)
    print(node + " ", end = '')

  def DFS(self, node):
    self.nodes[node].was_visited = True
    for neighbor in self.nodes[node].neighbors:
      if not self.nodes[neighbor].was_visited:
        self.DFS(neighbor)

  def dijkstra(self, starting_node):
    self.reset_visited_nodes()
    self.nodes[starting_node].distance = 0

    from queue import PriorityQueue

    priority_queue = PriorityQueue()
    priority_queue.put((self.nodes[starting_node].distance, starting_node))

    while priority_queue: # not priority_queue.empty():
      distance, node = priority_queue.get()
      if not self.nodes[node].was_visited:
        self.nodes[node].was_visited = True
        for neighbor in self.nodes[node].neighbors:
          if not self.nodes[neighbor].was_visited:
            new_distance = distance + self.nodes[node].neighbors[neighbor].weight
            if new_distance < self.nodes[neighbor].distance:
              self.nodes[neighbor].distance = new_distance
              self.nodes[neighbor].predecessor = node
              priority_queue.put(new_distance, neighbor)
