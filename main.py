##
## main.py
##

# Import
from driver import launch_driver
from log_manager import write_log
from algo.minesweeper import play
import time

# Get Minesweeper Table
def get_minesweeper_table(driver):
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

# Main
def main():
  write_log('|===| S T A R T |===|')
  driver = launch_driver('http://demineur.hugames.fr/')
  table = get_minesweeper_table(driver)
  play(driver, table)
  time.sleep(5)
  write_log('|===|   E N D   |===|')

# Launcher
if __name__ == "__main__":
  main()
