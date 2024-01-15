import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import random
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json


def create_graph_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    G = nx.Graph()

    # Add nodes
    for ponto in data['PontosTuristicos']:
        nome = ponto['nome']
        latitude = ponto['latitude']
        longitude = ponto['longitude']
        G.add_node(nome, pos=(longitude, latitude))

    # Add edges
    for conexao in data['conexoes']:
        origem = conexao['origem']
        destino = conexao['destino']
        cost = conexao['cost']
        G.add_edge(origem, destino, cost=cost)

    return G


def generate_traffic_intersections(G):
    # Convert set of nodes to list
    nodes_list = list(G.nodes())

    # Randomly select 6 intersections
    intersections = random.sample(nodes_list, 4)

    # Assign exactly 2 high traffic intersections and 4 medium traffic intersections
    high_traffic_intersections = random.sample(intersections, 2)
    medium_traffic_intersections = list(set(intersections) - set(high_traffic_intersections))

    # Create a list of all edges that have high traffic intersections
    high_traffic_edges = [edge for edge in G.edges() if
                          edge[0] in high_traffic_intersections or edge[1] in high_traffic_intersections]

    # Create a list of all edges that have medium traffic intersections
    medium_traffic_edges = [edge for edge in G.edges() if
                            edge[0] in medium_traffic_intersections or edge[1] in medium_traffic_intersections]

    # Update edge weights for high traffic intersections
    for edge in high_traffic_edges:
        G[edge[0]][edge[1]]['cost'] += 1

    # Update edge weights for medium traffic intersections
    for edge in medium_traffic_edges:
        G[edge[0]][edge[1]]['cost'] += 0.3

    return G


def draw_graph(G):
    pos = nx.get_node_attributes(G, 'pos')

    # Set different colors for each node
    colors = plt.cm.rainbow(np.linspace(0, 1, len(G.nodes())))

    # Adjust the size of the nodes
    node_size = 60

    # Draw edges with different colors based on traffic
    edge_colors = []
    for edge in G.edges():
        if G[edge[0]][edge[1]]['cost'] == 1:
            edge_colors.append('red')  # High traffic
        elif G[edge[0]][edge[1]]['cost'] == 0.3:
            edge_colors.append('orange')  # Medium traffic
        else:
            edge_colors.append('green')  # Default color for other edges

    nx.draw(G, pos, with_labels=False, node_color=colors, node_size=node_size, edge_color=edge_colors)

    # Create a legend
    legend_elements = [Line2D([0], [0], marker='o', color='w', markerfacecolor=colors[i], markersize=8,
                              label=node) for i, node in enumerate(G.nodes())]

    # Add custom legend for edge colors
    legend_elements.append(Line2D([0], [0], color='w', markerfacecolor='red', markersize=8, label='High Traffic'))
    legend_elements.append(Line2D([0], [0], color='w', markerfacecolor='orange', markersize=8, label='Medium Traffic'))

    plt.legend(handles=legend_elements, loc='upper left', title='Points', fontsize=8)
    plt.show()


def create_and_draw_graph(json_file):
    G = create_graph_from_json(json_file)
    G = generate_traffic_intersections(G)

    fig, ax = plt.subplots()
    draw_graph(G)
    return fig


def draw_graph_teste(G, path_edges=None):
    pos = nx.get_node_attributes(G, 'pos')

    # Set different colors for each node
    colors = plt.cm.rainbow(np.linspace(0, 1, len(G.nodes())))

    # Adjust the size of the nodes
    node_size = 60

    # Draw edges with different colors based on traffic
    edge_colors = []
    for edge in G.edges():
        if G[edge[0]][edge[1]]['cost'] == 1:
            edge_colors.append('red')  # High traffic
        elif G[edge[0]][edge[1]]['cost'] == 0.3:
            edge_colors.append('orange')  # Medium traffic
        else:
            edge_colors.append('green')  # Default color for other edges

    nx.draw(G, pos, with_labels=False, node_color=colors, node_size=node_size, edge_color=edge_colors)

    # Highlight path with blue color
    if path_edges:
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='blue', width=2)

    # Create a legend
    legend_elements = [Line2D([0], [0], marker='o', color='w', markerfacecolor=colors[i], markersize=8,
                              label=node) for i, node in enumerate(G.nodes())]

    # Add custom legend for edge colors
    legend_elements.append(Line2D([0], [0], color='w', markerfacecolor='red', markersize=8, label='High Traffic'))
    legend_elements.append(Line2D([0], [0], color='w', markerfacecolor='orange', markersize=8, label='Medium Traffic'))

    plt.legend(handles=legend_elements, loc='upper left', title='Points', fontsize=8)
    plt.show()


