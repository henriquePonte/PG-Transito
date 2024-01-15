import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
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


def create_and_draw_graph(json_file):
    G = create_graph_from_json(json_file)

    fig, ax = plt.subplots()
    draw_graph(G)
    return fig

def draw_graph(G, path_edges=None):
    pos = nx.get_node_attributes(G, 'pos')

    # Set different colors for each node
    colors = plt.cm.rainbow(np.linspace(0, 1, len(G.nodes())))

    # Adjust the size of the nodes
    node_size = 60

    # Draw edges with different colors based on traffic
    edge_colors = []
    for edge in G.edges():
        if G[edge[0]][edge[1]]['cost'] < 5:
            edge_colors.append('green')  # Sem Tráfego
        elif G[edge[0]][edge[1]]['cost'] < 10:
            edge_colors.append('yellow')  # Tráfego Ligeiro
        elif 10 <= G[edge[0]][edge[1]]['cost'] <= 30:
            edge_colors.append('orange')  # Tráfego Medio
        else:
            edge_colors.append('red')  # Tráfego Grave

    # Draw nodes with numbers
    node_numbers = {node: str(i + 1) for i, node in enumerate(G.nodes())}
    nx.draw_networkx_labels(G, pos, labels=node_numbers, font_color='black', font_size=8, font_weight='bold')

    nx.draw(G, pos, with_labels=False, node_color=colors, node_size=node_size, edge_color=edge_colors)

    # Highlight path with blue color
    if path_edges:
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='blue', width=2)

    # Legenda das Arrestas
    legend_elements_nodes = [Line2D([0], [0], marker='o', color='w', markerfacecolor=colors[i], markersize=8,
                                     label=f'{node}: {node_numbers[node]}') for i, node in enumerate(G.nodes())]

    # Legenda das arrestas de tráfego
    legend_elements_edges = [
        Line2D([0], [0], color='green', label='Sem Tráfego'),
        Line2D([0], [0], color='yellow', label='Tráfego Ligeiro'),
        Line2D([0], [0], color='orange', label='Tráfego Medio'),
        Line2D([0], [0], color='red', label='Tráfego Grave')
    ]

    # Ajusta a possição da legenda
    plt.legend(handles=legend_elements_nodes + legend_elements_edges, bbox_to_anchor=(1.05, 1), loc='upper left',
               title='Pontos Turisticos', fontsize=8)
    plt.tight_layout()
    plt.show()