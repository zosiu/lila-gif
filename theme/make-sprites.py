import sys
import xml.etree.ElementTree as ET
import chess.svg
from pathlib import Path

LILA_DIR = sys.argv[1]

COLORS = {
    'brown': [
        "#f0d9b5", # light square
        "#b58863", # dark square
        "#ced26b", # highlighted light square
        "#aaa23b", # highlighted dark square
        "#262421", # dark background
        "#bababa", # text color
        "#bf811d", # title color
        "#b72fc6", # bot color
        "#706f6e", # 50% text color on dark background
    ],
    'blue': [
        "#dee3e6", # light square
        "#8ca2ad", # dark square
        "#c3d899", # highlighted light square
        "#92b277", # highlighted dark square
        "#262421", # dark background
        "#bababa", # text color
        "#bf811d", # title color
        "#b72fc6", # bot color
        "#706f6e", # 50% text color on dark background
    ]
}

def make_sprite(board_colors, piece_set, square_size):
    color_width = square_size * 2 // 3

    svg = ET.Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg",
        "version": "1.1",
        "xmlns:xlink": "http://www.w3.org/1999/xlink",
        "viewBox": f"0 0 {square_size * 8} {square_size * 8}",
    })

    defs = ET.SubElement(svg, "defs")
    for color_name, color_key in {'white': 'w', 'black': 'b'}.items():
        for piece_name, piece_key in {'pawn': 'P', 'knight': 'N', 'bishop': 'B', 'rook': 'R', 'queen': 'Q', 'king': 'K'}.items():
            piece_svg = ET.Element('g', {'id': f'{color_name}-{piece_name}'})
            piece_template = ET.fromstring(Path(f'{LILA_DIR}/public/piece/{piece_set}/{color_key}{piece_key}.svg').read_text())
            piece_svg.extend(piece_template)
            defs.append(piece_svg)

    defs.append(ET.fromstring(chess.svg.CHECK_GRADIENT))

    for x, color in enumerate(COLORS[board_color][4:]):
        ET.SubElement(svg, "rect", {
            "x": str(square_size * 4 + color_width * x),
            "y": "0",
            "width": str(color_width),
            "height": str(square_size),
            "stroke": "none",
            "fill": color,
        })

    for x in range(8):
        ET.SubElement(svg, "rect", {
            "x": str(square_size * x),
            "y": str(square_size if x >= 4 else 0),
            "width": str(square_size),
            "height": str(square_size * (7 if x >= 4 else 8)),
            "stroke": "none",
            "fill": COLORS[board_color][x % 4],
        })

        for y in range(1, 8):
            piece_type = min(y, 6)
            color = "white" if x >= 4 else "black"

            if y == 7:
                ET.SubElement(svg, "rect", {
                    "x": str(square_size * x),
                    "y": str(square_size * y),
                    "width": str(square_size),
                    "height": str(square_size),
                    "fill": "url(#check_gradient)",
                })

            ET.SubElement(svg, "use", {
                "xlink:href": f"#{color}-{chess.PIECE_NAMES[piece_type]}",
                "transform": f"translate({square_size * x}, {square_size * y})",
            })

    open(f'sprites/{piece_set}_{board_colors}.svg', "wb").write(ET.tostring(svg))

if __name__ == "__main__":
    PIECE_SET_SIZES = {
        # 'reillycraig': 0, # ?
        # 'riohacha': 0, # ?
        # 'california': 0, # ?
        'alpha': 2048,
        'cardinal': 50,
        'cburnett': 45,
        'chess7': 68,
        'chessnut': 800,
        'companion': 64,
        'dubrovny': 50,
        'fantasy': 900, # ids needed change
        'fresca': 50,
        'gioco': 50,
        'governor': 50,
        'horsey': 400,
        'icpieces': 368,
        'kosal': 81, # ids needed change
        'leipzig': 51,
        'letter': 300,
        'libra': 50,
        'maestro': 50,
        'merida': 50,
        'pirouetti': 3810,
        'pixel': 16,
        'shapes': 200,
        'spatial': 200, # ids needed change
        'staunty': 50,
        'tatiana': 50
    }

    for board_color in COLORS:
        for piece_set, square_size in PIECE_SET_SIZES.items():
            make_sprite(board_color, piece_set, square_size)
