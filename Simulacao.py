import json
import tkinter as tk
import time
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

        # Adiciona um rótulo para exibir a hora
        self.time_label = tk.Label(self.root, text="")
        self.time_label.pack()

        # Inicializa a hora simulada com a hora atual
        self.simulated_time = time.localtime()
        self.update_time()

        # Adiciona um widget de entrada para alterar a hora
        self.time_entry = tk.Entry(self.root)
        self.time_entry.pack()

        # Adiciona um botão para definir a hora
        set_time_button = tk.Button(self.root, text="Definir hora", command=self.set_time)
        set_time_button.pack()

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
        self.G = Graph.create_graph_from_json("PontosTuristicos.conf")

    def update_time(self):
        # Atualiza o rótulo da hora com a hora simulada
        self.time_label.config(text=time.strftime("%H:%M:%S", self.simulated_time))
        self.root.after(1000, self.update_time)

    def update_costs_general(self):
        # Obtém a hora atual
        current_hour = self.simulated_time.tm_hour

        # Ajusta os custos das conexões com base na hora do dia
        if 8 <= current_hour <= 11 or 16 <= current_hour <= 19:
            for conexao in self.cities["conexoes"]:
                conexao["cost"] += 2
                # Atualiza o custo da conexão correspondente no grafo
                self.G[conexao["origem"]][conexao["destino"]]['cost'] += 2
                self.G[conexao["destino"]][conexao["origem"]]['cost'] += 2
        else:
            for conexao in self.cities["conexoes"]:
                conexao["cost"] = max(0, conexao["cost"] - 1)
                # Atualiza o custo da conexão correspondente no grafo
                self.G[conexao["origem"]][conexao["destino"]]['cost'] = max(0, self.G[conexao["origem"]][
                    conexao["destino"]]['cost'] - 1)
                self.G[conexao["destino"]][conexao["origem"]]['cost'] = max(0, self.G[conexao["destino"]][
                    conexao["origem"]]['cost'] - 1)

    def update_costs(self):
        # Obtém a hora atual
        current_hour = self.simulated_time.tm_hour

        # Ajusta os custos das conexões com base na hora do dia
        if 8 <= current_hour <= 11 or 16 <= current_hour <= 19:
            for conexao in self.cities["conexoes"]:
                # Aumenta o custo em 1 para todas as conexões
                conexao["cost"] += 1
                self.G[conexao["origem"]][conexao["destino"]]['cost'] += 1
                self.G[conexao["destino"]][conexao["origem"]]['cost'] += 1

                # Aumenta o custo adicionalmente em 2 para as conexões entre "Torre de Belém" e "Mosteiro dos Jerónimos"
                if (conexao["origem"] == "Torre de Belém" and conexao["destino"] == "Mosteiro dos Jerónimos") or \
                        (conexao["origem"] == "Mosteiro dos Jerónimos" and
                         conexao["destino"] == "Pastéis de Belém") or \
                        (conexao["origem"] == "Pastéis de Belém" and conexao["destino"] == "Avenida da Liberdade"):
                    conexao["cost"] += 2
                    self.G[conexao["origem"]][conexao["destino"]]['cost'] += 2
                    self.G[conexao["destino"]][conexao["origem"]]['cost'] += 2
                # Aumenta o custo adicionalmente em 3 para as conexões entre
                # "Mosteiro dos Jerónimos" e "Padrão dos Descobrimentos"
                elif (conexao["origem"] == "Mosteiro dos Jerónimos" and conexao[
                    "destino"] == "Padrão dos Descobrimentos") or \
                        (conexao["origem"] == "Padrão dos Descobrimentos" and conexao[
                            "destino"] == "Praça do Comércio") or \
                        (conexao["origem"] == "Praça do Comércio" and conexao["destino"] == "Castelo de São Jorge"):
                    conexao["cost"] += 3
                    self.G[conexao["origem"]][conexao["destino"]]['cost'] += 3
                    self.G[conexao["destino"]][conexao["origem"]]['cost'] += 3
        elif 2 <= current_hour <= 3:
            for conexao in self.cities["conexoes"]:
                conexao["cost"] = max(0, conexao["cost"] - 0.1)
                # Atualiza o custo da conexão correspondente no grafo
                self.G[conexao["origem"]][conexao["destino"]]['cost'] = max(0, self.G[conexao["origem"]][
                    conexao["destino"]]['cost'] - 0.1)
                self.G[conexao["destino"]][conexao["origem"]]['cost'] = max(0, self.G[conexao["destino"]][
                    conexao["origem"]]['cost'] - 0.1)
        else:
            for conexao in self.cities["conexoes"]:
                conexao["cost"] = max(0, conexao["cost"] - 2)
                self.G[conexao["origem"]][conexao["destino"]]['cost'] = max(0, self.G[conexao["origem"]][
                    conexao["destino"]]['cost'] - 2)
                self.G[conexao["destino"]][conexao["origem"]]['cost'] = max(0, self.G[conexao["destino"]][
                    conexao["origem"]]['cost'] - 2)

    def set_time(self):
        # Define a hora simulada conforme a entrada do utilizador
        time_string = self.time_entry.get()
        try:
            new_time = time.strptime(time_string, "%H:%M:%S")  # Verifica se a hora está no formato correto
            # Atualiza a hora simulada, mantendo a data atual
            self.simulated_time = time.struct_time(
                (self.simulated_time.tm_year, self.simulated_time.tm_mon, self.simulated_time.tm_mday,
                 new_time.tm_hour, new_time.tm_min, new_time.tm_sec,
                 self.simulated_time.tm_wday, self.simulated_time.tm_yday, self.simulated_time.tm_isdst))
            # Atualiza os custos das conexões
            self.update_costs()
            # Atualiza o gráfico
            self.fig = plt.figure()  # Cria uma nova figura
            Graph.draw_graph(self.G)  # Desenha o gráfico na figura

            # Remove o canvas antigo
            self.canvas.get_tk_widget().pack_forget()

            # Cria um canvas e adiciona à janela Tkinter
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack()

        except ValueError:
            print("Hora inválida! Por favor, insira a hora no formato HH:MM:SS.")

    def start_search_and_draw_path(self):
        start_city = self.start_entry.get()
        goal_city = self.goal_entry.get()

        # Obtém a hora atual
        current_hour = self.simulated_time.tm_hour

        # Cria uma cópia das cidades para não modificar os dados originais
        cities_copy = self.cities.copy()

        # Ajusta os custos das conexões com base na hora do dia
        if 12 <= current_hour <= 18:
            for conexao in cities_copy["conexoes"]:
                conexao["cost"] *= 2

        # Use o grafo atualizado para a pesquisa
        path_edges = H_star.start_search(start_city, goal_city, cities_copy)
        self.draw_path(path_edges, self.G)

    def draw_path(self, path_edges, G):
        # Cria uma figura
        self.fig = plt.figure()

        # Usa o grafo atualizado para desenhar o gráfico
        Graph.draw_graph(G, path_edges)

        # Remove o canvas antigo
        self.canvas.get_tk_widget().pack_forget()

        # Cria um canvas e adiciona à janela Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def advance_time(self):
        # Avança a hora simulada em 60 minutos
        new_time = time.localtime(time.mktime(self.simulated_time) + 60 * 60)
        self.simulated_time = time.struct_time(
            (new_time.tm_year, new_time.tm_mon, new_time.tm_mday,
             new_time.tm_hour, new_time.tm_min, new_time.tm_sec,
             new_time.tm_wday, new_time.tm_yday, new_time.tm_isdst))
        # Atualiza os custos das conexões
        self.update_costs()
        # Atualiza o gráfico
        self.update_graph()

    def update_graph(self):
        self.fig = plt.figure()  # Cria uma figura
        Graph.draw_graph(self.G)  # Desenha o gráfico na figura

        # Remove o canvas antigo
        self.canvas.get_tk_widget().pack_forget()

        # Cria um canvas e adiciona à janela Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def run(self):
        self.advance_time()
        self.root.after(15000, self.run)
        self.root.mainloop()


def main():
    cities = read_file("./PontosTuristicos.conf")
    window = GraphWindow(cities)
    window.run()


if __name__ == '__main__':
    main()
