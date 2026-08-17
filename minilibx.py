import os
from PIL import Image, ImageDraw

FILE = "maze.txt"
OUT_PNG = "maze.png"

# bit0=N, bit1=E, bit2=S, bit3=W (LSB->MSB)
def walls_from_nibble(n: int):
    north = (n >> 0) & 1
    east  = (n >> 1) & 1
    south = (n >> 2) & 1
    west  = (n >> 3) & 1
    return north == 1, east == 1, south == 1, west == 1

def parse_xy(s: str):
    a, b = s.split(",")
    return int(a), int(b)

def parse_maze(path: str):
    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    hex_rows = []
    i = 0

    while i < len(lines):
        s = lines[i]
        if not s:
            i += 1
            continue
        if "," in s:
            break
        if all(c in "0123456789abcdef" for c in s):
            hex_rows.append(s.lower())
            i += 1
            continue
        i += 1

    while i < len(lines) and lines[i] == "":
        i += 1
    entry = parse_xy(lines[i]); i += 1

    while i < len(lines) and lines[i] == "":
        i += 1
    exit_ = parse_xy(lines[i]); i += 1

    while i < len(lines) and lines[i] == "":
        i += 1
    route = lines[i] if i < len(lines) else ""

    return hex_rows, entry, exit_, route

def route_to_points(start_xy, route, rows, cols):
    x, y = start_xy
    pts = [(x, y)]
    move = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0)}
    for ch in route.strip():
        ch = ch.upper()
        if ch not in move:
            continue
        dx, dy = move[ch]
        nx, ny = x + dx, y + dy
        if 0 <= nx < cols and 0 <= ny < rows:
            x, y = nx, ny
            pts.append((x, y))
    return pts

def render_png(hex_rows, entry, exit_, route, out_png=OUT_PNG):
    rows = len(hex_rows)
    cols = len(hex_rows[0])

    cell = 18
    pad = 14
    wall_w = 4

    W = pad * 2 + cols * cell
    H = pad * 2 + rows * cell


    BG = (255, 255, 255)
    CLOSED_FILL = (255, 205, 120)
    WALL = (20, 20, 20)
    PATH = (30, 170, 90)
    ENTRY = (50, 120, 255)
    EXIT = (230, 60, 60)

    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    def cell_rect(x, y):
        x0 = pad + x * cell
        y0 = pad + y * cell
        x1 = x0 + cell
        y1 = y0 + cell
        return x0, y0, x1, y1

    def cell_center(x, y):
        x0, y0, x1, y1 = cell_rect(x, y)
        return (x0 + x1) // 2, (y0 + y1) // 2

    for y in range(rows):
        row = hex_rows[y]
        for x in range(cols):
            nib = int(row[x], 16)
            if nib == 15:
                x0, y0, x1, y1 = cell_rect(x, y)
                draw.rectangle([x0, y0, x1, y1], fill=CLOSED_FILL)

    for y in range(rows):
        row = hex_rows[y]
        for x in range(cols):
            nib = int(row[x], 16)
            north, east, south, west = walls_from_nibble(nib)
            x0, y0, x1, y1 = cell_rect(x, y)

            if north:
                draw.rectangle([x0, y0, x1, y0 + wall_w], fill=WALL)

            if west:
                draw.rectangle([x0, y0, x0 + wall_w, y1], fill=WALL)

            if x == cols - 1 and east:
                draw.rectangle([x1 - wall_w, y0, x1, y1], fill=WALL)

            if y == rows - 1 and south:
                draw.rectangle([x0, y1 - wall_w, x1, y1], fill=WALL)

    ex_cx, ex_cy = cell_center(*entry)
    out_cx, out_cy = cell_center(*exit_)

    r = max(6, cell // 3)
    draw.ellipse([ex_cx - r, ex_cy - r, ex_cx + r, ex_cy + r], fill=ENTRY, outline=ENTRY)
    draw.ellipse([out_cx - r, out_cy - r, out_cx + r, out_cy + r], fill=EXIT, outline=EXIT)

    pts = route_to_points(entry, route, rows, cols)
    if len(pts) >= 2:
        path_xy = [cell_center(px, py) for (px, py) in pts]
        draw.line(path_xy, fill=PATH, width=max(3, cell // 5), joint="curve")

    img.save(out_png, "PNG")
    print(f"Imagem gerada: {out_png} ({W}x{H})")

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    maze_path = os.path.join(here, FILE)

    hex_rows, entry, exit_, route = parse_maze(maze_path)
    render_png(hex_rows, entry, exit_, route, OUT_PNG)

if __name__ == "__main__":
    main()

