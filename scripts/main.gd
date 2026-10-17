extends Node2D

## Test world: fills the ground with grass and drops a few solid
## obstacles (rocks/trees) so player collision can be verified by walking
## into them.

@onready var ground: TileMapLayer = $Ground

const GRID_WIDTH := 20
const GRID_HEIGHT := 12
const SOURCE_ID := 0

const GRASS := Vector2i(0, 0)
const ROCK := Vector2i(1, 0)
const TREE := Vector2i(2, 0)

const OBSTACLES := {
	Vector2i(3, 3): ROCK,
	Vector2i(4, 3): TREE,
	Vector2i(15, 8): ROCK,
	Vector2i(16, 2): TREE,
	Vector2i(9, 9): ROCK,
}


func _ready() -> void:
	for x in range(GRID_WIDTH):
		for y in range(GRID_HEIGHT):
			ground.set_cell(Vector2i(x, y), SOURCE_ID, GRASS)
	for coords in OBSTACLES:
		ground.set_cell(coords, SOURCE_ID, OBSTACLES[coords])
