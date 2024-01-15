import nodes
import queue2
import Graph


def get_heuristic_value(heuristic: list, city: str) -> int:
    for h in heuristic:
        if h['origem'] == city:
            return h['distancia']
    return -1


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
    while not (node is None):
        if node.get_parent() is None:
            path.insert(0, [node.get_name(), node.get_total_cost(), "(root)"])
        else:
            path.insert(0, [node.get_name(), node.get_total_cost(), node.get_parent().get_name()])

        node = node.get_parent()
    for step in path:
        print(step[2], "-", step[1], "->", step[0])


def start_search(start_city, goal_city, cities):
    root = nodes.Node(start_city, None, 0)

    frontier_nodes = queue2.Queue()
    visited_nodes = []
    end = False
    solution = False
    last_node = None

    # frontier_nodes.push(root)
    frontier_nodes.add(root)
    while not end:
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

            if node.get_name() == goal_city:
                end = True
                solution = True
                last_node = node
                print("Solution found!")
            else:
                # Preparar h_star
                # Get information about heuristics
                heuristic = cities["heuristicas"]
                for cn in cities["conexoes"]:
                    if node.get_name() == cn["origem"]:
                        if not in_nodes_list(cn["destino"], visited_nodes):
                            # Preparar h_star #
                            value = get_heuristic_value(heuristic, cn["destino"])
                            print("Heuristic from the city ", cn["destino"], " to Faro is:", value)

                            new_node = nodes.Node(cn["destino"], node, cn["cost"])
                            # Test
                            print("New node not in the frontiers and not visited!")
                            frontier_nodes.add(new_node)
                        # Test
                frontier_nodes.print_queue("Queue")
    if solution:
        print("Last node:", last_node.get_name())
        print("Root node:", root.get_name())
        print_path(last_node)

        # Construir lista de arestas do caminho
        path_edges = []
        node = last_node
        while node.get_parent() is not None:
            path_edges.insert(0, (node.get_parent().get_name(), node.get_name()))
            node = node.get_parent()

        return path_edges
