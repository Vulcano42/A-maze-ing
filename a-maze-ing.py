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



def end(data):
    print("Encerrrando janela....")
    mlx, mlx_ptr, win_ptr = data
    print(data)
    print("oi.....")
    mlx.mlx_destroy_window(mlx_ptr, win_ptr)
    mlx.mlx_loop_exit(mlx_ptr)

def paint_block(mlx, mlx_ptr, win_ptr, color, size_x, size_y, x, y):
    for pos_x in range(size_x):
        for pos_y in range(size_y):
            mlx.mlx_pixel_put(mlx_ptr, win_ptr, x + pos_x, y + pos_y, color)


# def put_block_pixel(maze, mlx, mlx_ptr, win_ptr, size):
#     pos_y = 0
#     pos_x = 0
#     main_color = 0x101821
#     wall_color = 0x7d92ab
#     # ft_color = 0xcdd9e7
#     for line in maze:
#         for node in line:
#             paint_block(mlx, mlx_ptr, win_ptr, main_color, size, size, pos_x, pos_y)
#             if node.wall & 1 == 1 and not node.fix:
#                 paint_block(mlx, mlx_ptr, win_ptr, wall_color, 5, size, pos_x, pos_y)
#             if node.wall & 2 == 2 and not node.fix:
#                 paint_block(mlx, mlx_ptr, win_ptr, wall_color, size, 5, pos_x, pos_y + size - 5 - 1)
#             if node.wall & 4 == 4 and not node.fix:
#                 paint_block(mlx, mlx_ptr, win_ptr, wall_color, 5, size, pos_x + size - 5 - 1, pos_y + 0)
#             if node.wall & 8 == 8 and not node.fix:
#                 paint_block(mlx, mlx_ptr, win_ptr, wall_color, size, 5, pos_x, pos_y)
#             pos_x += size
#             pos_y += size

def put_block_pixel(maze, mlx, mlx_ptr, win_ptr, size):
    pos_y = 0
    # main_color = 0x101821
    # wall_color = 0x7d92ab
    main_color = 0xFF0000  # Vermelho forte (Para ter certeza que está pintando)
    wall_color = 0x00FF00  # Verde forte
    # ft_color = 0xcdd9e7
    print("dentro de put")
    
    for line in maze:
        pos_x = 0  # CORREÇÃO 1: Zera a posição X ao iniciar uma nova linha
        
        for node in line:
            paint_block(mlx, mlx_ptr, win_ptr, main_color, size, size, pos_x, pos_y)
            
            if node.wall & 1 == 1 and not node.fix:
                paint_block(mlx, mlx_ptr, win_ptr, wall_color, 5, size, pos_x, pos_y)
            if node.wall & 2 == 2 and not node.fix:
                # CORREÇÃO 3: Removido o "- 1"
                paint_block(mlx, mlx_ptr, win_ptr, wall_color, size, 5, pos_x, pos_y + size - 5)
            if node.wall & 4 == 4 and not node.fix:
                # CORREÇÃO 3: Removido o "- 1" e o "+ 0" inútil
                paint_block(mlx, mlx_ptr, win_ptr, wall_color, 5, size, pos_x + size - 5, pos_y)
            if node.wall & 8 == 8 and not node.fix:
                paint_block(mlx, mlx_ptr, win_ptr, wall_color, size, 5, pos_x, pos_y)
            
            pos_x += size  # Avança o X para o próximo bloco da mesma linha
            
        # CORREÇÃO 2: Esta linha deve ficar FORA do loop interno (for node in line:)
        pos_y += size  # Avança o Y para a linha de baixo apenas quando a linha inteira acabar


# COR PRINCIPAL == 101821
# COR PAREDE == 7d92ab
# COR CAMINHO == 65d4ee
# COR 42 == cdd9e7
# tamanho de cada quadrado == 20px

def render_maze(params):
    maze, mlx, mlx_ptr, win_ptr, size = params
    print("Renderizando Labirinto")
    put_block_pixel(maze, mlx, mlx_ptr, win_ptr, size)

foi_renderizado = False

def loop_render(params):
    global foi_renderizado
    # Se ainda não foi pintado, desenha tudo e trava a função
    if not foi_renderizado:
        maze_data, mlx_obj, mlx_p, win_p, sz = params
        print("Renderizando Labirinto no WSL...")
        put_block_pixel(maze_data, mlx_obj, mlx_p, win_p, sz)
        foi_renderizado = True

def key_hook(params, keycode):
    maze, mlx, mlx_ptr, win_ptr, size = params
    print(f"Tecla acionada! Forçando desenho imediato...")
    put_block_pixel(maze, mlx, mlx_ptr, win_ptr, size)

def render_handler(params):
    mlx, mlx_ptr, win_ptr, img_ptr = params
    # Joga a imagem inteira na janela na posição x=0, y=0
    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)

if __name__ == "__main__":
    maze = MazeGenerator()
    maze.genereate_maze()
    maze.save_file()
    size = 20
    mlx = mlx.Mlx()
    mlx_ptr = mlx.mlx_init()
    win_ptr = mlx.mlx_new_window(mlx_ptr, maze.width * size, maze.height * size, "a-maze-ing")
    img_ptr = mlx.mlx_new_image(mlx_ptr, maze.width * size, maze.height * size,)
    # put_block_pixel(maze.maze, mlx, mlx_ptr, win_ptr, size)
    mlx.mlx_hook(win_ptr, 33, 0, end, (mlx, mlx_ptr, win_ptr))
    mlx.mlx_loop_hook(mlx_ptr, render_handler, (mlx, mlx_ptr, win_ptr, img_ptr))
    # mlx.mlx_expose_hook(win_ptr, render_maze, (maze.maze, mlx, mlx_ptr, win_ptr, size))
    # mlx.mlx_loop_hook(mlx_ptr, loop_render, (maze.maze, mlx, mlx_ptr, win_ptr, size))
    # mlx.mlx_hook(win_ptr, 2, 0, key_hook, (maze.maze, mlx, mlx_ptr, win_ptr, size))
    mlx.mlx_loop(mlx_ptr)
    
#    print(f"{maze.dict_graph}")
