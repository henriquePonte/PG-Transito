import json
import tkinter as tk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import H_star
import Graph


def read_file(cities: str) -> list:
    with open(cities, encoding="utf-8") as config_file:
        # Reading the configuration file
        lst = json.load(config_file)
        # Test: printing config file
        print("Configuração:", lst)
    return lst


class GraphWindow:
    def __init__(self, cities):
        self.root = tk.Tk()
        self.cities = cities
        self.fig = Graph.create_and_draw_graph("PontosTuristicos.conf")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        start_label = tk.Label(self.root, text="Digite a cidade de início ou 'sair' para parar: ")
        start_label.pack()
        self.start_entry = tk.Entry(self.root)
        self.start_entry.pack()

        goal_label = tk.Label(self.root, text="Digite a cidade de fim: ")
        goal_label.pack()
        self.goal_entry = tk.Entry(self.root)
        self.goal_entry.pack()

        start_button = tk.Button(self.root, text="Iniciar busca",
                                 command=self.start_search_and_draw_path)
        start_button.pack()

    def start_search_and_draw_path(self):
        path_edges = H_star.start_search(self.start_entry.get(), self.goal_entry.get(), self.cities)
        self.draw_path(path_edges)

    def draw_path(self, path_edges):
        # Cria uma nova figura
        self.fig = plt.figure()

        G = Graph.create_graph_from_json("./PontosTuristicos.conf")
        Graph.draw_graph_teste(G, path_edges)

        # Remove o canvas antigo
        self.canvas.get_tk_widget().pack_forget()

        # Cria um novo canvas e adiciona à janela Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def run(self):
        self.root.mainloop()


def main():
    cities = read_file("./PontosTuristicos.conf")
    window = GraphWindow(cities)
    window.run()


if __name__ == '__main__':
    main()