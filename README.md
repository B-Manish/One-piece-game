# One Piece Game

Top-down 2D pixel art game (Godot 4.7, GDScript), Stardew-Valley-ish style.
Currently: just a player that walks around a small test world. No story,
combat, or inventory yet.

## Running it

1. Open Godot 4.7, choose **Import**, select this folder's `project.godot`.
2. Press **F5** (or the Play button) to run `scenes/main.tscn`.
3. Move with WASD or arrow keys (8-direction, diagonals aren't faster).

## Project layout

- `assets/` — sprites and tiles (currently placeholder art)
- `scenes/` — `main.tscn` (test world) and `scenes/player/player.tscn`
- `scripts/` — `main.gd` and `scripts/player/player.gd`
- `tools/` — one-off/re-runnable scripts that generate art and resources

## Swapping in your own sprite sheet

The player sheet layout lives in one place:
`assets/sprites/player/sheet_config.json`:

```json
{
  "frame_width": 16,
  "frame_height": 32,
  "columns": 4,
  "directions": ["down", "left", "right", "up"],
  "walk_fps": 8,
  "sheet_path": "res://assets/sprites/player/player_sheet.png"
}
```

To drop in your own Aseprite export:

1. Export a sheet with the same grid: one row per direction (in the order
   listed in `directions`), `columns` walk frames per row, each frame
   `frame_width` x `frame_height`. Or just edit the config to match whatever
   grid your sheet actually uses.
2. Save it over (or point `sheet_path` at) `player_sheet.png`.
3. Re-run the builder to regenerate the `SpriteFrames` resource:
   ```
   godot --headless --script tools/build_player_spriteframes.gd
   ```

No GDScript changes needed — `player.gd` just plays `walk_<direction>` /
`idle_<direction>` animations by name.

## Placeholder art

Nothing here is final art. `tools/make_placeholder_sprites.py` (requires
Pillow: `pip install Pillow`) generates:

- `assets/sprites/player/player_sheet.png` — 4 directions x 4 walk frames,
  16x32 each, colored per direction with a simple face marker.
- `assets/tiles/tileset.png` — grass, rock, tree, 16x16 each.

Re-run it any time with `python tools/make_placeholder_sprites.py`, then
re-run the two build scripts below to regenerate the Godot resources that
read those PNGs:

```
godot --headless --script tools/build_player_spriteframes.gd
godot --headless --script tools/build_tileset.gd
```

## Manual checks (can't see the game window from here)

- Movement feels right in all 8 directions, diagonals aren't faster.
- Idle animation matches the direction you were last walking.
- Walking into a rock or tree tile stops the player (collision works);
  walking over grass doesn't.
- Camera follows smoothly, no snapping/jitter.
- Window scales as pixel-perfect blocks when resized (no blurring).
