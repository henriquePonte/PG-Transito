import json
import nodes
import queue2
import networkx as nx
import matplotlib.pyplot as plt


def create_graph_from_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    G = nx.DiGraph()
    for connection in data['connections']:
        G.add_edge(connection['from'], connection['to'], cost=connection['cost'])
    return G


def draw_graph(G):
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_edges(G, pos, width=2)
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
    edge_labels = nx.get_edge_attributes(G, 'cost')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.axis('off')
    plt.show()


def create_and_draw_graph(json_file):
    G = create_graph_from_json(json_file)
    draw_graph(G)


def print_nodes(dsc: str, ns: list):
    print(dsc, ":")
    for n in ns:
        n.print()


def print_path(last: nodes.Node):
    """
    Print the sequence of steps (with increasing cost) from root to goal node
    :return:
    """
    node = last
    path = []
    while (not (node is None)):
        if node.get_parent() is None:
            path.insert(0, [node.get_name(), node.get_total_cost(), "(root)"])
        else:
            path.insert(0, [node.get_name(), node.get_total_cost(), node.get_parent().get_name()])

        node = node.get_parent()
    for step in path:
        print(step[2], "-", step[1], "->", step[0])


def in_nodes_list(nm: str, nodes: list) -> bool:
    names_list = []
    for n in nodes:
        names_list.append(n.get_name())
    # Test
    # print("in_nodes_list:",names_list)
    if nm in names_list:
        return True
    else:
        return False


# Example of Search using cities
def read_file(cities: str) -> list:
    with open(cities) as config_file:
        # Reading the configuration file
        lst = json.load(config_file)
        # Test: printing config file
        print("Configuração:", lst)
    return lst


def get_heuristic_value(heuristic: list, city: str) -> int:
    for h in heuristic:
        if h['from'] == city:
            return h['distance']
    return -1


def main():
    # cities = read_file("./cities.conf")
    ### Preparar h_star ###
    cities = read_file("./cities_heuristic.conf")

    # root
    root = nodes.Node("Arrifes", None, 0)

    frontier_nodes = queue2.Queue()
    visited_nodes = []
    end = False
    solution = False
    last_node = None
    goal_node_name = "Candelaria"
    # frontier_nodes.push(root)
    frontier_nodes.add(root)
    while end == False:
        # Test
        print("Size of frontiers nodes:", frontier_nodes.get_size())
        if frontier_nodes.empty():
            end = True
            print("Solution not found!")
        else:
            node = frontier_nodes.get_sorted()
            visited_nodes.append(node)
            if not frontier_nodes.empty():
                print("Node name to remove:", node.get_name())
                frontier_nodes.remove_by_name(node)
            # Test
            print("Frontier after removing:")
            frontier_nodes.print_queue("after removing")

            if node.get_name() == goal_node_name:
                end = True
                solution = True
                last_node = node
                print("Solution found!")
            else:
                ### Preparar h_star ###
                # Get information about heuristics
                heuristic = cities["heuristic"]
                for cn in cities["connections"]:
                    if node.get_name() == cn["from"]:
                        if not in_nodes_list(cn["to"], visited_nodes):
                            #### Preparar h_star ###
                            value = get_heuristic_value(heuristic, cn["to"])
                            print("Heuristic from the city ", cn["to"], " to Faro is:", value)

                            new_node = nodes.Node(cn["to"], node, cn["cost"])
                            # Test
                            print("New node not in the frontiers and not visited!")
                            frontier_nodes.add(new_node)
                        # Test
                frontier_nodes.print_queue("Queue")
    if solution == True:
        print("Last node:", last_node.get_name())
        print("Root node:", root.get_name())
        print_path(last_node)


create_and_draw_graph("cities_heuristic.conf")
main()
