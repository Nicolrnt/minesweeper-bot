##
## main.py
##

# Import
from driver import launch_driver
from log_manager import write_log
from algo.setup import load_table
from algo.minesweeper import play
import time

# Main
def main():
  write_log('|===| S T A R T |===|')
  driver = launch_driver('http://demineur.hugames.fr/')
  table = load_table(driver)
  play(driver, table)
  time.sleep(5)
  write_log('|===|   E N D   |===|')

# Launcher
if __name__ == "__main__":
  main()
