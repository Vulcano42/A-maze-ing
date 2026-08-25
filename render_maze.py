from typing import Any
import mlx
import random


class Render:
    def __init__(self, maze_obj: Any) -> None:
        from a_maze_ing import MazeGenerator
        self.colors = self.select_color()
        self.maze_obj: MazeGenerator = maze_obj
        self.show_path: bool = False

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
        mlx_obj = mlx.Mlx()
        mlx_ptr = mlx_obj.mlx_init()
        win_ptr = mlx_obj.mlx_new_window(
            mlx_ptr, width, height + 100, "a-maze-ing"
        )
        params = (self.maze_obj, mlx_obj, mlx_ptr, win_ptr, width, height)
        mlx_obj.mlx_hook(win_ptr, 33, 0, self.end, (mlx_obj, mlx_ptr, win_ptr))
        mlx_obj.mlx_key_hook(win_ptr, self.gere_key, params)
        mlx_obj.mlx_expose_hook(win_ptr, self.render_maze, params)
        self.render_maze(params)
        mlx_obj.mlx_string_put(
            mlx_ptr, win_ptr, 0, height + 5, 0xFFFFFFFF,
            "1. Re-generate a new maze"
            )
        mlx_obj.mlx_string_put(
            mlx_ptr, win_ptr, 0, height + 25, 0xFFFFFFFF,
            "2. Show/Hide path"
            )
        mlx_obj.mlx_string_put(
            mlx_ptr, win_ptr, 0, height + 45, 0xFFFFFFFF,
            "3. Change color"
            )
        mlx_obj.mlx_string_put(
            mlx_ptr, win_ptr, 0, height + 65, 0xFFFFFFFF,
            "4. Quit"
            )

        mlx_obj.mlx_loop(mlx_ptr)

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

    def put_entry_exit(self, params: Any) -> None:

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

        maze, mlx, mlx_ptr, win_ptr, width, height = params
        self.put_block_pixel(maze.maze, mlx, mlx_ptr, win_ptr, height, width)
        self.put_entry_exit(params)

    def gere_key(self, key: int, params: Any) -> None:
        maze, mlx, mlx_ptr, win_ptr, width, height = params
        print(key)
        if key == 49:  # '1'
            random.seed(None)
            new_seed = random.randint(0, 100000)
            maze.seed = new_seed
            maze.maze = []
            maze.genereate_maze()
            maze.save_file()
            self.paint_block(
                mlx, mlx_ptr, win_ptr, 0x00000000, width, height, 0, 0
            )
            self.render_maze(params)
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
