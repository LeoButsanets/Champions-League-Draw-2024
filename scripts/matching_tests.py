import networkx as nx
from graph_utils import *
from networkx.algorithms.flow import edmonds_karp
import matplotlib.pyplot as plt
from display import display_matching_in_bipartite_graph, display_graph
from edmonds.blossom import find_maximum_matching
from edmonds.graph_utils import Matching, Graph

def is_matching_distinct_pots(pot_i, pot_j, degree_dict=None, degree = 2, show = False):
    """
    Returns True if a subset F has been found such that
    ∀v ∈ V degF (v) = d in the bipartite graph between pot_i and pot_j where i!=j
    
    """
    # Initialize the dictionary of degrees
    if degree_dict is None:
        degree_dict = {team['club']: degree for team in pot_i + pot_j}
    else:
        degree = degree_dict[list(degree_dict.keys())[0]]
        
    # Initialize bipartite graph
    B = initialize_bipartite_graph(pot_i, pot_j)
    U = {node for node, bipartite in B.nodes(data='bipartite') if bipartite == 0}
    V = {node for node, bipartite in B.nodes(data='bipartite') if bipartite == 1}
    # Create maximum flow graph
    G = max_flow_graph(B, degree_dict)

    # Find maximum flow with Edmonds-Karp algorithm
    flow_value, flow_dict = nx.maximum_flow(G, 's', 't', flow_func=edmonds_karp)

    # Position of edges
    pos = dict()
    pos['s'] = (0,6)
    pos['t'] = (18,6)
    for i, node in enumerate(U):
        pos[node] = (6, i + 2)
    for i, node in enumerate(V):
        pos[node] = (12, i + 2)

    # Display graph
    if show:
        display_graph(G, pos, "s-t maximum flow graph")

    # Check if all nodes in V have a flow degree greater than or equal to d
    result = True
    for v in V:
        flow = 0
        for u in flow_dict[v]:
            flow += flow_dict[v][u]
        result = (flow == degree_dict[v])
        if not result:
            break

    if show:
        # Display result
        if result:
            # Build matching by selecting charged edges
            matching = []
            for u, v in G.edges():
                if flow_dict[u][v] == 1:
                    matching.append((u,v))
            print(f"A subset F has been found such that ∀v ∈ V degF (v) = {degree}.")
            # Display matching
            print("Resulting graph with charged edges")
            print("\n")
            print("=================================================================")
            print("\n")
            print(matching)
            print("\n")
            print("===================================================================")

            # Display flow in maximum flow graph
            Gdash = nx.DiGraph()
            Gdash.add_nodes_from(G.nodes)
            for u,v in G.edges():
                if (u,v) in matching:
                    Gdash.add_edge(u, v, color="r", weight=3)
                else:
                    Gdash.add_edge(u, v, color="forestgreen", weight=1)

            color = [Gdash[u][v]["color"] for u, v in G.edges()]
            weight = [Gdash[u][v]["weight"] for u, v in G.edges()]

            if show:
                options = {"font_size": 30, "font_color": "orangered", "node_size": 3000, "node_color": "white", "edgecolors": "darkorange", "linewidths": 5}
                nx.draw(Gdash, pos, with_labels=True, edge_color=color, width=weight, **options)
            ax = plt.gca()
            plt.title("s-t maximum flow graph", pad = 10)
            ax.margins(0.1)
            plt.axis("off")
            plt.show()
            plt.figure(figsize = (30,30))
            display_matching_in_bipartite_graph(U, V, flow_dict, "Matching found")
        else:
            print(f"No subset F was found such that ∀v ∈ V degF (v) = {degree}.")

    return result


def matching_existence_distinct_pots(pots, degree_dict=None, degree=2):
    """
    Tests whether there exists a matching such that for every i != j in [1, ..., k] and for every vertex v in (V_i U V_j) induced by pot_i and pot_j in pots,
    degF(v) = d.

    Args:
    - pots (dict): a dictionary of pots where each pot is a dictionary of teams characterized by their club and their country attributes
    - degree_dict: a dictionaty of the degree for each node (club) in the matching
    - degree: the degree for each node (club) in the matching if degree_dict is None

    Returns:
    - True if there every couple of distinct pots that satisfies the condition, False otherwise
    """
    result = True

    # Initialize the dictionary of degrees
    if degree_dict is None:
        degree_dict = {team['club']: degree for pot in pots.values() for team in pot}
    else:
        degree = degree_dict[list(degree_dict.keys())[0]]

    # Iterate over all pairs of pots
    for i, pot_i in pots.items():
        for j, pot_j in pots.items():
            if i < j:
                # Check if there exists a matching between the two pots that satisfies the condition
                result = is_matching_distinct_pots(pot_i, pot_j, degree_dict=degree_dict, degree=degree)

                if not result:
                    # If there is no matching that satisfies the condition, print message and return False
                    print(f"There doesn't exist matching such that ∀i!=j ∈ [1,..., k] ∀v ∈ (V_i U V_j) degF (v) = {degree}.")
                    print("\n")
                    return False

    # If there is a matching that satisfies the condition, print message and return True
    if result:        
        print(f"There exist a matching such ∀i!=j ∈ [1,..., k] ∀v ∈ (V_i U V_j) degF (v) = {degree} .")
        return True
    

def is_matching_within_pot(pot, degree_dict=None, degree=2):
    """
    Returns True if a perfect d-matching is found in the pot.

    Args:
    - pot: a Pot object
    - d: degree value for matching

    Returns:
    - True if a perfect d-matching is found, False otherwise
    """

    G_ = single_pot_graph(pot)
    G, nodes = transformed_graph(G_, degree_dict=degree_dict, degree=degree)
    graph = Graph()
    graph.nodes = list(G.nodes())
    edges_ = [[u, v] for u, v in G.edges()]
    graph.edges = edges_
    matching = Matching()
    matching = find_maximum_matching(graph, matching).edges

    d_tot = sum(degree_dict[v] for v in G_.nodes())
    nb_edges = len(list(G_.edges))
    matching_size = len(list(matching))

    nb_edges = len(G_.edges())
    return matching_size == (d_tot + 2*nb_edges)//2

def matching_existence_within_pots(pots, degree_dict=None, degree=2):
    """
    Tests whether a perfect d-matching exists in each of the pots.
    Returns True if a perfect d-matching is found in each pot, False otherwise.
    """
    
    # Initialize the dictionary of degrees
    if degree_dict is None:
        degree_dict = {team['club']: degree for pot in pots.values() for team in pot}
    else:
        degree = degree_dict[list(degree_dict.keys())[0]]

    for pot_name, pot in pots.items():
        # Check if a perfect d-matching is found in the pot
        result = is_matching_within_pot(pot, degree_dict=degree_dict, degree=degree)

        # If no perfect d-matching is found, return False and print error message
        if not result:
            print(f"There doesn't exist a perfect matching in pot {pot_name} for the d = {degree}.")
            print("\n")
            return False

    # If all pots have a perfect d-matching, return True and print success message
    print(f"There exist a perfect matching in each pot for d = {degree}.")
    return True