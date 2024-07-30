import networkx as nx
import matplotlib.pyplot as plt
import random
import tkinter as tk
from tkinter import simpledialog

# Função para gerar custos aleatórios
def gerar_custo():
    return random.randint(1, 16)

# Criar a rede de roteadores
G = nx.DiGraph()

# Adicionar os roteadores com rótulos formatados
routers = [f"ISR4331\nRouter{i}" for i in range(12) if i not in (1, 6)]
G.add_nodes_from(routers)

# Adicionar as conexões com custos aleatórios
conexoes = [
    ("ISR4331\nRouter0", "ISR4331\nRouter2"),
    ("ISR4331\nRouter0", "ISR4331\nRouter3"),
    ("ISR4331\nRouter2", "ISR4331\nRouter4"),
    ("ISR4331\nRouter2", "ISR4331\nRouter0"),
    ("ISR4331\nRouter3", "ISR4331\nRouter8"),
    ("ISR4331\nRouter3", "ISR4331\nRouter0"),
    ("ISR4331\nRouter3", "ISR4331\nRouter9"),
    ("ISR4331\nRouter4", "ISR4331\nRouter5"),
    ("ISR4331\nRouter4", "ISR4331\nRouter2"),
    ("ISR4331\nRouter4", "ISR4331\nRouter8"),
    ("ISR4331\nRouter4", "ISR4331\nRouter10"),
    ("ISR4331\nRouter5", "ISR4331\nRouter7"),
    ("ISR4331\nRouter5", "ISR4331\nRouter9"),
    ("ISR4331\nRouter5", "ISR4331\nRouter4"),
    ("ISR4331\nRouter7", "ISR4331\nRouter11"),
    ("ISR4331\nRouter7", "ISR4331\nRouter5"),
    ("ISR4331\nRouter8", "ISR4331\nRouter3"),
    ("ISR4331\nRouter8", "ISR4331\nRouter4"),
    ("ISR4331\nRouter8", "ISR4331\nRouter10"),
    ("ISR4331\nRouter9", "ISR4331\nRouter5"),
    ("ISR4331\nRouter9", "ISR4331\nRouter3"),
    ("ISR4331\nRouter10", "ISR4331\nRouter11"),
    ("ISR4331\nRouter10", "ISR4331\nRouter4"),
    ("ISR4331\nRouter10", "ISR4331\nRouter8"),
    ("ISR4331\nRouter11", "ISR4331\nRouter7"),
    ("ISR4331\nRouter11", "ISR4331\nRouter10"),
]

for origem, destino in conexoes:
    if origem in G.nodes and destino in G.nodes:
        G.add_edge(origem, destino, weight=gerar_custo())

# Função para encontrar o melhor caminho usando o algoritmo de Dijkstra
def melhor_caminho(G, inicio, fim):
    return nx.dijkstra_path(G, inicio, fim), nx.dijkstra_path_length(G, inicio, fim)

# Visualizar a rede de roteadores e o caminho encontrado
def visualizar_rede(G, caminho=None, resumo=None):
    pos = {
        "ISR4331\nRouter0": (0.1, 0.7),
        "ISR4331\nRouter2": (0.2, 0.5),
        "ISR4331\nRouter3": (0.3, 0.8),
        "ISR4331\nRouter4": (0.4, 0.4),
        "ISR4331\nRouter5": (0.6, 0.2),
        "ISR4331\nRouter7": (0.8, 0.2),
        "ISR4331\nRouter8": (0.6, 0.8),
        "ISR4331\nRouter9": (0.7, 0.5),
        "ISR4331\nRouter10": (0.8, 0.8),
        "ISR4331\nRouter11": (0.9, 0.4)
    }
    labels = nx.get_edge_attributes(G, 'weight')

    fig, ax = plt.subplots(figsize=(12, 8))

    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold", arrows=True, ax=ax)

    # Adicionar os rótulos das arestas com fundo amarelo, garantindo que cada aresta tenha apenas um rótulo
    seen_edges = set()
    for (n1, n2), label in labels.items():
        if (n1, n2) not in seen_edges and (n2, n1) not in seen_edges:
            x = (pos[n1][0] + pos[n2][0]) / 2 + random.uniform(-0.02, 0.02)
            y = (pos[n1][1] + pos[n2][1]) / 2 + random.uniform(-0.02, 0.02)
            ax.text(x, y, label, size=12, color='black', bbox=dict(facecolor='yellow', alpha=0.5))
            seen_edges.add((n1, n2))

    if caminho:
        path_edges = list(zip(caminho, caminho[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2, ax=ax)

    # Adicionar cabeçalho
    plt.figtext(0.5, 0.97, "Trabalho 2 - Redes de Computadores I - Prof. Ronaldo Toshiaki Oikawa - Algoritmo Dijkstra", ha='center', fontsize=14, bbox={"facecolor":"white", "alpha":0.5, "pad":5})
    plt.figtext(0.51, 0.93, "Aluno: Filipe Nava", ha='center', fontsize=12, bbox={"facecolor":"white", "alpha":0.5, "pad":5})

    # Adicionar resumo na parte inferior esquerda
    if resumo:
        plt.figtext(0.2, 0.01, resumo, ha='left', fontsize=12, bbox={"facecolor":"yellow", "alpha":0.5, "pad":5})

    plt.title("Rede de Roteadores", y=1.00)
    plt.show()

# Interface gráfica para selecionar os roteadores de início e fim
def obter_entrada():
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal

    inicio_num = simpledialog.askinteger("Entrada", "Digite o número do roteador de início (0 ou 2 até 5 ou 7 até 11):")
    fim_num = simpledialog.askinteger("Entrada", "Digite o número do roteador de fim (0 ou 2 até 5 ou 7 até 11):")

    return inicio_num, fim_num

inicio_num, fim_num = obter_entrada()

# Adicionar o prefixo "ISR4331\nRouter" aos números de entrada
inicio = f"ISR4331\nRouter{inicio_num}"
fim = f"ISR4331\nRouter{fim_num}"

# Encontrar e exibir o melhor caminho e seu custo
caminho, custo = melhor_caminho(G, inicio, fim)
resumo = f"Melhor caminho de {inicio} para {fim}: {' -> '.join(caminho)} com custo total de {custo}"
print(resumo)

# Visualizar a rede com o melhor caminho destacado
visualizar_rede(G, caminho, resumo)
