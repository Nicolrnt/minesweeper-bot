##
## utils.py
##

# Import
import sys
import time
from selenium.webdriver import ActionChains

# Coord To Id
def coord_to_id(coord):
  tile_id_template = 'minesweeper-1-x-y'

  tile_id = tile_id_template.replace('x', str(coord[0])).replace('y', str(coord[1]))
  return (tile_id)

# Click Tile
def click_tile(table, coord):
  table[coord_to_id(coord)]['tile'].click()

# Flag Tile
def flag_tile(driver, table, coord):
  action = ActionChains(driver)
  action.context_click(table[coord_to_id(coord)]['tile']).perform()

# Mark Tile
def mark_tile(driver, table, coord, is_clean):
  flag_tile(driver, table, coord)
  if (is_clean):
    flag_tile(driver, table, coord)

# Print Coord
def print_coord(coord):
  print('> Tile : [' + str(coord[0]) + ', ' + str(coord[1]) + ']')

# Print Coord With Msg
def print_coord_with_msg(msg, coord):
  print('> ' + msg + ' : [' + str(coord[0]) + ', ' + str(coord[1]) + ']')

# Display Table
def dislpay_table(table):
  ascii_char = ['  ', ' 1', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7', ' 8', '..', '|>']
  row = ''

  row = '      '
  for i in range(0, 30):
    if (i < 10):
      row += ' ' + str(i) + ' | '
    else:
      row += str(i) + ' | '
  print(row)
  for y in range(0, 16):
    row = str(y)
    if (y < 10):
       row += ' > | '
    else:
      row += '> | '
    for x in range(0, 30):
      row += ascii_char[table[coord_to_id((x, y))]['value']] + ' | '
    print(row)
