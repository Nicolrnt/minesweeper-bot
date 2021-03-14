##
## minesweeper.py
##

# Macro
DEBUG = False
UNKOWN = 9
FLAGGED = 10

# Import
from algo.update_table import update_table
from algo.utils import coord_to_id, click_tile, flag_tile, dislpay_table, print_coord, print_coord_with_msg
from log_manager import write_log

# Play First Move
def play_first_move(table):
  click_tile(table, (15, 8))

# Free Tile
def free_tile(driver, table, coord):
  x_limit = range(0, 30)
  y_limit = range(0, 16)

  for y in range(coord[1] - 1, coord[1] + 2):
    for x in range(coord[0] - 1, coord[0] + 2):
      if (x in x_limit and y in y_limit and table[coord_to_id((x, y))]['value'] == UNKOWN):
        click_tile(table, (x, y))
  return (table)

# Lock Tile
def lock_tile(driver, table, coord):
  x_limit = range(0, 30)
  y_limit = range(0, 16)

  for y in range(coord[1] - 1, coord[1] + 2):
    for x in range(coord[0] - 1, coord[0] + 2):
      if (x in x_limit and y in y_limit and table[coord_to_id((x, y))]['value'] == UNKOWN):
        table[coord_to_id((x, y))]['value'] = 10
        flag_tile(driver, table, (x, y))
  return (table)

# Check Satisfaction
def check_satisfaction(driver, table, coord):
  tableHasChanged = False
  nb_unknown = 0
  nb_flagged = 0
  x_limit = range(0, 30)
  y_limit = range(0, 16)

  for y in range(coord[1] - 1, coord[1] + 2):
    for x in range(coord[0] - 1, coord[0] + 2):
      if (x in x_limit and y in y_limit and table[coord_to_id((x, y))]['value'] == UNKOWN):
        nb_unknown += 1
      if (x in x_limit and y in y_limit and table[coord_to_id((x, y))]['value'] == FLAGGED):
        nb_flagged += 1
  if (nb_flagged == table[coord_to_id(coord)]['value']):
    table[coord_to_id(coord)]['isSafe'] = True
    tableHasChanged = True
    table = free_tile(driver, table, coord)
  elif (nb_unknown + nb_flagged == table[coord_to_id(coord)]['value']):
    table[coord_to_id(coord)]['isSafe'] = True
    tableHasChanged = True
    table = lock_tile(driver, table, coord)
  return table, tableHasChanged

# Check Link Tiles
def check_linked_tiles(driver, table, coord):
  unknown_tiles = []
  nb_flagged = 0

  for y in range(coord[1] - 2, coord[1] + 3):
    for x in range(coord[0] - 2, coord[0] + 3):
      if (x in x_limit and y in y_limit and table[coord_to_id((x, y))]['value'] == UNKOWN):
        unknown_tiles.append((x, y))
        nb_linked += 1
      if (x in x_limit and y in y_limit and table[coord_to_id((x, y))]['value'] == FLAGGED):
        nb_flagged += 1


# Play Next
def play_next(driver, table, tableHasChanged):
  number_list = [1, 2, 3, 4, 5, 6, 7, 8]

  if (not tableHasChanged):
    # table = check_linked_tiles(driver, table, (x, y))
    print('Table Hasn\'t Changed')
  for y in range(0, 16):
    for x in range(0, 30):
      if (not table[coord_to_id((x, y))]['isSafe'] and table[coord_to_id((x, y))]['value'] in number_list):
        table, tableHasChanged = check_satisfaction(driver, table, (x, y))
  return table, tableHasChanged

# Is Mined
def is_mined(table):
  nb_bomb = 100

  for tile_id in table.keys():
    if (table[tile_id]['value'] == FLAGGED):
      nb_bomb -= 1
  return (nb_bomb)

# Play
def play(driver, table):
  tableHasChanged = True

  play_first_move(table)
  while (is_mined(table)):
    table = update_table(driver, table)
    if (DEBUG):
      dislpay_table(table)
    table, tableHasChanged = play_next(driver, table, tableHasChanged)
