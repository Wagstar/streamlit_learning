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

# pumpkins only pay out cubed when the whole block is harvested at once,
# so ripe ones wait until every pumpkin tile in the sweep is ripe
PUMPKIN_TILES = 0
for row in LAYOUT:
	for cell in row:
		if cell == P:
			PUMPKIN_TILES += 1

LAST_PUMPKIN = (0, 0)
for y in range(SIZE):
	for i in range(SIZE):
		if y % 2 == 0:
			x = i
		else:
			x = SIZE - 1 - i
		if LAYOUT[y][x] == P:
			LAST_PUMPKIN = (x, y)

ripe_pumpkins = 0
# sunflowers give the 5x bonus at max petals (15); lower the bar
# after sweeps without a harvest so they can't stall
sun_idle = 0
sun_harvested = False

def tend(x, y):
	global ripe_pumpkins, sun_idle, sun_harvested
	want = LAYOUT[y % SIZE][x % SIZE]
	have = get_entity_type()
	ripe = can_harvest()

	if want == P:
		# a Dead_Pumpkin is not harvestable but must be cleared
		if have == Entities.Dead_Pumpkin:
			harvest()
			have = None
		elif ripe:
			ripe_pumpkins += 1
			# last pumpkin tile of the sweep: cash in the whole block
			if ripe_pumpkins == PUMPKIN_TILES and (x, y) == LAST_PUMPKIN:
				harvest()
				have = None
			else:
				return
	elif want == S and have == S:
		if ripe and measure() >= 15 - sun_idle:
			harvest()
			sun_harvested = True
			have = None
	elif ripe:
		harvest()
		have = None
	elif have != want:
		# starting grass or something unwanted
		harvest()
		have = None

	# tile is empty: fix the ground, then plant
	if have == None:
		if needs_soil(want):
			if get_ground_type() != Grounds.Soil:
				till()
		else:
			if get_ground_type() != Grounds.Grassland:
				till()
		plant(want)

	# water anything that's growing and needs it
	if needs_water(want) and not can_harvest():
		water_tile()

# go to (0,0) in case the drone starts elsewhere
while get_pos_x() > 0:
	move(West)
while get_pos_y() > 0:
	move(South)

while True:
	ripe_pumpkins = 0
	sun_harvested = False
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
	if sun_harvested:
		sun_idle = 0
	else:
		sun_idle += 1
