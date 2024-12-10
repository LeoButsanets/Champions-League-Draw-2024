import networkx as nx
from typing import List, Dict, Any, Tuple
import networkx as nx
import matplotlib.pyplot as plt

def init_d_v(pots, d):
    """
    Initializes a dictionary with all nodes in the pots and assigns the value d to each node.

    Parameters:
    pots (dict): Dictionary with groups of teams.
    d (int): The value to assign to each node.

    Returns:
    dict: A dictionary with nodes as keys and d as values.
    """
    d_v = {node['club']: d for pot in pots.values() for node in pot}
    return d_v

def initialize_edges(U: List[Dict[str, Any]], V: List[Dict[str, Any]]) -> List[Tuple[str, str]]:
    """
    Creates a list of edges between two lists of vertices U and V by checking that the
    vertices have different attributes.

    Args:
    U (List[Dict[str, Any]]): List of vertices in U.
    V (List[Dict[str, Any]]): List of vertices in V.

    Returns:
    edges (List[Tuple[str, str]]): List of edges between the vertices of U and V.
    """
    return [(u['club'], v['club']) for u in U for v in V if u['country'] != v['country']]

def initialize_bipartite_graph(Pot_i, Pot_j):
    """
    Create a bipartite graph between two pots and return the graph, the two lists of vertices,
    and the list of edges.

    Args:
    Pot_i (list): List of teams in pot i.
    Pot_j (list): List of teams in pot j.

    Returns:
    B (networkx.Graph): Bipartite graph.
    U (list): List of vertices in pot i.
    V (list): List of vertices in pot j.
    """
    B = nx.Graph()  # initialize empty bipartite graph
    # add the vertices and edges to the bipartite graph
    B.add_nodes_from([t['club'] for t in Pot_i], bipartite=0)
    B.add_nodes_from([t['club'] for t in Pot_j], bipartite=1)
    B.add_edges_from(initialize_edges(Pot_i, Pot_j))

    return B

def max_flow_graph(B, degree_dict):
    """
    Returns the directed graph for solving the maximum d-flow problem by fixing the capacities to d for the outgoing
    edges of s and incoming edges of t, and to 1 for the edges between U and V.

    Args:
    B (networkx.Graph): Bipartite graph.
    d (int): Capacity for outgoing edges of s and incoming edges of t.

    Returns:
    G (networkx.DiGraph): Directed graph for maximum d-flow problem.
    """
    U = {node for node, bipartite in B.nodes(data='bipartite') if bipartite == 0}
    V = {node for node, bipartite in B.nodes(data='bipartite') if bipartite == 1}

    G = nx.DiGraph()
    G.add_nodes_from(U | V)  # Union of sets U and V
    for u, v in list(B.edges):
        G.add_edge(u, v, capacity=1)

    G.add_nodes_from(['s', 't'])
    for u in U:
        G.add_edge('s', u, capacity=degree_dict[u])
    for v in V:
        G.add_edge(v, 't', capacity=degree_dict[v])

    return G

def single_pot_graph(pot, show=False):
    """
    Returns the graph of a pot.

    Parameters:
    pot (list): List of tuples representing the players in a pot.
    show (bool, optional): Whether to display the graph. Default is False.

    Returns:
    G (nx.Graph): Graph representing the pot.
    """

    # Initialize the graph
    G = nx.Graph()
    G.add_nodes_from([t['club'] for t in pot])
    G.add_edges_from(initialize_edges(pot, pot))

    if show:
        # Display the graph
        options = {
            "font_size": 30,
            "font_color": "orangered",
            "node_size": 3000,
            "node_color": "white",
            "edgecolors": "darkorange",
            "edge_color": "forestgreen",
            "linewidths": 3,
            "width" : 2
        }

        pos = nx.circular_layout(G)
        plt.figure(figsize=(20,20))
        nx.draw(G, pos, with_labels=True, **options)
        ax = plt.gca()
        plt.title("Au sein d'un pot", pad=10)
        ax.margins(0.1)
        plt.axis("off")
        #plt.savefig('one_pot.png', transparent=True)
        plt.show()

    return G

def transformed_graph(G, degree_dict=None, degree=2, show=False, options={
    "font_size": 10,
    "font_color": "orangered",
    "node_size": 700,
    "node_color": "white",
    "edgecolors": "darkorange",
    "linewidths": 3,
    "width": 1,
  }):
  """Consider the graph constructed from G=(V,E) as follows:
    • Replace each vertex u by d(u) copies u1, ..., ud(u).
    • For each edge (u, v) (which is removed): create two vertices u' and v' connected
    by an edge, add d edges between the ui's and u', add d edges between the vi's and v'.
    Let the new graph be G' = (d|V| + 2|E|, (2d + 1)|E|)."""


  # G = (V, E)
  # Initialize the dictionary of degrees
  if degree_dict is None:
    degree_dict = {node: degree for node in G.nodes()}

  V = G.nodes()
  E = G.edges()
  G_ = nx.Graph()
  # Replace each vertex u by d copies u1, ..., ud
  nodes_copies = dict()
  for v in V:
    copies = []
    if degree_dict[v] != 0:
      for i in range(1, degree_dict[v] + 1):
        G_.add_node(str(v) + "_" + str(i))
        copies.append(str(v) + "_" + str(i))
      nodes_copies[v] = copies
    else:
      nodes_copies[v] = []
  # For each edge (u, v) (which is removed)
  nodes_primes = dict()
  for i, (u, v) in enumerate(E):
    if nodes_copies[u] != [] and nodes_copies[v] != []:
        # create two vertices u' and v' connected by an edge
        u_prime, v_prime = str(u) + "_" + str(i+1) + "'", str(v) +  "_" + str(i+1) + "'"
        G_.add_edge(u_prime, v_prime)
        nodes_primes[u,v] = u_prime, v_prime
        # add d edges between the ui's and u', and add d edges between the vi's and v'
        for u_copie in nodes_copies[u]:
          G_.add_edge(u_copie, u_prime)
        for v_copie in nodes_copies[v]:
          G_.add_edge(v_copie, v_prime)


  if show:
    pos = nx.circular_layout(G_)
    nx.draw(G_, pos, with_labels=True, **options)
    ax = plt.gca()
    plt.title("Transformed Graph", pad=10)
    #plt.savefig('transformed_graph.png', transparent=True)
    ax.margins(0.1)
    plt.axis("off")

  return G_, nodes_primes

def reconstitute_matching(G, nodes_primes, matching, pos, d=2, show=True, options={"font_color": "orangered", "node_color": "white", "edgecolors": "darkorange", "linewidths": 3}, figsize=(30,30)):
    """Returns the d-matching if it is perfect and displays it in the graph G"""
    matching_size = len(matching)
    nb_edges = len(G.edges)
    nb_nodes = len(G.nodes)
    
    # Check if the d-matching is perfect (if it covers all nodes exactly d times)
    if matching_size != (d * nb_nodes + 2 * nb_edges) // 2:
        return []
    
    # Reconstruct the graph with the edges chosen in the d-matching
    else:
        m = []
        for u, v in G.edges():
            u_p, v_p = nodes_primes[u, v]
            if [u_p, v_p] in matching or [v_p, u_p] in matching:
                m.append((u, v))
        
        true_matching = []
        for u, v in G.edges():
            if (u, v) not in m:
                true_matching.append((u, v))

        Gdash = nx.Graph()
        Gdash.add_nodes_from(G.nodes)
        
        for u, v in G.edges:
            if (u, v) in true_matching:
                Gdash.add_edge(u, v, color="r", weight=3)
            else:
                Gdash.add_edge(u, v, color="forestgreen", weight=2)
        
        color = [Gdash[u][v]["color"] for u, v in G.edges()]
        weight = [Gdash[u][v]["weight"] for u, v in G.edges()]
        
        if show:
            plt.figure(figsize=figsize)
            nx.draw(
                Gdash,
                pos,
                with_labels=True,
                edge_color=color,
                width=weight,
                **options
            )

            #plt.savefig("reconstitute_matching.png", transparent=True)
            plt.show()
    
    return true_matching
