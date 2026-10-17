extends SceneTree

# Builds assets/sprites/player/player_frames.tres from the placeholder (or
# your own) sheet, using the layout in assets/sprites/player/sheet_config.json.
# Re-run after swapping in a new sheet with the same config:
#   godot --headless --script tools/build_player_spriteframes.gd

const CONFIG_PATH := "res://assets/sprites/player/sheet_config.json"
const OUT_PATH := "res://assets/sprites/player/player_frames.tres"

func _init() -> void:
	var config_file := FileAccess.open(CONFIG_PATH, FileAccess.READ)
	var config: Dictionary = JSON.parse_string(config_file.get_as_text())
	config_file.close()

	var fw: int = config["frame_width"]
	var fh: int = config["frame_height"]
	var columns: int = config["columns"]
	var directions: Array = config["directions"]
	var walk_fps: float = config["walk_fps"]
	var sheet: Texture2D = load(config["sheet_path"])

	var frames := SpriteFrames.new()
	frames.remove_animation("default")

	for row in range(directions.size()):
		var direction: String = directions[row]
		var walk_anim := "walk_%s" % direction
		var idle_anim := "idle_%s" % direction

		frames.add_animation(walk_anim)
		frames.set_animation_speed(walk_anim, walk_fps)
		frames.set_animation_loop(walk_anim, true)

		frames.add_animation(idle_anim)
		frames.set_animation_speed(idle_anim, 1.0)
		frames.set_animation_loop(idle_anim, true)

		for col in range(columns):
			var atlas := AtlasTexture.new()
			atlas.atlas = sheet
			atlas.region = Rect2(col * fw, row * fh, fw, fh)
			frames.add_frame(walk_anim, atlas)
			if col == 0:
				frames.add_frame(idle_anim, atlas)

	var err := ResourceSaver.save(frames, OUT_PATH)
	if err != OK:
		printerr("Failed to save SpriteFrames: %s" % err)
	else:
		print("Wrote %s" % OUT_PATH)
	quit()
