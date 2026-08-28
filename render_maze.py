from typing import Any
import mlx
from mazegen import MazeGenerator


class Render:
    def __init__(self, maze_obj: Any) -> None:
        self.colors = self.select_color()
        self.maze_obj: MazeGenerator = maze_obj
        self.show_path: bool = False
        self.mlx_obj = mlx.Mlx()
        self.mlx_ptr = None
        self.win_ptr = None
        self.params_r = ()
    class Color:
        def __init__(self, color: tuple[int, int, int]) -> None:
            self.color = color
            self.next = self

    def select_color(self) -> Color:
        c_1 = self.Color((0xFF1E2956, 0xFFFC360E, 0xFF96C696))
        c_2 = self.Color((0xFF2E2058, 0xFFFE7F14, 0xFF9DDB58))
        c_3 = self.Color((0xFF2C1059, 0xFFFFFE21, 0xFFFF0109))
        c_4 = self.Color((0xFF781359, 0xFF69B21B, 0xFFC9501B))
        c_1.next = c_2
        c_2.next = c_3
        c_3.next = c_4
        c_4.next = c_1
        return c_1

    def next_color(self) -> None:
        self.colors = self.colors.next

    def start(self) -> None:
        width: int = self.maze_obj.width * 10 + 5 * (self.maze_obj.width + 1)
        height = self.maze_obj.height * 10 + 5 * (self.maze_obj.height + 1)
        self.mlx_ptr = self.mlx_obj.mlx_init()
        self.win_ptr = self.mlx_obj.mlx_new_window(
            self.mlx_ptr, width, height + 100, "a-maze-ing"
        )
        params = (self.maze_obj, self.mlx_obj, self.mlx_ptr, self.win_ptr, width, height)
        self.params_r = params
        self.mlx_obj.mlx_hook(self.win_ptr, 33, 0, self.end, (self.mlx_obj, self.mlx_ptr, self.win_ptr))
        self.mlx_obj.mlx_key_hook(self.win_ptr, self.gere_key, params)
        # self.render_maze(params)
        # self.mlx_obj.mlx_expose_hook(self.win_ptr, self.render_maze, params)
        self.mlx_obj.mlx_string_put(
            self.mlx_ptr, self.win_ptr, 0, height + 5, 0xFFFFFFFF,
            "1. Regen new maze"
            )
        self.mlx_obj.mlx_string_put(
            self.mlx_ptr, self.win_ptr, 0, height + 25, 0xFFFFFFFF,
            "2. Show/Hide path"
            )
        self.mlx_obj.mlx_string_put(
            self.mlx_ptr, self.win_ptr, 0, height + 45, 0xFFFFFFFF,
            "3. Change color"
            )
        self.mlx_obj.mlx_string_put(
            self.mlx_ptr, self.win_ptr, 0, height + 65, 0xFFFFFFFF,
            "4. Quit"
            )

        # mlx_obj.mlx_loop(self.mlx_ptr)
    def init_animation(self):
        # if self.maze_obj.animation:

        gen = self.maze_obj.generate_maze()
        next(gen)
        self.render_maze(self.params_r)
        self.mlx_obj.mlx_do_sync(self.mlx_ptr)
        # self.start()
        while True:
            try:
                value = next(gen)
                print(value)
                if value == -1:
                    break
                if self.maze_obj.animation:
                    self.animate_wall(value[0])
                    self.animate_wall(value[1])
                # self.loop()
                print("main")
            except StopIteration:
                break
        if not self.maze_obj.animation:
            self.render_maze(self.params_r)
        self.put_entry_exit(self.params_r)
        self.maze_obj.save_file()
        self.loop()
        # else:
        #     print("teste")
        #     # breakpoint()
        #     test = self.maze_obj.generate_maze()
        #     next(test)
        #     print(self.maze_obj.maze)
        #     for line in self.maze_obj.maze:
        #         for node in line:
        #             print("amogus")
        #             print(node.wall, end=" ")
        #         print()
        #     self.render_maze(self.params_r)
        #     self.loop()



    def loop(self):
        self.mlx_obj.mlx_loop(self.mlx_ptr)

    def end(self, data: Any) -> None:
        print("Encerrrando janela....")
        mlx, mlx_ptr, win_ptr = data
        mlx.mlx_destroy_window(mlx_ptr, win_ptr)
        mlx.mlx_loop_exit(mlx_ptr)

    def paint_block(
        self,
        mlx: Any,
        mlx_ptr: Any,
        win_ptr: Any,
        color: int,
        size_x: int,
        size_y: int,
        x: int,
        y: int
    ) -> None:
        for p_x in range(size_x):
            for p_y in range(size_y):
                mlx.mlx_pixel_put(mlx_ptr, win_ptr, y + p_y, x + p_x, color)

    def put_block_pixel(
        self,
        maze: list[list[Any]],
        mlx: Any,
        mlx_ptr: Any,
        win_ptr: Any,
        width: int,
        height: int
    ) -> None:
        # for linha in maze:
        #     for no in linha:
        #         print(no.wall, end=" ")
        #     print()

        pos_y = 0
        pos_x = 0
        main_color = self.colors.color[0]
        wall_color = self.colors.color[1]
        ft_color = self.colors.color[2]
        self.paint_block(
            mlx, mlx_ptr, win_ptr, main_color, width, height, pos_x, pos_y
        )
        for line in maze:
            pos_y = 0
            for node in line:
                if node.wall & 1 == 1:
                    self.paint_block(
                        mlx, mlx_ptr, win_ptr, wall_color, 5, 20, pos_x, pos_y
                    )
                if node.wall & 2 == 2:
                    self.paint_block(
                        mlx, mlx_ptr, win_ptr, wall_color,
                        20, 5, pos_x, pos_y + 20 - 5
                    )
                if node.wall & 4 == 4:
                    self.paint_block(
                        mlx, mlx_ptr, win_ptr, wall_color,
                        5, 20, pos_x + 20 - 5, pos_y + 0
                    )
                if node.wall & 8 == 8:
                    self.paint_block(
                        mlx, mlx_ptr, win_ptr, wall_color,
                        20, 5, pos_x, pos_y
                    )
                if node.fix:
                    self.paint_block(
                        mlx, mlx_ptr, win_ptr, ft_color,
                        10, 10, pos_x + 5, pos_y + 5
                    )
                pos_y += 15
            pos_x += 15

    def animate_wall(self, node):
        # mlx, mlx_ptr, win_ptr, main_color, width, height = self.params_r
        # pos_x, pos_y = node.cords[0] * 15, node.cords[1] * 15
        row, column = node.cords

        pos_x = row * 15
        pos_y = column * 15

        print("animacadiafj")
        main_color = self.colors.color[0]
        wall_color = self.colors.color[1]
        ft_color = self.colors.color[2]
        if node.wall & 1 == 1:
            self.paint_block(
                self.mlx_obj, self.mlx_ptr, self.win_ptr, wall_color, 5, 20, pos_x, pos_y
            )
        else:
            self.paint_block(
                self.mlx_obj, self.mlx_ptr, self.win_ptr, main_color, 5, 10, pos_x, pos_y + 5
            )
        if node.wall & 2 == 2:
            self.paint_block(
                self.mlx_obj, self.mlx_ptr, self.win_ptr, wall_color,
                20, 5, pos_x, pos_y + 20 - 5
            )
        else:
            self.paint_block(
                self.mlx_obj, self.mlx_ptr, self.win_ptr, main_color,
                10, 5, pos_x + 5, pos_y + 20 - 5
            )

        if node.wall & 4 == 4:
            self.paint_block(
                self.mlx_obj, self.mlx_ptr, self.win_ptr, wall_color,
                5, 20, pos_x + 20 - 5, pos_y + 0
            )
        else:
            self.paint_block(
                self.mlx_obj, self.mlx_ptr, self.win_ptr, main_color,
                5, 10, pos_x + 20 - 5, pos_y + 5
            )
        if node.wall & 8 == 8:
            self.paint_block(
                self.mlx_obj, self.mlx_ptr, self.win_ptr, wall_color,
                20, 5, pos_x, pos_y
            )
        else:
            self.paint_block(
                self.mlx_obj, self.mlx_ptr, self.win_ptr, main_color,
                10, 5, pos_x + 5, pos_y
            )
        if node.fix:
            self.paint_block(
                self.mlx_obj, self.mlx_ptr, self.win_ptr, ft_color,
                10, 10, pos_x + 5, pos_y + 5
            )
        else:
            self.paint_block(
                self.mlx_obj, self.mlx_ptr, self.win_ptr, main_color,
                10, 10, pos_x + 5, pos_y + 5
            )
        # def has_wall(r: int, c: int, bit: int) -> bool:
        #     if 0 <= r < maze.height and 0 <= c < maze.width:
        #         return (maze.maze[r][c].wall & bit) != 0
        #     return True

        def has_wall(r: int, c: int, bit: int) -> bool:
            if 0 <= r < self.maze_obj.height and 0 <= c < self.maze_obj.width:
                return (self.maze_obj.maze[r][c].wall & bit) != 0
            return True

        # Quina Superior-Esquerda
        if not (has_wall(row, column, 1) or has_wall(row, column, 8) or 
                has_wall(row-1, column, 8) or has_wall(row, column-1, 1)):
            self.paint_block(self.mlx_obj, self.mlx_ptr, self.win_ptr, main_color, 5, 5, pos_x, pos_y)

        # Quina Superior-Direita
        if not (has_wall(row, column, 1) or has_wall(row, column, 2) or 
                has_wall(row-1, column, 2) or has_wall(row, column+1, 1)):
            self.paint_block(self.mlx_obj, self.mlx_ptr, self.win_ptr, main_color, 5, 5, pos_x, pos_y + 15)

        # Quina Inferior-Esquerda
        if not (has_wall(row, column, 4) or has_wall(row, column, 8) or 
                has_wall(row+1, column, 8) or has_wall(row, column-1, 4)):
            self.paint_block(self.mlx_obj, self.mlx_ptr, self.win_ptr, main_color, 5, 5, pos_x + 15, pos_y)

        # Quina Inferior-Direita
        if not (has_wall(row, column, 4) or has_wall(row, column, 2) or 
                has_wall(row+1, column, 2) or has_wall(row, column+1, 4)):
            self.paint_block(self.mlx_obj, self.mlx_ptr, self.win_ptr, main_color, 5, 5, pos_x + 15, pos_y + 15)

        self.mlx_obj.mlx_do_sync(self.mlx_ptr)

    # def animation(self, nodes):



    def put_entry_exit(self, params: Any) -> None:

        maze, mlx, mlx_ptr, win_ptr, width, height = params
        entry_y, entry_x = maze.entry[1], maze.entry[0]
        exit_y, exit_x = maze.exit_maze[1], maze.exit_maze[0]

        entry_color = 0xFF0000FF
        exit_color = 0xFFCCAA09

        self.paint_block(
            mlx, mlx_ptr, win_ptr, entry_color,
            10, 10, entry_y * 15 + 5, entry_x * 15 + 5
        )
        self.paint_block(
            mlx, mlx_ptr, win_ptr, exit_color,
            10, 10, exit_y * 15 + 5, exit_x * 15 + 5
        )

    def render_path(self, params: Any) -> None:

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

    def render_maze(self, params: Any) -> None:
        print("oi")
        maze, mlx, mlx_ptr, win_ptr, width, height = params
        # mlx.mlx_do_sync(mlx_ptr)
        # for linha in maze.maze:
        #     for no in linha:
        #         print(no.wall, end=" ")
        #     print()
        self.put_block_pixel(maze.maze, mlx, mlx_ptr, win_ptr, height, width)
        self.put_entry_exit(params)

    def gere_key(self, key: int, params: Any) -> None:
        maze, mlx, mlx_ptr, win_ptr, width, height = params
        print(key)
        if key == 49:  # '1'
            maze.new_seed()
            maze.maze = []
            self.init_animation()
            # maze.save_file()
            self.paint_block(
                mlx, mlx_ptr, win_ptr, 0x00000000, width, height, 0, 0
            )
            # self.render_maze(params)
            self.show_path = False

        elif key == 50 or key == 16:  # '2'
            self.show_path = not self.show_path
            self.paint_block(
                mlx, mlx_ptr, win_ptr, 0x00000000, width, height, 0, 0
            )
            self.render_maze(params)
            if self.show_path:
                self.render_path(params)
            return
        elif key == 51:  # '3'
            self.next_color()
            self.render_maze(params)
            if self.show_path:
                self.render_path(params)
        elif key == 52:  # '4'
            self.end((mlx, mlx_ptr, win_ptr))
