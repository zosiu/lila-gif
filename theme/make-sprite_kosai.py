import xml.etree.ElementTree as ET
import chess.svg
from pathlib import Path

# from chess.svg import SQUARE_SIZE


COLORS = [
    # "#f0d9b5", # light square
    # "#b58863", # dark square
    # "#ced26b", # highlighted light square
    # "#aaa23b", # highlighted dark square
    "#DEE3E6", # light square
    "#8CA2AD", # dark square
    "#C3D899", # highlighted light square
    "#92B277", # highlighted dark square
    "#262421", # dark background
    "#bababa", # text color
    "#bf811d", # title color
    "#b72fc6", # bot color
    "#706f6e", # 50% text color on dark background
]

SQUARE_SIZE = 81
COLOR_WIDTH = SQUARE_SIZE * 2 // 3

def make_sprite(f):
    svg = ET.Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg",
        "version": "1.1",
        "xmlns:xlink": "http://www.w3.org/1999/xlink",
        "viewBox": f"0 0 {SQUARE_SIZE * 8} {SQUARE_SIZE * 8}",
    })

    defs = ET.SubElement(svg, "defs")
    for color_name, color_key in {'white': 'w', 'black': 'b'}.items():
        for piece_name, piece_key in {'pawn': 'P', 'knight': 'N', 'bishop': 'B', 'rook': 'R', 'queen': 'Q', 'king': 'K'}.items():
            piece_svg = ET.Element('g', {'id': f'{color_name}-{piece_name}'})
            piece_template = ET.fromstring(Path(f'kosal/{color_key}{piece_key}.svg').read_text())
            piece_svg.extend(piece_template)
            defs.append(piece_svg)

    # defs.append(ET.fromstring(chess.svg.CHECK_GRADIENT))
    defs.append(ET.fromstring(Path(f'kosal/check_gradient.svg').read_text()))

    for x, color in enumerate(COLORS[4:]):
        ET.SubElement(svg, "rect", {
            "x": str(SQUARE_SIZE * 4 + COLOR_WIDTH * x),
            "y": "0",
            "width": str(COLOR_WIDTH),
            "height": str(SQUARE_SIZE),
            "stroke": "none",
            "fill": color,
        })

    for x in range(8):
        ET.SubElement(svg, "rect", {
            "x": str(SQUARE_SIZE * x),
            "y": str(SQUARE_SIZE if x >= 4 else 0),
            "width": str(SQUARE_SIZE),
            "height": str(SQUARE_SIZE * (7 if x >= 4 else 8)),
            "stroke": "none",
            "fill": COLORS[x % 4],
        })

        for y in range(1, 8):
            piece_type = min(y, 6)
            color = "white" if x >= 4 else "black"

            if y == 7:
                ET.SubElement(svg, "rect", {
                    "x": str(SQUARE_SIZE * x),
                    "y": str(SQUARE_SIZE * y),
                    "width": str(SQUARE_SIZE),
                    "height": str(SQUARE_SIZE),
                    "fill": "url(#check_gradient)",
                })

            ET.SubElement(svg, "use", {
                "xlink:href": f"#{color}-{chess.PIECE_NAMES[piece_type]}",
                "transform": f"translate({SQUARE_SIZE * x}, {SQUARE_SIZE * y})",
            })

    f.write(ET.tostring(svg))


if __name__ == "__main__":
    make_sprite(open("sprite_blue_kosal.svg", "wb"))
