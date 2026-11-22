"""Graphical rendering of the A-Maze-ing project using the MLX library.

This module provides :class:`Render`, which opens an MLX window, draws the
maze (optionally animating its construction), highlights the entry, the exit
and the solution path, and handles keyboard interaction.

Drawing conventions used throughout the module:

* Each cell occupies a 20x20 pixel square, and neighbouring cells are
  spaced 15 pixels apart so that they share a 5-pixel wall.
* The wall bitmask of a node uses bit 1 for the north wall, 2 for the east
  wall, 4 for the south wall and 8 for the west wall.
* ``paint_block`` receives its position as ``(x, y)`` where ``x`` is the
  vertical (row) offset and ``y`` the horizontal (column) offset.
"""

from typing import Any, cast
import mlx
from mazegen import MazeGenerator
from mazegen.maze_utils import Node


class Render:
    """Draw a maze in an MLX window and handle user interaction.

    Attributes:
        colors (Render.Color): Current node of the circular color-scheme
            list; ``colors.color`` is a tuple of (background, wall, '42'
            logo) colors.
        maze_obj (MazeGenerator): The maze generator being displayed.
        show_path (bool): Whether the solution path is currently shown.
        mlx_obj (mlx.Mlx): The MLX library instance.
        mlx_ptr (Any): MLX connection pointer, set by :meth:`start`.
        win_ptr (Any): MLX window pointer, set by :meth:`start`.
        params (Any): Tuple ``(maze_obj, mlx_obj, mlx_ptr, win_ptr, width,
            height)`` shared with the drawing methods, set by :meth:`start`.
        animation (bool): Whether the generation is animated step by step.
    """

    def __init__(
        self, maze_obj: MazeGenerator, animation: bool = False
    ) -> None:
        """Initialize the renderer without opening any window.

        Args:
            maze_obj (MazeGenerator): The maze generator to display.
            animation (bool): If True, animate the maze construction.
                Defaults to False.
        """
        self.colors = self.select_color()
        self.maze_obj: MazeGenerator = maze_obj
        self.show_path: bool = False
        self.mlx_obj = mlx.Mlx()
        self.mlx_ptr = None
        self.win_ptr = None
        self.params: Any = ()
        self.animation = animation

    class Color:
        """Node of a circular linked list of color schemes.

        Attributes:
            color (tuple[int, int, int]): Colors in 0xAARRGGBB format, in
                the order (background, wall, '42' logo).
            next (Render.Color): The next color scheme in the cycle. It
                points to the node itself until linked.
        """

        def __init__(self, color: tuple[int, int, int]) -> None:
            """Create a color-scheme node linked to itself.

            Args:
                color (tuple[int, int, int]): Background, wall and logo
                    colors in 0xAARRGGBB format.
            """
            self.color = color
            self.next = self

    def select_color(self) -> Color:
        """Build the circular list of color schemes.

        Returns:
            Render.Color: The first of four color schemes, linked so that
            following ``next`` cycles through all of them and returns to
            the start.
        """
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
        """Switch to the next color scheme in the cycle."""
        self.colors = self.colors.next

    def start(self) -> None:
        """Open the MLX window and register events and the help text.

        Compute the window size from the maze dimensions, create the MLX
        connection and window (with 100 extra pixels at the bottom for the
        menu), store the shared ``params`` tuple, hook the window-close
        event and the key handler, and print the list of keyboard
        commands.
        """
        width: int = self.maze_obj.width * 10 + 5 * (self.maze_obj.width + 1)
        height = self.maze_obj.height * 10 + 5 * (self.maze_obj.height + 1)
        self.mlx_ptr = self.mlx_obj.mlx_init()
        self.win_ptr = self.mlx_obj.mlx_new_window(
            self.mlx_ptr, width, height + 100, "a-maze-ing"
        )
        self.params = (
            self.maze_obj,
            self.mlx_obj,
            self.mlx_ptr,
            self.win_ptr,
            width,
            height,
        )
        self.mlx_obj.mlx_hook(
            self.win_ptr, 33, 0, self.end_event, self.mlx_obj
        )
        self.mlx_obj.mlx_key_hook(self.win_ptr, self.gere_key, self.params)
        self.mlx_obj.mlx_string_put(
            self.mlx_ptr,
            self.win_ptr,
            0,
            height + 5,
            0xFFFFFFFF,
            "1. Regen new maze",
        )
        self.mlx_obj.mlx_string_put(
            self.mlx_ptr,
            self.win_ptr,
            0,
            height + 25,
            0xFFFFFFFF,
            "2. Show/Hide path",
        )
        self.mlx_obj.mlx_string_put(
            self.mlx_ptr,
            self.win_ptr,
            0,
            height + 45,
            0xFFFFFFFF,
            "3. Change color",
        )
        self.mlx_obj.mlx_string_put(
            self.mlx_ptr, self.win_ptr, 0, height + 65, 0xFFFFFFFF, "4. Quit"
        )

    def init_animation(self) -> None:
        """Generate and draw the maze, then enter the event loop.

        Consume the maze generator: draw the initial grid, and for each
        generation step either animate the two affected nodes (when
        ``animation`` is True) or simply keep generating. Without
        animation the finished maze is drawn at the end. Finally the
        entry and exit are marked, the maze is saved to its output file
        and the MLX event loop is started.
        """
        gen = self.maze_obj.generate_maze()
        next(gen)
        self.render_maze()
        self.mlx_obj.mlx_do_sync(self.mlx_ptr)
        while True:
            try:
                value = next(gen)
                if self.animation and len(value) == 2:
                    pair = cast("tuple[Node, Node]", value)
                    self.animate_wall(pair[0])
                    self.animate_wall(pair[1])
            except StopIteration:
                break
        if not self.animation:
            self.render_maze()
        self.put_entry_exit()
        self.maze_obj.save_file()
        self.loop()

    def loop(self) -> None:
        """Start the MLX event loop; block until it is exited."""
        self.mlx_obj.mlx_loop(self.mlx_ptr)

    def end(self) -> None:
        """Close the window and stop the MLX event loop."""
        print("Closing window")
        self.mlx_obj.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        self.mlx_obj.mlx_loop_exit(self.mlx_ptr)

    def end_event(self, mlx_obj: Any) -> None:
        """Handle the window-close event.

        Registered as the MLX hook for the window's close button.

        Args:
            mlx_obj (Any): The MLX instance passed back by the hook, used
                to destroy the window and leave the event loop.
        """
        print("Closing window")
        mlx_obj.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        mlx_obj.mlx_loop_exit(self.mlx_ptr)

    def paint_block(
        self,
        mlx: Any,
        mlx_ptr: Any,
        win_ptr: Any,
        color: int,
        size_x: int,
        size_y: int,
        x: int,
        y: int,
    ) -> None:
        """Fill a rectangle of pixels with a single color.

        Note that ``x`` and ``size_x`` refer to the vertical axis (rows)
        and ``y`` and ``size_y`` to the horizontal axis (columns).

        Args:
            mlx (Any): The MLX instance.
            mlx_ptr (Any): MLX connection pointer.
            win_ptr (Any): MLX window pointer.
            color (int): Fill color in 0xAARRGGBB format.
            size_x (int): Rectangle extent along the vertical axis, in
                pixels.
            size_y (int): Rectangle extent along the horizontal axis, in
                pixels.
            x (int): Vertical offset of the top-left corner, in pixels.
            y (int): Horizontal offset of the top-left corner, in pixels.
        """
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
        height: int,
    ) -> None:
        """Draw the whole maze: background, walls and '42' logo cells.

        Fill the background, then walk through every node and paint each
        of its walls according to the wall bitmask, plus a small square
        for the nodes belonging to the '42' logo.

        Args:
            maze (list[list[Any]]): Grid of nodes, indexed as
                ``maze[row][col]``.
            mlx (Any): The MLX instance.
            mlx_ptr (Any): MLX connection pointer.
            win_ptr (Any): MLX window pointer.
            width (int): Pixel extent of the background along the vertical
                axis (:meth:`render_maze` passes the maze pixel height).
            height (int): Pixel extent of the background along the
                horizontal axis (:meth:`render_maze` passes the maze pixel
                width).
        """
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
                        mlx,
                        mlx_ptr,
                        win_ptr,
                        wall_color,
                        20,
                        5,
                        pos_x,
                        pos_y + 20 - 5,
                    )
                if node.wall & 4 == 4:
                    self.paint_block(
                        mlx,
                        mlx_ptr,
                        win_ptr,
                        wall_color,
                        5,
                        20,
                        pos_x + 20 - 5,
                        pos_y + 0,
                    )
                if node.wall & 8 == 8:
                    self.paint_block(
                        mlx, mlx_ptr, win_ptr, wall_color, 20, 5, pos_x, pos_y
                    )
                if node.fix:
                    self.paint_block(
                        mlx,
                        mlx_ptr,
                        win_ptr,
                        ft_color,
                        10,
                        10,
                        pos_x + 5,
                        pos_y + 5,
                    )
                pos_y += 15
            pos_x += 15

    def animate_wall(self, node: Node) -> None:
        """Redraw a single node during the generation animation.

        Repaint each of the four walls of the node (in wall color when
        present, in background color when removed), the node interior
        (logo color or background), and the four corner squares, which are
        cleared only when none of the adjacent walls remains. The display
        is synchronized at the end.

        Args:
            node (Node): The node to redraw; its ``cords`` attribute is
                ``(row, column)``.
        """
        row, column = node.cords
        pos_x = row * 15
        pos_y = column * 15

        main_color = self.colors.color[0]
        wall_color = self.colors.color[1]
        ft_color = self.colors.color[2]
        if node.wall & 1 == 1:
            self.paint_block(
                self.mlx_obj,
                self.mlx_ptr,
                self.win_ptr,
                wall_color,
                5,
                20,
                pos_x,
                pos_y,
            )
        else:
            self.paint_block(
                self.mlx_obj,
                self.mlx_ptr,
                self.win_ptr,
                main_color,
                5,
                10,
                pos_x,
                pos_y + 5,
            )
        if node.wall & 2 == 2:
            self.paint_block(
                self.mlx_obj,
                self.mlx_ptr,
                self.win_ptr,
                wall_color,
                20,
                5,
                pos_x,
                pos_y + 20 - 5,
            )
        else:
            self.paint_block(
                self.mlx_obj,
                self.mlx_ptr,
                self.win_ptr,
                main_color,
                10,
                5,
                pos_x + 5,
                pos_y + 20 - 5,
            )

        if node.wall & 4 == 4:
            self.paint_block(
                self.mlx_obj,
                self.mlx_ptr,
                self.win_ptr,
                wall_color,
                5,
                20,
                pos_x + 20 - 5,
                pos_y + 0,
            )
        else:
            self.paint_block(
                self.mlx_obj,
                self.mlx_ptr,
                self.win_ptr,
                main_color,
                5,
                10,
                pos_x + 20 - 5,
                pos_y + 5,
            )
        if node.wall & 8 == 8:
            self.paint_block(
                self.mlx_obj,
                self.mlx_ptr,
                self.win_ptr,
                wall_color,
                20,
                5,
                pos_x,
                pos_y,
            )
        else:
            self.paint_block(
                self.mlx_obj,
                self.mlx_ptr,
                self.win_ptr,
                main_color,
                10,
                5,
                pos_x + 5,
                pos_y,
            )
        if node.fix:
            self.paint_block(
                self.mlx_obj,
                self.mlx_ptr,
                self.win_ptr,
                ft_color,
                10,
                10,
                pos_x + 5,
                pos_y + 5,
            )
        else:
            self.paint_block(
                self.mlx_obj,
                self.mlx_ptr,
                self.win_ptr,
                main_color,
                10,
                10,
                pos_x + 5,
                pos_y + 5,
            )

        def has_wall(r: int, c: int, bit: int) -> bool:
            """Tell whether a node has a given wall.

            Args:
                r (int): Row of the node.
                c (int): Column of the node.
                bit (int): Wall bit to test (1, 2, 4 or 8).

            Returns:
                bool: True if the wall is set, or if the position lies
                outside the maze (the border counts as a wall).
            """
            if 0 <= r < self.maze_obj.height and 0 <= c < self.maze_obj.width:
                return (self.maze_obj.maze[r][c].wall & bit) != 0
            return True

        if not (
            has_wall(row, column, 1)
            or has_wall(row, column, 8)
            or has_wall(row - 1, column, 8)
            or has_wall(row, column - 1, 1)
        ):
            self.paint_block(
                self.mlx_obj,
                self.mlx_ptr,
                self.win_ptr,
                main_color,
                5,
                5,
                pos_x,
                pos_y,
            )

        if not (
            has_wall(row, column, 1)
            or has_wall(row, column, 2)
            or has_wall(row - 1, column, 2)
            or has_wall(row, column + 1, 1)
        ):
            self.paint_block(
                self.mlx_obj,
                self.mlx_ptr,
                self.win_ptr,
                main_color,
                5,
                5,
                pos_x,
                pos_y + 15,
            )

        if not (
            has_wall(row, column, 4)
            or has_wall(row, column, 8)
            or has_wall(row + 1, column, 8)
            or has_wall(row, column - 1, 4)
        ):
            self.paint_block(
                self.mlx_obj,
                self.mlx_ptr,
                self.win_ptr,
                main_color,
                5,
                5,
                pos_x + 15,
                pos_y,
            )

        if not (
            has_wall(row, column, 4)
            or has_wall(row, column, 2)
            or has_wall(row + 1, column, 2)
            or has_wall(row, column + 1, 4)
        ):
            self.paint_block(
                self.mlx_obj,
                self.mlx_ptr,
                self.win_ptr,
                main_color,
                5,
                5,
                pos_x + 15,
                pos_y + 15,
            )

        self.mlx_obj.mlx_do_sync(self.mlx_ptr)

    def put_entry_exit(self) -> None:
        """Mark the maze entry and exit with colored squares.

        The entry is drawn in blue and the exit in yellow, each as a
        10x10 pixel square at the center of its cell. Coordinates are
        read from the stored ``params`` tuple.
        """
        maze, mlx, mlx_ptr, win_ptr, width, height = self.params
        entry_y, entry_x = maze.entry[1], maze.entry[0]
        exit_y, exit_x = maze.exit_maze[1], maze.exit_maze[0]

        entry_color = 0xFF0000FF
        exit_color = 0xFFCCAA09

        self.paint_block(
            mlx,
            mlx_ptr,
            win_ptr,
            entry_color,
            10,
            10,
            entry_y * 15 + 5,
            entry_x * 15 + 5,
        )
        self.paint_block(
            mlx,
            mlx_ptr,
            win_ptr,
            exit_color,
            10,
            10,
            exit_y * 15 + 5,
            exit_x * 15 + 5,
        )

    def render_path(self) -> None:
        """Draw the solution path over the maze.

        Paint a square on every node of ``maze.path`` and a connector
        block between each pair of consecutive nodes, then redraw the
        entry and exit markers on top. If no path has been generated, print
        a message and return without drawing.
        """
        maze, mlx, mlx_ptr, win_ptr, width, height = self.params
        path_color: int = 0xFF11A3FE

        x: int = maze.entry[0]
        y: int = maze.entry[1]

        if not maze.path:
            print("Path not generated")
            return

        for i in range(len(maze.path)):

            curr_y, curr_x = maze.path[i].cords
            self.paint_block(
                mlx,
                mlx_ptr,
                win_ptr,
                path_color,
                10,
                10,
                curr_y * 15 + 5,
                curr_x * 15 + 5,
            )

            if i < len(maze.path) - 1:

                next_y, next_x = maze.path[i + 1].cords

                if next_y < curr_y:
                    self.paint_block(
                        mlx,
                        mlx_ptr,
                        win_ptr,
                        path_color,
                        5,
                        10,
                        curr_y * 15,
                        curr_x * 15 + 5,
                    )
                    y -= 1
                if next_y > curr_y:
                    self.paint_block(
                        mlx,
                        mlx_ptr,
                        win_ptr,
                        path_color,
                        5,
                        10,
                        curr_y * 15 + 15,
                        curr_x * 15 + 5,
                    )
                    y += 1
                if next_x > curr_x:
                    self.paint_block(
                        mlx,
                        mlx_ptr,
                        win_ptr,
                        path_color,
                        10,
                        5,
                        curr_y * 15 + 5,
                        curr_x * 15 + 15,
                    )
                    x += 1
                if next_x < curr_x:
                    self.paint_block(
                        mlx,
                        mlx_ptr,
                        win_ptr,
                        path_color,
                        10,
                        5,
                        curr_y * 15 + 5,
                        curr_x * 15,
                    )
                    x -= 1

        self.put_entry_exit()

    def render_maze(self) -> None:
        """Draw the full maze and the entry and exit markers."""
        maze, mlx, mlx_ptr, win_ptr, width, height = self.params
        self.put_block_pixel(maze.maze, mlx, mlx_ptr, win_ptr, height, width)
        self.put_entry_exit()

    def gere_key(self, key: int, params: Any) -> None:
        """Handle a key press.

        Supported keys:

        * ``1`` (49): generate a new maze with a new seed.
        * ``2`` (50) or key code 16: show or hide the solution path.
        * ``3`` (51): switch to the next color scheme.
        * ``4`` (52): quit.

        Args:
            key (int): Key code received from MLX.
            params (Any): Tuple ``(maze_obj, mlx_obj, mlx_ptr, win_ptr,
                width, height)`` registered in :meth:`start`.
        """
        maze, mlx, mlx_ptr, win_ptr, width, height = params
        if key == 49:
            maze.new_seed()
            maze.maze = []
            self.show_path = False
            self.init_animation()

        elif key == 50 or key == 16:
            self.show_path = not self.show_path
            self.paint_block(
                mlx, mlx_ptr, win_ptr, 0x00000000, width, height, 0, 0
            )
            self.render_maze()
            if self.show_path:
                self.render_path()
        elif key == 51:
            self.next_color()
            self.render_maze()
            if self.show_path:
                self.render_path()
        elif key == 52:
            self.end()
