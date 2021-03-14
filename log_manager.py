##
## log.py
##

# Import

# Write Log
def write_log(msg):
  file = open('run.log', 'a')
  file.write('> ' + msg + '\n')
  file.close()
