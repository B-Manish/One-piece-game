extends CharacterBody2D

## Top-down 8-direction player controller.
## Drives an AnimatedSprite2D with walk_<dir>/idle_<dir> animations
## (built by tools/build_player_spriteframes.gd) where <dir> is one of
## down, up, left, right.

@export var speed: float = 80.0

@onready var sprite: AnimatedSprite2D = $AnimatedSprite2D

var _last_direction: String = "down"


func _physics_process(_delta: float) -> void:
	var input_vector := Vector2(
		Input.get_action_strength("move_right") - Input.get_action_strength("move_left"),
		Input.get_action_strength("move_down") - Input.get_action_strength("move_up")
	)
	if input_vector.length() > 1.0:
		input_vector = input_vector.normalized()

	velocity = input_vector * speed
	move_and_slide()

	_update_animation(input_vector)


func _update_animation(input_vector: Vector2) -> void:
	if input_vector.is_zero_approx():
		sprite.play("idle_%s" % _last_direction)
		return

	_last_direction = _direction_from_vector(input_vector)
	sprite.play("walk_%s" % _last_direction)


func _direction_from_vector(v: Vector2) -> String:
	# Pick whichever axis dominates so diagonal input still maps to one
	# of the four sprite directions instead of blending nonexistent ones.
	if absf(v.x) > absf(v.y):
		return "right" if v.x > 0.0 else "left"
	return "down" if v.y > 0.0 else "up"
