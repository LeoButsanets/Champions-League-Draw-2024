import networkx as nx
import matplotlib.pyplot as plt 

def display_graph(G, pos, title, options = {
    "font_size": 30,
    "font_color": "orangered",
    "node_size": 3000,
    "edge_color" : "forestgreen",
    "node_color": "white",
    "edgecolors": "darkorange",
    "linewidths": 3,
    "width": 1,
  }):
  """
  Displays graph G with node positions and display options.

  Args:
  G: graph to be displayed
  pos: dictionary of node positions
  title: title of the plot
  options: dictionary of display options

  Returns:
  None
  """
  nx.draw(G, pos = pos, **options, with_labels=True)
  ax = plt.gca()
  plt.title(title, pad = 10)
  ax.margins(0.1)
  plt.axis("off")
  #plt.savefig('visualize/img/s-t_flow_graph_construction.png', transparent=True)
  plt.show()
  
def display_matching_in_bipartite_graph(U, V, flow_dict, title):
    """Reconstructs the matching from the flow_dict and displays the solution"""

    # Create bipartite graph
    T = nx.Graph()
    T.add_nodes_from(U, bipartite=0)
    T.add_nodes_from(V, bipartite=1)

    # Select edges with flow = 1 to obtain the matching
    matching = []
    for u in U:
        flow = 0
        for v in flow_dict[u]:
            flow += flow_dict[u][v]
            if flow_dict[u][v] == 1:
                T.add_edge(u,v)
                matching.append((u,v))

    # Set positions of nodes in the plan
    pos_T = dict()
    for i, node in enumerate(U):
        pos_T[node] = (6, i + 2)
    for i, node in enumerate(V):
        pos_T[node] = (12, i + 2)

    # Set options for graph display
    options = {
        "font_size": 40,
        "font_color": "orangered",
        "node_size": 3000,
        "edge_color" : "forestgreen",
        "node_color": "white",
        "edgecolors": "darkorange",
        "linewidths": 5,
        "width": 4
    }

    # Display the matching
    print(f"A possible matching is: ")
    for edge in T.edges():
        print(f"{edge[0]} - {edge[1]}" )

    display_graph(T, pos_T, title, options)

