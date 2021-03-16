##
## setup.py
##

# Import

# Load Table
def load_table(driver):
  id_template = 'minesweeper-1-x-y'
  table = {}

  for y in range(0, 16):
    for x in range(0, 30):
      tile_id = id_template.replace('x', str(x)).replace('y', str(y))
      table[tile_id] = {
        'isSafe': False,
        'value': 9,
        'tile': driver.find_element_by_id(tile_id)
      }
  return (table)
