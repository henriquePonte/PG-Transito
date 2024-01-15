import json
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import H_star
import nodes
import Graph


def read_file(cities: str) -> list:
    with open(cities, encoding="utf-8") as config_file:
        # Reading the configuration file
        lst = json.load(config_file)
        # Test: printing config file
        print("Configuração:", lst)
    return lst


def change_cost(cities, origem, destino, new_cost):
    found = False
    for conexao in cities["conexoes"]:
        if (conexao["origem"] == origem and conexao["destino"] == destino) or \
                (conexao["origem"] == destino and conexao["destino"] == origem):
            conexao["cost"] = new_cost
            found = True
    if found:
        return "O custo foi atualizado com sucesso."
    else:
        return "Conexão não encontrada."


def main():
    # Preparar h_star
    cities = read_file("./PontosTuristicos.conf")
    fig = Graph.create_and_draw_graph("PontosTuristicos.conf")

    # Criação da janela Tkinter
    root = tk.Tk()

    # Criação do widget de entrada para a cidade inicial
    start_label = tk.Label(root, text="Digite a cidade de início ou 'sair' para parar: ")
    start_label.pack()
    start_entry = tk.Entry(root)
    start_entry.pack()

    # Criação do widget de entrada para a cidade final
    goal_label = tk.Label(root, text="Digite a cidade de fim: ")
    goal_label.pack()
    goal_entry = tk.Entry(root)
    goal_entry.pack()

    # Criação do botão para iniciar a busca
    start_button = tk.Button(root, text="Iniciar busca",
                             command=lambda: start_search_and_draw_path(start_entry.get(), goal_entry.get(), cities))
    start_button.pack()

    # Adicionando o gráfico à janela Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    root.mainloop()


def start_search_and_draw_path(start_city, goal_city, cities):
    path_edges = H_star.start_search(start_city, goal_city, cities)
    G = Graph.create_graph_from_json("./PontosTuristicos.conf")
    Graph.draw_graph_teste(G, path_edges)


main()
