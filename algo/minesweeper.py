##
## minesweeper.py
##

# Macro
DEBUG = False
UNKOWN = 9
FLAGGED = 10

# Import
import time
from algo.setup import load_table
from algo.update_table import update_table
from algo.utils import coord_to_id, click_tile, flag_tile, mark_tile, dislpay_table, print_coord, print_coord_with_msg

# Play First Move
def play_first_move(game):
  click_tile(game['table'], (15, 8))
  game['tableHasChanged'] = True
  return (game)

#
## C H E C K
#

# Coord Is Correct
def coord_is_correct(coord):
  x_limit = range(0, 30)
  y_limit = range(0, 16)

  if (coord[0] in x_limit and coord[1] in y_limit):
    return (True)
  return (False)

# Tiles Are Linked
def tiles_are_linked(table, tiles):
  if (
    table[coord_to_id(tiles[0])]['value'] != UNKOWN or
    table[coord_to_id(tiles[0])]['value'] != UNKOWN
  ):
    print('> HAHAHA')
    return (False)
  if (
    (
      tiles[0][0] == tiles[1][0] and
      tiles[0][1] == tiles[1][1] - 1
    ) or
    (
      tiles[0][1] == tiles[1][1] and
      tiles[0][0] == tiles[1][0] - 1
    )
  ):
    return (True)
  return (False)

# Link Is Vertical
def link_is_vertical(link):
  if (link[0][0] == link[1][0]):
    return (True)
  return (False)

# Is Unknown
def is_unknown(table, coord):
  if (coord_is_correct(coord) and table[coord_to_id(coord)]['value'] == UNKOWN):
    return (True)
  return (False)

# Is Flagged
def is_flagged(table, coord):
  if (coord_is_correct(coord) and table[coord_to_id(coord)]['value'] == FLAGGED):
    return (True)
  return (False)

# Is Same Coord
def is_same_coord(a, b):
  if (a[0] == b[0] and a[1] == b[1]):
    return (True)
  return (False)

#
## A C T I O N
#

# Free Tile
def free_tile(driver, table, coord):
  x_limit = range(0, 30)
  y_limit = range(0, 16)

  for y in range(coord[1] - 1, coord[1] + 2):
    for x in range(coord[0] - 1, coord[0] + 2):
      if (is_unknown(table, (x, y))):
        click_tile(table, (x, y))
  return (table)

# Free Guessed Tile
def free_guessed_tile(driver, game, field, coord):
  for y in range(coord[1] - 1, coord[1] + 2):
    for x in range(coord[0] - 1, coord[0] + 2):
      if (
        is_unknown(game['table'], (x, y)) and
        not is_same_coord(field['unknown_tiles'][0], (x, y)) and
        not is_same_coord(field['unknown_tiles'][1], (x, y))
      ):
        game['tableHasChanged'] = True
        game['nbInactive'] = 0
        click_tile(game['table'], (x, y))
  return (game)

# Lock Tile
def lock_tile(driver, table, coord):
  x_limit = range(0, 30)
  y_limit = range(0, 16)

  for y in range(coord[1] - 1, coord[1] + 2):
    for x in range(coord[0] - 1, coord[0] + 2):
      if (is_unknown(table, (x, y))):
        table[coord_to_id((x, y))]['value'] = 10
        flag_tile(driver, table, (x, y))
  return (table)

# Lock Guessed Tile
def lock_guessed_tile(driver, game, field, coord):
  for y in range(coord[1] - 1, coord[1] + 2):
    for x in range(coord[0] - 1, coord[0] + 2):
      if (
        is_unknown(game['table'], (x, y)) and
        not is_same_coord(field['unknown_tiles'][0], (x, y)) and
        not is_same_coord(field['unknown_tiles'][1], (x, y))
      ):
        game['tableHasChanged'] = True
        game['nbInactive'] = 0
        flag_tile(driver, game['table'], (x, y))
  return (game)

# Get Field Data
def get_field_data(table, coord):
  field = {
    'unknown_tiles': [],
    'nb_unknown': 0,
    'nb_flagged': 0
  }

  for y in range(coord[1] - 1, coord[1] + 2):
    for x in range(coord[0] - 1, coord[0] + 2):
      if (is_unknown(table, (x, y))):
        field['unknown_tiles'].append((x, y))
        field['nb_unknown'] += 1
      if (is_flagged(table, (x, y))):
        field['nb_flagged'] += 1
  return (field)

# Generate Target Coords
def generate_target_coords(coord, field):
  target_coords = []
  base_coord = field['unknown_tiles'][0]

  if (link_is_vertical(field['unknown_tiles'])):
    for y in range(base_coord[1], base_coord[1] + 2):
      for x in range(base_coord[0] - 1, base_coord[0] + 2):
        if (
          coord_is_correct((x, y)) and
          not is_same_coord(coord, (x, y)) and
          not is_same_coord(field['unknown_tiles'][0], (x, y)) and
          not is_same_coord(field['unknown_tiles'][1], (x, y))
        ):
          target_coords.append((x, y))
  else:
    for y in range(base_coord[1] - 1, base_coord[1] + 2):
      for x in range(base_coord[0], base_coord[0] + 2):
        if (
          coord_is_correct((x, y)) and
          not is_same_coord(coord, (x, y)) and
          not is_same_coord(field['unknown_tiles'][0], (x, y)) and
          not is_same_coord(field['unknown_tiles'][1], (x, y))
        ):
          target_coords.append((x, y))
  return (target_coords)

# Proceed Elimination
def proceed_elimination(driver, game, coord, field):
  print_coord_with_msg('proceed_elimination', coord)
  target_coords = generate_target_coords(coord, field)

  for target_coord in target_coords:
    target_field = get_field_data(game['table'], target_coord)
    if (target_field['nb_flagged'] == game['table'][coord_to_id(target_coord)]['value'] - 1):
      game = free_guessed_tile(driver, game, field, target_coord)
    elif (game['table'][coord_to_id(target_coord)]['value'] - target_field['nb_flagged'] == target_field['nb_unknown'] - 1):
      game = lock_guessed_tile(driver, game, field, target_coord)
  return (game)

# Check Satisfaction
def check_satisfaction(driver, game, coord):
  field = get_field_data(game['table'], coord)

  if (field['nb_flagged'] == game['table'][coord_to_id(coord)]['value']):
    game['tableHasChanged'] = True
    game['nbInactive'] = 0
    game['table'][coord_to_id(coord)]['isSafe'] = True
    game['table'] = free_tile(driver, game['table'], coord)
  elif (field['nb_unknown'] + field['nb_flagged'] == game['table'][coord_to_id(coord)]['value']):
    game['tableHasChanged'] = True
    game['nbInactive'] = 0
    game['table'][coord_to_id(coord)]['isSafe'] = True
    game['table'] = lock_tile(driver, game['table'], coord)
  return (game)

# Check Linked Tiles
def check_linked_tiles(driver, game, coord):
  field = get_field_data(game['table'], coord)

  if (
    # game['table'][coord_to_id(coord)]['value'] != 1 and
    field['nb_unknown'] == 2 and
    field['nb_flagged'] == game['table'][coord_to_id(coord)]['value'] - 1 and
    tiles_are_linked(game['table'], field['unknown_tiles'])
  ):
    game = proceed_elimination(driver, game, coord, field)
  return (game)

# Check Brut Force
def check_brut_force(driver, game, coord):
  print('> Check brut force')
  return (game)

# Play Next
def play_next(driver, game):
  number_list = [1, 2, 3, 4, 5, 6, 7, 8]

  game['tableHasChanged'] = False
  # Check satisfaction strategy
  for y in range(0, 16):
    for x in range(0, 30):
      if (not game['table'][coord_to_id((x, y))]['isSafe'] and game['table'][coord_to_id((x, y))]['value'] in number_list):
       game = check_satisfaction(driver, game, (x, y))
  # Check linked tiles strategy
  if (not game['tableHasChanged']):
    for y in range(0, 16):
      for x in range(0, 30):
        if (not game['table'][coord_to_id((x, y))]['isSafe'] and game['table'][coord_to_id((x, y))]['value'] in number_list):
          game = check_linked_tiles(driver, game, (x, y))
  # Check brut force strategy
  if (not game['tableHasChanged']):
    for y in range(0, 16):
      for x in range(0, 30):
        if (not game['table'][coord_to_id((x, y))]['isSafe'] and game['table'][coord_to_id((x, y))]['value'] in number_list):
          game = check_brut_force(driver, game, (x, y))
  return (game)

# Is Mined
def is_mined(table):
  nb_bomb = 100

  for tile_id in table.keys():
    if (table[tile_id]['value'] == FLAGGED):
      nb_bomb -= 1
  return (nb_bomb)

# Reset
def reset(driver, game):
  print('|===| R E S E T |===|')
  timeout = 60
  for i in range(0, timeout):
    print(str(timeout - i) + '..')
    time.sleep(1)
  driver.get('http://demineur.hugames.fr/')
  game['tableHasChanged'] = False
  game['nbInactive'] = 0
  game['table'] = load_table(driver)
  game = play_first_move(game)
  game['table'] = update_table(driver, game['table'])
  return (game)

# Play
def play(driver, table):
  game = {
    'tableHasChanged': False,
    'nbInactive': 0,
    'table': table
  }

  game = play_first_move(game)
  game['table'] = update_table(driver, game['table'])
  while (is_mined(table)):
    # if (not game['tableHasChanged']):
    game['table'] = update_table(driver, game['table'])
    game = play_next(driver, game)
    if (not game['tableHasChanged']):
      game['nbInactive'] += 1
    if (game['nbInactive'] == 2):
      game = reset(driver, game)
