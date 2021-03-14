##
## driver.py
##

# Import
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from log_manager import write_log

# Get driver
def get_driver():
  write_log('get_driver()')
  driver = webdriver.Chrome(executable_path=r'./chromedriver')
  driver.maximize_window()
  return (driver)

# Launch Driver
def launch_driver(url):
  write_log('launch_driver()')
  driver = get_driver()
  driver.get(url)
  return (driver)
