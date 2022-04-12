import math

class Node:
  def __init__(self):
    self.neighbors = {}
    self.was_visited = False
    self.steps = math.inf
    self.distance = math.inf
    self.predecessor = None
  
  def print_edges(self):
    for edge in self.neighbors:
      print(edge, end = ' ')
    print()
  
  def degree(self):
    return len(self.neighbors)
  
  def is_adjacent(self, node):
    for neighbor in self.neighbors:
      if node == neighbor:
        return True
    return False
  
  def reset_node(self):
    self.was_visited = False
    self.distance = math.inf
    self.predecessor = None
