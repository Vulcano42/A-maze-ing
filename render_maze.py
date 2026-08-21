from typing import Any, Tuple
import mlx
import random

# BACKGROUND-COLOR
#1E2956 AZUL
#2E2058 BLUE-VIOLET
#2C1059 VIOLET
#781359 RED-VIOLET
# WALL-COLOR
#FC360E ORANGE
#FE7F14 YELLOW ORANGE
#FFFE21 YELLOW
#69B21B YELLOW GREEN
# 42-COLOR
#96C696 BLUE GREEN
#9DDB58 GREEN
#FF0109 RED
#C9501B RED-ORANGE

class Render:
    def __init__(self, maze_obj: Any) -> None:
        from a_maze_ing import MazeGenerator
        self.colors = self.select_color()
        self.maze_obj: MazeGenerator = maze_obj
        self.show_path: bool = False
        # self.mlx = mlx.Mlx()
        # self.mlx_ptr = self.mlx.mlx_init()
        # self.win_ptr = self.mlx_new_window()

    class Color:
        def __init__(self, color) -> None:
            self.color = color
            self.next = self
    # ARGB
    def select_color(self):
        c_1 = self.Color((0xFF1E2956, 0xFFFC360E, 0xFF96C696))
        c_2 = self.Color((0xFF2E2058, 0xFFFE7F14, 0xFF9DDB58))
        c_3 = self.Color((0xFF2C1059, 0xFFFFFE21, 0xFFFF0109))
        c_4 = self.Color((0xFF781359, 0xFF69B21B, 0xFFC9501B))
        c_1.next = c_2
        c_2.next = c_3
        c_3.next = c_4
        c_4.next = c_1
        return c_1

    def next_color(self):
        self.colors = self.colors.next

    def start(self):
        width: int = self.maze_obj.width * 10 + 5 * (self.maze_obj.height + 1)
        height = self.maze_obj.height * 10 + 5 * (self.maze_obj.height + 1)
        mlx_obj = mlx.Mlx()
        mlx_ptr = mlx_obj.mlx_init()
        win_ptr = mlx_obj.mlx_new_window(mlx_ptr, width, height, "a-maze-ing")
        params = (self.maze_obj, mlx_obj, mlx_ptr, win_ptr, width, height)
        mlx_obj.mlx_hook(win_ptr, 33, 0, self.end, (mlx_obj, mlx_ptr, win_ptr))
        mlx_obj.mlx_key_hook(win_ptr, self.gere_key, params)
        mlx_obj.mlx_expose_hook(win_ptr, self.render_maze, params)
        self.render_maze(params)
        mlx_obj.mlx_loop(mlx_ptr)

    def end(self, data):
        print("Encerrrando janela....")
        mlx, mlx_ptr, win_ptr = data
        mlx.mlx_destroy_window(mlx_ptr, win_ptr)
        mlx.mlx_loop_exit(mlx_ptr)

    def paint_block(self, mlx, mlx_ptr, win_ptr, color, size_x, size_y, x, y):
        for pos_x in range(size_x):
            for pos_y in range(size_y):
                mlx.mlx_pixel_put(mlx_ptr, win_ptr, y + pos_y, x + pos_x, color)


    def put_block_pixel(self, maze, mlx, mlx_ptr, win_ptr, width, height):
        pos_y = 0
        pos_x = 0
        contador = 0
        main_color = self.colors.color[0]  #101821 # Vermelho forte (Para ter certeza que está pintando)
        wall_color = self.colors.color[1]  #7D92AB # Verde forte
        ft_color = self.colors.color[2]
        self.paint_block(mlx, mlx_ptr, win_ptr, main_color, width, height, pos_x, pos_y)
        for line in maze:
            pos_y = 0
            for node in line:
                if node.wall & 1 == 1:
                    self.paint_block(mlx, mlx_ptr, win_ptr, wall_color, 5, 20, pos_x, pos_y)
                if node.wall & 2 == 2:
                    self.paint_block(mlx, mlx_ptr, win_ptr, wall_color, 20, 5, pos_x, pos_y + 20 - 5)
                if node.wall & 4 == 4:
                    self.paint_block(mlx, mlx_ptr, win_ptr, wall_color, 5, 20, pos_x + 20 - 5, pos_y + 0)
                if node.wall & 8 == 8:
                    self.paint_block(mlx, mlx_ptr, win_ptr, wall_color, 20, 5, pos_x, pos_y)
                if node.fix:
                    self.paint_block(mlx, mlx_ptr, win_ptr, ft_color, 10, 10, pos_x + 5, pos_y + 5)
                contador += 1
                pos_y += 15
                # print("y:", pos_y)
            pos_x += 15
            # print("x:", pos_x)
        # print("x:", pos_x, "y:", pos_y)
        print(contador)

    def put_entry_exit(self, params) -> None:

        maze, mlx, mlx_ptr, win_ptr, width, height = params
        entry_y, entry_x = maze.entry[1], maze.entry[0]
        exit_y, exit_x = maze.exit_maze[1], maze.exit_maze[0]

        entry_color = 0xFF0000FF
        exit_color = 0xFFFF0109

        self.paint_block(
            mlx, mlx_ptr, win_ptr, entry_color,
            10, 10, entry_y * 15 + 5, entry_x * 15 + 5
        )
        self.paint_block(
            mlx, mlx_ptr, win_ptr, exit_color,
            10, 10, exit_y * 15 + 5, exit_x * 15 + 5
        )


    def render_path(self, params) -> None:

        maze, mlx, mlx_ptr, win_ptr, width, height = params
        path_color: int = 0xFF11A3FE

        x: int = maze.entry[0]
        y: int = maze.entry[1]

        if not maze.path:
            print("Path not generated")
            return
        

        for i in range(len(maze.path)):

            curr_y, curr_x = maze.path[i].cords
            self.paint_block(
                mlx, mlx_ptr, win_ptr, path_color,
                10, 10, curr_y * 15 + 5, curr_x * 15 + 5
            )

            if i < len(maze.path) - 1:

                next_y, next_x = maze.path[i + 1].cords

                if next_y < curr_y:
                    self.paint_block(
                        mlx, mlx_ptr, win_ptr, path_color,
                        5, 10, curr_y * 15, curr_x * 15 + 5
                    )
                    y -= 1
                if next_y > curr_y:
                    self.paint_block(
                        mlx, mlx_ptr, win_ptr, path_color,
                        5, 10, curr_y * 15 + 15, curr_x * 15 + 5
                    )
                    y += 1
                if next_x > curr_x:
                    self.paint_block(
                        mlx, mlx_ptr, win_ptr, path_color,
                        10, 5, curr_y * 15 + 5, curr_x * 15 + 15
                    )
                    x += 1
                if next_x < curr_x:
                    self.paint_block(
                        mlx, mlx_ptr, win_ptr, path_color,
                        10, 5, curr_y * 15 + 5, curr_x * 15
                    )
                    x -= 1

        self.put_entry_exit(params)


    def render_maze(self, params):

        maze, mlx, mlx_ptr, win_ptr, width, height = params
        print("Renderizando Labirinto")
        self.put_block_pixel(maze.maze, mlx, mlx_ptr, win_ptr, width, height)
        x, y = maze.entry[0], maze.entry[1]
        self.put_entry_exit(params)


    def gere_key(self, key, params):
        print(f"Got key {key}: ", end="")
        maze, mlx, mlx_ptr, win_ptr, width, height = params

        if key == 113:  # 'q'
               
            random.seed(None)
            new_seed = random.randint(0, 100000)
            maze.seed = new_seed
            maze.dict_graph["seed"] = str(maze.seed)
            maze.maze = []
            maze.genereate_maze()
            maze.save_file()
            mlx.mlx_clear_window(mlx_ptr, win_ptr)
            self.next_color()
            self.render_maze(params)
            self.show_path = False
#            for line in maze.maze:
#                for node in line:
#                    node.wall = 15
#                    node.parent = node
#                    node.rank = 0
#            print("maze.seed: ", maze.seed)
#            new_seed = random.randint(0, 10000)
#            print("New seed:", new_seed)
#            random.seed(new_seed)
#            maze.seed = new_seed
#            print("maze.seed: ", maze.seed)
#            maze.dict_graph["seed"] = str(new_seed)
#            maze.genereate_maze()
#            maze.save_file()
#            mlx.mlx_clear_window(mlx_ptr, win_ptr)
#            self.next_color()
#            self.render_maze(params)
#            self.show_path = False

        # elif key == 119:  # 'w'
        #     xvar.mlx.mlx_do_key_autorepeaton(xvar.mlx_ptr)
        #     print("key repeat on")
        #     return 0
        # elif key == 101:  # 'e'
        #     draw_colormap(xvar)
        #     print("colormap")
        #     return 0
        # elif key == 114:  # 'r'
        #     xvar.mlx.mlx_mouse_hide(xvar.mlx_ptr)
        #     print("mouse hide")
        #     return 0
        # elif key == 116:  # 't'
        #     xvar.mlx.mlx_mouse_show(xvar.mlx_ptr)
        #     print("mouse show")
        #     return 0

        elif key == 121 or key == 16:  # 'y'
            self.show_path = not self.show_path
            mlx.mlx_clear_window(mlx_ptr, win_ptr)
            self.render_maze(params)
            if self.show_path:
                self.render_path(params)
            return 0
        # elif key == 117:  # 'u'
        #     ret, x, y = xvar.mlx.mlx_mouse_get_pos(xvar.win_1)
        #     print(f"current mouse pos is {x} x {y}")
        #     return 0
        # elif key == 105:  # 'i'
        #     xvar.mlx.mlx_sync(xvar.mlx_ptr, Mlx.SYNC_IMAGE_WRITABLE, xvar.img_2.img)
        #     # fill image in white
        #     for offset in range(0, xvar.img_2.sl * 100, 4):
        #         xvar.img_2.data[offset:offset+4] = (0xFFFFFFFF).to_bytes(4, 'little')
        #
        #     xvar.mlx.mlx_put_image_to_window(xvar.mlx_ptr, xvar.win_1, xvar.img_2.img, 50, 50)
        #
        #     # update in red
        #     for offset in range(0, xvar.img_2.sl * 100, 4):
        #         xvar.img_2.data[offset:offset+4] = (0xFFFF0000).to_bytes(4, 'little')
        #
        #     xvar.mlx.mlx_put_image_to_window(xvar.mlx_ptr, xvar.win_1, xvar.img_2.img, 250, 250)
        #     print("update image without sync - most likely 2 red squares")
        #     return 0

        else:
            key
            pass