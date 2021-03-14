##
## update_table.py
##

# Macro
UNKOWN = 9

# Import

# Class To Value
def class_to_value(tile_classes):
  if (tile_classes.find('minesweeper-nb-0') != -1):
    return (0)
  elif (tile_classes.find('minesweeper-nb-1') != -1):
    return (1)
  elif (tile_classes.find('minesweeper-nb-2') != -1):
    return (2)
  elif (tile_classes.find('minesweeper-nb-3') != -1):
    return (3)
  elif (tile_classes.find('minesweeper-nb-4') != -1):
    return (4)
  elif (tile_classes.find('minesweeper-nb-5') != -1):
    return (5)
  elif (tile_classes.find('minesweeper-nb-6') != -1):
    return (6)
  elif (tile_classes.find('minesweeper-nb-7') != -1):
    return (7)
  elif (tile_classes.find('minesweeper-nb-8') != -1):
    return (8)
  elif (tile_classes.find('minesweeper-unknown') != -1):
    return (9)
  elif (tile_classes.find('minesweeper-flag') != -1):
    return (10)

# Update Table
def update_table(driver, table):
  for tile_id in table.keys():
    if (table[tile_id]['value'] == UNKOWN):
      tile_classes = driver.find_element_by_id(tile_id).get_attribute('class')
      table[tile_id]['value'] = class_to_value(tile_classes)
  return (table)
