import pygame as pg
import pygame.freetype as ft

pg.init()

FONT_PATH = "assets/font/FREAKSOFNATUREMASSIVE.ttf"
FONT_SIZE = 120
LINE_GAP = 10

TEXT_LINES = [
    "Tetro",
    "mino",
    "Tetris"
]

COLORS = [
    (255, 165,   0),  # orange
    (255, 215,   0),  # yellow
    (255,   0,   0),  # red
    (160,  32, 240),  # purple
    (  0,   0, 255),  # blue
    (  0, 200,   0),  # green
]

font = ft.Font(FONT_PATH, FONT_SIZE)

# --- Measure total logo size ---
line_surfaces = []
max_width = 0
total_height = 0
color_index = 0

for line in TEXT_LINES:
    x = 0
    line_height = 0
    letter_surfaces = []

    for ch in line:
        surf, rect = font.render(ch, fgcolor=COLORS[color_index % len(COLORS)])
        color_index += 1
        letter_surfaces.append((surf, rect))
        x += rect.width
        line_height = max(line_height, rect.height)

    line_surfaces.append((letter_surfaces, line_height, x))
    max_width = max(max_width, x)
    total_height += line_height + LINE_GAP

total_height -= LINE_GAP  # remove last gap

# --- Create transparent surface ---
logo_surf = pg.Surface((max_width, total_height), pg.SRCALPHA)

# --- Blit letters ---
y = 0
for letter_surfaces, line_height, line_width in line_surfaces:
    x = (max_width - line_width) // 2  # center each line
    for surf, rect in letter_surfaces:
        logo_surf.blit(surf, (x, y))
        x += rect.width
    y += line_height + LINE_GAP

# --- Save PNG ---
pg.image.save(logo_surf, "assets/logo.png")

pg.quit()
