#!/usr/bin/env python3

import random
from typing import Any
import mlx

# height == números de linhas
# widht == número de colunas
# mst == minimum spanning tree


class Node:
    def __init__(self, x: int, y: int) -> None:
        self.parent = self
        self.rank = 0
        self.distance = -1
        self.visited = "white"
        self.wall = 15
        self.cords = (x, y)
        self.fix = False


class Bfs():
    @staticmethod
    def short_path(
        maze,
        entry: tuple[int, int],
        exit: tuple[int, int]
    ) -> list[Node]:

        start_node = maze[entry[0]][entry[1]]
        visited: set[Node] = {start_node}

        queue: list = [(start_node, [start_node])]
        max_y = len(maze)
        max_x = len(maze[0])

        while queue:
            current, path = queue.pop(0)

            if current.cords == exit:
                return path

            y, x = current.cords

            if (current.wall & 1) == 0 and y > 0: # 1 == 0001 Norte
                neighbor = maze[y - 1][x]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

            if (current.wall & 2) == 0 and x < max_x - 1: # 2 == 0010 Leste
                neighbor = maze[y][x + 1]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

            if (current.wall & 4) == 0 and y < max_y - 1: # 4 == 0100 Sul
                neighbor = maze[y + 1][x]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

            if (current.wall & 8) == 0 and x > 0: # 8 == 1000 Oeste
                neighbor = maze[y][x - 1]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return []


class Kruskal():
    @staticmethod
    def link(x: Node, y: Node) -> None:
        if x.rank > y.rank:
            y.parent = x
        else:
            x.parent = y
            if x.rank == y.rank:
                y.rank += 1

    @staticmethod
    def find_set(x: Node) -> Node:
        if x.parent != x:
            x.parent = Kruskal.find_set(x.parent)
        return x.parent

    @staticmethod
    def union(x: Node, y: Node) -> None:
        Kruskal.link(Kruskal.find_set(x), Kruskal.find_set(y))

    @staticmethod
    def create_edge(
        maze: list[list[Node]],
        height: int, width: int
    ) -> list[tuple[Node, Node]]:
        adjacency_list: list = []
        random.shuffle(adjacency_list)
        for i in range(height):
            for j in range(width - 1):
                adjacency_list.append((maze[i][j], maze[i][j + 1]))
        for i in range(width):
            for j in range(height - 1):
                adjacency_list.append((maze[j][i], maze[j + 1][i]))
        random.shuffle(adjacency_list)
        return adjacency_list

    @staticmethod
    def kruskal_perfect(
        maze: list[list[Node]],
        height: int, width: int
    ) -> list[tuple[Node, Node]]:
        adjacency_list = Kruskal.create_edge(maze, height, width)
        mst = []
        for t in adjacency_list:
            if (
                Kruskal.find_set(t[0]) != Kruskal.find_set(t[1])
                and not (t[0].fix or t[1].fix)
            ):
                if t[0].cords[0] > t[1].cords[0]:
                    t[0].wall = t[0].wall - 2**0
                    t[1].wall = t[1].wall - 2**2
                if t[0].cords[0] < t[1].cords[0]:
                    t[0].wall = t[0].wall - 2**2
                    t[1].wall = t[1].wall - 2**0
                if t[0].cords[1] > t[1].cords[1]:
                    t[0].wall = t[0].wall - 2**3
                    t[1].wall = t[1].wall - 2**1
                if t[0].cords[1] < t[1].cords[1]:
                    t[0].wall = t[0].wall - 2**1
                    t[1].wall = t[1].wall - 2**3
                mst.append((t[0], t[1]))
                Kruskal.union(t[0], t[1])
        return mst
# 1110
# 1101
# 1011
# 0111
    @staticmethod
    def kruskal_imperfect(
        maze: list[list[Node]],
        height: int, width: int
    ) -> None:
        mst = Kruskal.kruskal_perfect(maze, height, width)
        max_y = len(maze)
        max_x = len(maze[0])
        # for i in range(max_y):
        #     for j in range(max_x):
        #         print(f"{maze[i][j].wall:x}", end="")
        #     print()
    #        print("--------")
        while Kruskal.verify(maze, max_x, max_y):
            for y in range(max_y):
                for x in range(max_x):
                    options = []
                    if maze[y][x].wall.bit_count() == 3 and not maze[y][x].fix:
                        if maze[y][x].wall & 1 == 1 and y > 0 and y - 1 > 0 and not maze[y - 1][x].fix:
                            options.append(maze[y - 1][x])
                        if maze[y][x].wall & 2 == 2 and x < max_x - 1 and not maze[y][x + 1].fix:
                            options.append(maze[y][x + 1])
                        if maze[y][x].wall & 4 == 4 and y < max_y - 1 and not maze[y + 1][x].fix:
                            options.append((maze[y + 1][x]))
                        if maze[y][x].wall & 8 == 8 and x > 0 and x - 1 >= 0 and not maze[y][x - 1].fix:
                            options.append(maze[y][x - 1])
                        print("----")
                        if options:
                            neighbor = random.choice(options)
                            print("one -", neighbor.wall, neighbor.cords, flush=True)
                            if maze[y][x].cords[0] > neighbor.cords[0]:
                                maze[y][x].wall = maze[y][x].wall - 2**0
                                neighbor.wall = neighbor.wall - 2**2
                            if maze[y][x].cords[0] < neighbor.cords[0]:
                                maze[y][x].wall = maze[y][x].wall - 2**2
                                neighbor.wall = neighbor.wall - 2**0
                            if maze[y][x].cords[1] > neighbor.cords[1]:
                                maze[y][x].wall = maze[y][x].wall - 2**3
                                neighbor.wall = neighbor.wall - 2**1
                            if maze[y][x].cords[1] < neighbor.cords[1]:
                                maze[y][x].wall = maze[y][x].wall - 2**1
                                neighbor.wall = neighbor.wall - 2**3
                            print("two -", maze[y][x].wall, maze[y][x].cords, neighbor.wall, neighbor.cords, flush=True)
            print("saiu do while")

    @staticmethod
    def verify(maze, max_x, max_y):
        for y in range(max_y):
            for x in range(max_x):
                ft_count = 0
                ft_count += 1 if x + 1 < max_x and maze[y][x + 1].fix else 0
                ft_count += 1 if x - 1 >= 0 and maze[y][x - 1].fix else 0
                ft_count += 1 if y + 1 < max_y and maze[y + 1][x].fix else 0
                ft_count += 1 if y - 1 > 0 and maze[y - 1][x].fix else 0
                if maze[y][x].wall.bit_count() == 3 and not maze[y][x].fix and ft_count < 3:
                    print(ft_count)
                    print(maze[y][x].wall, maze[y][x].cords)
                    for i in range(max_y):
                        for j in range(max_x):
                            print(f"{maze[i][j].wall:x}", end="")
                        print()

                    # print(x, y)
                    return True
        print("saido")

        return False







    # def kruskal_imperfect():
        # Em teoria é criamos uma mst
        # depois tendo a mst iteramos ela para buscar celulas celulas
        # com 3 paredes e selecionar uma parede de forma aleatorio
        # e eliminar ela, mas existem limitações
        # como não podemos criar 3x3 area aberta
        # e não pode retirar os cantos do labirinto


#     @staticmethod
#     def kruskal_imperfect(
#         maze: list[list[Node]],
#         height: int, width: int
#     ) -> list[tuple[Node, Node]]:
#
#         # 1) começa com perfeita
#         Kruskal.kruskal_perfect(maze, height, width)
#
#         # 2) cria lista inicial de "células com 3 paredes fechadas" (não-fix)
#         candidates = []
#         for y in range(height):
#             for x in range(width):
#                 c = maze[y][x]
#                 if (c.wall.bit_count() == 3) and (not c.fix):
#                     candidates.append(c)
#
#         rng = random.Random()  # ou use random.seed(...) do seu gerador
#
#         # bits -> (dx,dy, bit_deste, bit_do_vizinho)
#         # N: 1 no atual <-> 4 no vizinho
#         # E: 2 no atual <-> 8 no vizinho
#         # S: 4 no atual <-> 1 no vizinho
#         # W: 8 no atual <-> 2 no vizinho
#         DIRS = [
#             (0, -1, 1, 4),  # abre Norte do atual, remove Sul do vizinho
#             (1, 0,  2, 8),  # abre Leste do atual, remove Oeste do vizinho
#             (0, 1,  4, 1),  # abre Sul do atual, remove Norte do vizinho
#             (-1, 0, 8, 2),  # abre Oeste do atual, remove Leste do vizinho
#         ]
#
#         # (opcional) tentativas máximas pra evitar loop infinito
#         max_tries = height * width * 20
#         tries = 0
#
#         # 3) tenta abrir paredes fechadas em alguns candidatos
#         rng.shuffle(candidates)
#
#         # Para deixar estável/rápido, usamos também uma "pool" dinâmica:
#         # quando a abertura torna outro vizinho "ruim" (bit_count==3), ele entra na pool.
#         in_pool = set((n.cords[0], n.cords[1]) for n in candidates)
#
#         def try_open_edge(ax, ay, nx, ny, bit_a, bit_n):
#             """Retorna True se abriu (e aplicou), False se não abriu."""
#             a = maze[ay][ax]
#             n = maze[ny][nx]
#
#             if a.fix and n.fix:
#                 return False
#             if n.fix:
#                 return False
#
#             # se a parede já está aberta, não precisa
#             if (a.wall & bit_a) == 0:
#                 return False
#
#             # snapshot
#             old_a = a.wall
#             old_n = n.wall
#
#             # remove parede nos dois lados
#             a.wall &= ~bit_a
#             n.wall &= ~bit_n
#
#             # ---- aqui plugue seus VALIDADORES EXATOS ----
#             # Se falhar, desfaz.
#             if not validate_after_change(maze, height, width, ax, ay, nx, ny):
#                 a.wall = old_a
#                 n.wall = old_n
#                 return False
#             # -------------------------------------------
#
#             return True
#
#         while tries < max_tries and candidates:
#             tries += 1
#             c = candidates.pop()
#             ax, ay = c.cords  # note: no seu Node, cords = (x,y) ou (x,y)? no seu código: (x,y) no Node init
#             # No seu código, você usa maze[entry[0]][entry[1]] no BFS => (y,x).
#             # Mas no Node init você faz Node(j,i) e cords=(x,y) -> aqui é (x,y) = (j,i).
#             # Então: ax = c.cords[0] (coluna), ay = c.cords[1] (linha).
#             # Para indexar maze corretamente: maze[ay][ax]
#
#             # se mudou e deixou de ser 3-paredes, pode pular
#             if (maze[ay][ax].wall.bit_count() != 3) or maze[ay][ax].fix:
#                 continue
#
#             # embaralha direções pra ficar variado
#             rng_dirs = DIRS[:]
#             rng.shuffle(rng_dirs)
#
#             for dx, dy, bit_a, bit_n in rng_dirs:
#                 nx = ax + dx
#                 ny = ay + dy
#                 if not (0 <= nx < width and 0 <= ny < height):
#                     continue
#
#                 # não abra no vizinho se ele é fix
#                 if maze[ny][nx].fix:
#                     continue
#
#                 # só tenta se a parede está fechada
#                 if (maze[ay][ax].wall & bit_a) == 0:
#                     continue
#
#                 if try_open_edge(ax, ay, nx, ny, bit_a, bit_n):
#                     # se abriu com sucesso, pode tornar alguns vizinhos candidatos
#                     # adicionamos os "impactados" na pool: c e o vizinho
#                     for bx, by in [(ax, ay), (nx, ny)]:
#                         if not maze[by][bx].fix and maze[by][bx].wall.bit_count() == 3:
#                             key = (bx, by)
#                             if key not in in_pool:
#                                 in_pool.add(key)
#                                 candidates.append(maze[by][bx])
#                     # depois da primeira abertura, saia (mantém bem mais restrito)
#                     break
#
#         return []  # você não usa mst no imperfect; pode retornar algo se precisar
#
# # ---- Você precisa implementar/ligar seus validadores aqui ----
# def validate_after_change(maze, height, width, ax, ay, nx, ny):
#     """
#     Aqui você coloca seus checks:
#     - nunca deixar 3x3 aberto (conforme seu critério)
#     - corredor largura <= 2
#     - (se necessário) manter conectividade etc.
#
#     Importante: como só mudou 1 aresta, você deve checar só regiões locais
#     (3x3 que inclui ax/ay/nx/ny, etc.) pra ficar rápido.
#     """
#     # EXEMPLO (PLACEHOLDER):
#     # if would_create_3x3_open_area(...): return False
#     # if corridor_wider_than_2(...): return False
#     return True
#

class MazeGenerator:
    def __init__(
        self,
    ) -> None:
        self.dict_graph: dict[str, Any] = {}
        self.validate_config()
        self.height = self.dict_graph["height"]
        self.width = self.dict_graph["width"]
        self.entry = self.dict_graph["entry"]
        self.exit_maze = self.dict_graph["exit"]
        self.seed = self.dict_graph["seed"]
        self.perfect = self.dict_graph["perfect"]
        self.output_file = self.dict_graph["output_file"]
        self.maze: list[list[Node]] = []
        self.path = ""

    # def imprimir(self):
    #     print(self.output_file)
    def genereate_maze(self) -> None:
        self.validate_config()
        self.maze = [
            [Node(j, i) for i in range(self.dict_graph["width"])]
            for j in range(self.dict_graph["height"])
        ]
        self.logo()
        if self.perfect:
            mst = Kruskal.kruskal_perfect(self.maze, self.height, self.width)
        else:
            mst = Kruskal.kruskal_imperfect(self.maze, self.height, self.width)
        path = Bfs.short_path(self.maze, self.entry, self.exit_maze)
        path_str = ""
        for i in range(len(path) - 1):
            if path[i].cords[0] > path[i + 1].cords[0]:
                path_str += "N"
            if path[i].cords[0] < path[i + 1].cords[0]:
                path_str += "S"
            if path[i].cords[1] > path[i + 1].cords[1]:
                path_str += "W"
            if path[i].cords[1] < path[i + 1].cords[1]:
                path_str += "E"
        self.path = path_str

#        for i in range(self.height):
#            for j in range(self.width):
#                print(f"{self.maze[i][j].wall:x}", end="")
#            print()
#        print()
        print(f"{self.entry[0]},{self.entry[1]}\n{self.exit_maze[0]},{self.exit_maze[1]}")
        print(path_str)




    def logo(self) -> None:
        mid_h = int(self.dict_graph["height"] / 2)
        mid_w = int(self.dict_graph["width"] / 2)
        self.maze[mid_h][mid_w - 1].fix = True
        self.maze[mid_h][mid_w - 2].fix = True
        self.maze[mid_h][mid_w - 3].fix = True
        self.maze[mid_h - 1][mid_w - 3].fix = True
        self.maze[mid_h - 2][mid_w - 3].fix = True
        self.maze[mid_h + 1][mid_w - 1].fix = True
        self.maze[mid_h + 2][mid_w - 1].fix = True

        self.maze[mid_h][mid_w + 1].fix = True
        self.maze[mid_h][mid_w + 2].fix = True
        self.maze[mid_h][mid_w + 3].fix = True
        self.maze[mid_h - 1][mid_w + 3].fix = True
        self.maze[mid_h - 2][mid_w + 3].fix = True
        self.maze[mid_h - 2][mid_w + 2].fix = True
        self.maze[mid_h - 2][mid_w + 1].fix = True
        self.maze[mid_h + 1][mid_w + 1].fix = True
        self.maze[mid_h + 2][mid_w + 1].fix = True
        self.maze[mid_h + 2][mid_w + 2].fix = True
        self.maze[mid_h + 2][mid_w + 3].fix = True

        if self.maze[self.entry[0] - 1][self.entry[1] - 1].fix == True:
            print("Maze entry is the same as 42 logo")
            exit(1)

        if self.maze[self.exit_maze[0] - 1][self.exit_maze[1] - 1].fix == True:
            print("Maze exit is the same as 42 logo")
            exit(1)

# def parse_config(file: str) -> dict(int, int, tuplent, int):


    def validate_config(self) -> None:
        error_msg: str = (
            "Error while reading config.txt"
            "\nPlease open the file and write the values in the format:"
            "\nWIDTH=<int>0>"
            "\nHEIGHT=<int>0>"
            "\nENTRY=<int,int>"
            "\nEXIT=<int,int>"
            "\nOUTPUT_FILE=<*.txt>"
            "\nPERFECT=<bool>"
            "\nSEED=<int> or leave it blank"
        )
        dict_raw: dict[str, str] = {}
        try:
            with open("config.txt", "r") as f:
                for line in f:
                    if line == "\n" or line.strip().startswith("#"):
                        continue
                    key, value = line.split("=", 1)
                    key = key.lower()
                    value = value.strip()
                    dict_raw[key] = value
        except Exception:
            print(error_msg)
            exit(1)
        try:
            self.dict_graph["width"] = int(dict_raw["width"])
            self.dict_graph["height"] = int(dict_raw["height"])
            self.dict_graph["perfect"] = False
            self.dict_graph["output_file"] = dict_raw["output_file"]
            if dict_raw["seed"]:
                self.dict_graph["seed"] = int(dict_raw["seed"])
                random.seed(self.dict_graph["seed"])
            else:
                self.dict_graph["seed"] = "random"
            # self.dict_graph["seed"] = "random"
            # if dict_raw["seed"] != "random":
            #     self.dict_graph["seed"] = int(dict_raw["seed"])
            #     random.seed(dict_graph[])
            if not dict_raw["output_file"].endswith(".txt"):
                print(error_msg)
                exit(1)
            entry = dict_raw["entry"].split(",")
            exit_maze = dict_raw["exit"].split(",")
            if len(entry) != 2 or len(exit_maze) != 2:
                print(error_msg)
                exit(1)
            self.dict_graph["entry"] = (int(entry[0]), int(entry[1]))
            self.dict_graph["exit"] = (int(exit_maze[0]), int(exit_maze[1]))
            if not (
                int(entry[0]) <= int(self.dict_graph["height"])
                and int(entry[1]) <= int(self.dict_graph["width"])
                and int(exit_maze[0]) <= int(self.dict_graph["height"])
                and int(exit_maze[1]) <= int(self.dict_graph["width"])
                and int(entry[0]) >= 0
                and int(entry[1]) >= 0
                and int(exit_maze[0])
                and int(exit_maze[1]) >= 0
            ):
                print(error_msg)
                exit(1)
            for key in self.dict_graph.keys():
                if not (key == "widht" or "height" or "entry" or "exit"
                        or "output_file" or "perfect" or "seed"):
                    print(error_msg)
                    exit(1)

            if len(self.dict_graph.keys()) != 7:
                print(error_msg)
                exit(1)
        except Exception:
            print(error_msg)
            exit(1)

    def save_file(self) -> None:
        try:
            with open(self.output_file, "w") as file:
                for row in range(self.height):
                    for node in range(self.width):
                        file.write(f"{self.maze[row][node].wall:x}")
                    file.write("\n")
                file.write("\n")
                file.write(f"{self.entry[0]},{self.entry[1]}\n")
                file.write(f"{self.exit_maze[0]},{self.exit_maze[1]}\n")
                file.write(self.path)
            print(f"Maze succesfully save in: {self.output_file}")

        except Exception:
            print("Error while tring to save output file.")


# def print_hex_maze(hex_map: list[str]) -> None:
#     if not hex_map:
#         return
#
#     # Desenha o teto (Norte) apenas da primeira linha
#     top_border: str = "+"
#     for char in hex_map[0]:
#         val: int = int(char, 16)
#         # Verifica Bit 0 (Norte)
#         top_border += "---+" if (val & 1) else "   +"
#     print(top_border)
#
#     for line in hex_map:
#         # A parede Oeste (Esquerda) só é checada na primeira célula da linha
#         first_val: int = int(line[0], 16)
#         row_str: str = "|" if (first_val & 8) else " "
#
#         bottom_str: str = "+"
#
#         for char in line:
#             val = int(char, 16)
#
#             # O centro da célula (podemos colocar um " " ou um "X" se for o caminho)
#             cell_center: str = "   "
#
#             # Verifica Bit 1 (Leste / Direita)
#             row_str += f"{cell_center}|" if (val & 2) else f"{cell_center} "
#
#             # Verifica Bit 2 (Sul / Baixo)
#             bottom_str += "---+" if (val & 4) else "   +"
#
#         print(row_str)
#         print(bottom_str)
#
# if __name__ == "__main__":
#     # O seu dump hexadecimal
#     my_maze: list[str] = [
#         "957bd11555791539513b",
#         "8556d2e9113aad2ad686",
#         "8553d2d6eec2ebc053eb",
#         "83b83c17d53a9456d056",
#         "ac6aa92d3baead513ebb",
#         "87baeac78045297e8782",
#         "ed0454116ad10039016a",
#         "bd2bbd6c3ebeee86ec7a",
#         "8542a93f816fffc397d6",
#         "ebd006efec557f928557",
#         "d03ea97fffbfffaa83d3",
#         "d68386d13fafd56c6856",
#         "bd6a87beafafffd15413",
#         "c152838103abbbd453ee",
#         "b87c6c2eec06847b9413",
#         "c6bbb90397c3839003ae",
#         "b94042ac07d06aeeaac3",
#         "82d43aebad56b87beed2",
#         "aad56812c53bc6941152",
#         "ec557eeed5447d6d6c7e",
#     ]
#
#     print_hex_maze(my_maze)
#
def end(data):
    print("Encerrrando janela....")
    mlx, mlx_ptr, mlx_win = data
    print(data)
    print("oi.....")
    mlx.mlx_destroy_window(mlx_ptr, mlx_win)
    mlx.mlx_loop_exit(mlx_ptr)
    exit(0)

if __name__ == "__main__":
    maze = MazeGenerator()
    maze.genereate_maze()
    maze.save_file()
    size = 20
    mlx = mlx.Mlx()
    mlx_ptr = mlx.mlx_init()
    mlx_win = mlx.mlx_new_window(mlx_ptr, maze.width * size, maze.height * size, "a-maze-ing")
    mlx.mlx_hook(mlx_win, 33, 0, end, (mlx, mlx_ptr, mlx_win))
    # end((mlx, mlx_ptr, mlx_win))
    mlx.mlx_loop(mlx_ptr)
    
#    print(f"{maze.dict_graph}")
