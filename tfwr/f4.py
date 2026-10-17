N = get_world_size()

T = Entities.Tree
G = Entities.Grass
B = Entities.Bush
C = Entities.Carrot
P = Entities.Pumpkin
S = Entities.Sunflower

# LAYOUT[y][x]  (8x8)
# Trees never touch each other, pumpkins sit in one 4x2 block,
# and 16 sunflowers (>= 10) allow the max-petal power bonus.
LAYOUT = [
	[T, G, T, G, T, G, T, G],
	[B, C, B, C, B, C, B, C],
	[T, G, T, G, T, G, T, G],
	[B, C, B, C, B, C, B, C],
	[G, B, G, B, P, P, P, P],
	[B, G, B, G, P, P, P, P],
	[S, S, S, S, S, S, S, S],
	[S, S, S, S, S, S, S, S],
]
SIZE = len(LAYOUT)

WATER_MIN = 0.5

def needs_soil(want):
	return want == C or want == P or want == S

def needs_water(want):
	return want == T or want == C or want == P or want == S

def water_tile():
	if get_water() < WATER_MIN and num_items(Items.Water) > 0:
		use_item(Items.Water)

def tend(x, y):
	want = LAYOUT[y % SIZE][x % SIZE]

	# clear the tile if it's ripe or holds the wrong thing
	# (starting grass, or a Dead_Pumpkin)
	if can_harvest():
		harvest()
	elif get_entity_type() != want:
		harvest()

	# tile is empty: fix the ground, then plant
	if get_entity_type() != want:
		if needs_soil(want):
			if get_ground_type() != Grounds.Soil:
				till()
		else:
			if get_ground_type() != Grounds.Grassland:
				till()
		plant(want)

	# water anything that's growing and needs it
	if needs_water(want):
		if get_entity_type() == want and not can_harvest():
			water_tile()

# go to (0,0) in case the drone starts elsewhere
while get_pos_x() > 0:
	move(West)
while get_pos_y() > 0:
	move(South)

while True:
	for y in range(N):
		for i in range(N):
			if y % 2 == 0:
				x = i
			else:
				x = N - 1 - i
			tend(x, y)
			if i < N - 1:
				if y % 2 == 0:
					move(East)
				else:
					move(West)
		move(North)
