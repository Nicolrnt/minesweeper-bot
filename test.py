##
## test.py
##

coord = [3, 4]

# Print Coord
def print_coord(coord):
  print('[' + str(coord[0]) + ', ' + str(coord[1]) + ']')

# Main
def main():
  print('> From')
  print_coord(coord)

  print('> To Vertical')
  for y in range(coord[1], coord[1] + 2):
    for x in range(coord[0] - 1, coord[0] + 2):
      print_coord((x, y))

  print('> To Horizontal')
  for y in range(coord[1] - 1, coord[1] + 2):
    for x in range(coord[0], coord[0] + 2):
      print_coord((x, y))

# Launcher
main()
