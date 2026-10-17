extends SceneTree

# Builds assets/tiles/tileset.tres from assets/tiles/tileset.png:
# tile 0 = grass (walkable), tile 1 = rock, tile 2 = tree (both solid).
# Re-run after editing tileset.png: godot --headless --script tools/build_tileset.gd

const TEXTURE_PATH := "res://assets/tiles/tileset.png"
const OUT_PATH := "res://assets/tiles/tileset.tres"
const TILE_SIZE := Vector2i(16, 16)
const SOLID_TILES := [Vector2i(1, 0), Vector2i(2, 0)]

func _init() -> void:
	var tex: Texture2D = load(TEXTURE_PATH)

	var tileset := TileSet.new()
	tileset.tile_size = TILE_SIZE
	tileset.add_physics_layer()

	var source := TileSetAtlasSource.new()
	source.texture = tex
	source.texture_region_size = TILE_SIZE
	tileset.add_source(source)
	for i in range(3):
		source.create_tile(Vector2i(i, 0))

	var half := Vector2(TILE_SIZE) / 2.0
	var box := PackedVector2Array([
		Vector2(-half.x, -half.y), Vector2(half.x, -half.y),
		Vector2(half.x, half.y), Vector2(-half.x, half.y),
	])
	for coords in SOLID_TILES:
		var tile_data := source.get_tile_data(coords, 0)
		tile_data.add_collision_polygon(0)
		tile_data.set_collision_polygon_points(0, 0, box)

	var err := ResourceSaver.save(tileset, OUT_PATH)
	if err != OK:
		printerr("Failed to save TileSet: %s" % err)
	else:
		print("Wrote %s" % OUT_PATH)
	quit()
