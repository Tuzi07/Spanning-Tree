from graph import Graph

def graph_analysis(nodes_filepath, edges_filepath):
  print('Grafo')
  graph = Graph(nodes_filepath, edges_filepath)
  graph.print_graph()
  print()
  for source_node in graph.nodes:
    print('Spanning Tree from node', source_node)
    spanning_tree = graph.bfs_spanning_tree_from_node(source_node)
    spanning_tree.print_graph()
    print()
    for node in spanning_tree.nodes:
      print("Passos para o nó " + node + ": " + str(spanning_tree.nodes[node].steps))
      spanning_tree.print_path_to_node(node) # aqui tava graph ao inves de spanning_tree
      print('\n')
  print()

graph_analysis('nodes.csv', 'edges1.csv')
