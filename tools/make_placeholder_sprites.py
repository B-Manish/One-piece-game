"""Generates placeholder pixel-art for the player and the test world's tileset.

Run with: python tools/make_placeholder_sprites.py

Player sheet layout is read from assets/sprites/player/sheet_config.json so it
matches scripts/player/sprite_frames_builder.gd. Drop in your own Aseprite
export later by keeping the same frame_width/frame_height/columns/directions
in that config (or editing it to match your sheet) and re-running the builder
script in Godot -- no GDScript changes needed.
"""

import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
PLAYER_DIR = ROOT / "assets" / "sprites" / "player"
TILES_DIR = ROOT / "assets" / "tiles"

# Direction -> base body color, so frames are distinguishable at a glance.
DIRECTION_COLORS = {
    "down": (64, 140, 220),
    "left": (220, 150, 60),
    "right": (60, 180, 100),
    "up": (190, 70, 150),
}

TILE_SIZE = 16


def make_player_sheet(config: dict) -> None:
    fw, fh = config["frame_width"], config["frame_height"]
    columns = config["columns"]
    directions = config["directions"]
    rows = len(directions)

    sheet = Image.new("RGBA", (fw * columns, fh * rows), (0, 0, 0, 0))
    draw = ImageDraw.Draw(sheet)

    for row, direction in enumerate(directions):
        body = DIRECTION_COLORS[direction]
        dark = tuple(max(c - 60, 0) for c in body)
        for col in range(columns):
            ox, oy = col * fw, row * fh
            # Body (torso+legs block), leaves a few px of headroom.
            draw.rectangle([ox + 3, oy + 10, ox + fw - 4, oy + fh - 2], fill=body)
            # Head.
            draw.ellipse([ox + 4, oy + 1, ox + fw - 5, oy + 11], fill=(235, 200, 160))
            # Direction marker (face dot) so down/up/left/right read clearly.
            marker = {
                "down": (ox + fw // 2 - 1, oy + 6, ox + fw // 2 + 1, oy + 8),
                "up": (ox + fw // 2 - 1, oy + 2, ox + fw // 2 + 1, oy + 4),
                "left": (ox + 4, oy + 5, ox + 6, oy + 7),
                "right": (ox + fw - 7, oy + 5, ox + fw - 5, oy + 7),
            }[direction]
            draw.rectangle(marker, fill=(30, 30, 30))
            # Alternate leg offset per frame to fake a walk cycle.
            leg_shift = 2 if col % 2 == 1 else 0
            draw.rectangle(
                [ox + 4, oy + fh - 4 + (leg_shift // 2), ox + 6, oy + fh - 1],
                fill=dark,
            )
            draw.rectangle(
                [ox + fw - 7, oy + fh - 4 - (leg_shift // 2), ox + fw - 5, oy + fh - 1],
                fill=dark,
            )

    out_path = PLAYER_DIR / "player_sheet.png"
    sheet.save(out_path)
    print(f"Wrote {out_path} ({sheet.width}x{sheet.height})")


def make_tileset() -> None:
    """3 tiles side by side: grass (walkable), rock, tree (both solid)."""
    sheet = Image.new("RGBA", (TILE_SIZE * 3, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(sheet)

    # Tile 0: grass.
    draw.rectangle([0, 0, TILE_SIZE - 1, TILE_SIZE - 1], fill=(86, 160, 70))
    for x, y in [(2, 3), (9, 6), (5, 11), (12, 2)]:
        draw.point((x, y), fill=(70, 140, 58))

    # Tile 1: rock.
    ox = TILE_SIZE
    draw.rectangle([ox, 0, ox + TILE_SIZE - 1, TILE_SIZE - 1], fill=(86, 160, 70))
    draw.ellipse([ox + 3, 4, ox + 12, 13], fill=(130, 130, 130))
    draw.ellipse([ox + 3, 4, ox + 12, 13], outline=(90, 90, 90))

    # Tile 2: tree.
    ox = TILE_SIZE * 2
    draw.rectangle([ox, 0, ox + TILE_SIZE - 1, TILE_SIZE - 1], fill=(86, 160, 70))
    draw.rectangle([ox + 7, 9, ox + 9, 15], fill=(92, 60, 36))
    draw.ellipse([ox + 2, 0, ox + 14, 11], fill=(40, 110, 50))

    out_path = TILES_DIR / "tileset.png"
    sheet.save(out_path)
    print(f"Wrote {out_path} ({sheet.width}x{sheet.height})")


def main() -> None:
    PLAYER_DIR.mkdir(parents=True, exist_ok=True)
    TILES_DIR.mkdir(parents=True, exist_ok=True)

    config = json.loads((PLAYER_DIR / "sheet_config.json").read_text())
    make_player_sheet(config)
    make_tileset()


if __name__ == "__main__":
    main()
