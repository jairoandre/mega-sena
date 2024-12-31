import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import csv
import datetime

dozens = list(range(1,61))

def random_game(n):
  return random.sample(dozens, n)

def open_browser():
  print("Open browser")
  options = webdriver.ChromeOptions()
  options.add_experimental_option("debuggerAddress", "localhost:9222")
  driver = webdriver.Chrome(options=options)
  driver.get("https://www.loteriasonline.caixa.gov.br/silce-web/#/mega-sena/especial")
  print("Open tab")
  driver.implicitly_wait(2)
  return driver

def fill_game(driver, game):
  html = driver.find_element(By.TAG_NAME, 'html')
  html.send_keys(Keys.UP)
  for n in game:
    driver.implicitly_wait(1)
    elem_id = "n" + str(n).zfill(2)
    elem = driver.find_element("id", elem_id)
    clicked = False
    while not clicked:
      try:
        elem.click()
        clicked = True
      except WebDriverException:
        print("Error clicking")
        html.send_keys(Keys.UP)
  html.send_keys(Keys.DOWN)
  driver.implicitly_wait(2)
  cart_btn = driver.find_element("id", "colocarnocarrinho")
  cart_btn.click()

def read_games(file_name):
  games = []
  with open(file_name, newline='') as csvfile:
    lines = csv.reader(csvfile)
    for line in lines:
      game = [int(v) for v in line]
      games.append(game)
    return games
 
def gen_picks():
  past_games = read_games("results.csv")
  picks = []
  picks_to_sheet = []
  count_gen = 0
  while len(picks) < 87:
    count_gen += 1
    print(count_gen,end='\r')
    game = random_game(6)
    c4 = 0
    game_count = 0
    for past_game in past_games:
      game_count += 1
      c = count_matches(game, past_game)
      if c == 4:
        c4 += 1
    if c4 >= 3:
      picks.append(game)
      game_copy = game.copy()
      game_copy.append(c4)
      picks_to_sheet.append(game_copy)
  return [picks,picks_to_sheet]

def write_picks_to_csv(file_name, picks):
  timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
  with open(f"{file_name}.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for pick in picks:
      writer.writerow(pick)

def count_matches(l1,l2):
  set1 = set(l1)
  set2 = set(l2)
  matches = set1.intersection(set2)
  return len(matches)

def gen_games():
  picks = gen_picks()
  games = picks[0]
  games_to_sheet = picks[1]
  write_picks_to_csv("games", games)
  write_picks_to_csv("to_sheet", games_to_sheet)

def fill_games():
  games = read_games("games.csv")
  driver = open_browser()
  for game in games:
    print(game)
    fill_game(driver, game)
  driver.quit()

#gen_games()
fill_games()