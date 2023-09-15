from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By

def get_events(url) -> list:
  browser_options = ChromeOptions()
  browser_options.add_argument('--headless')
  browser_options.add_argument('--ignore-certificate-errors')

  driver = Chrome(options=browser_options)
  driver.get(url)

  eventTables = driver.find_elements(By.CSS_SELECTOR, "div[class='Schedule__EventLeague mb5 Schedule__EventLeague--ufc']")
  eventTables.pop()

  ufcEvents = []

  for table in eventTables:
    body = table.find_element(By.CSS_SELECTOR, "tbody[class='Table__TBODY']")
    rows = body.find_elements(By.TAG_NAME, "tr")
    for row in rows:
      columns = row.find_elements(By.TAG_NAME, "td")
      event = {
        "link": columns[3].find_element(By.TAG_NAME, "a").get_attribute("href"),
        "date": columns[0].text,
        "time": columns[1].text,
        "name": columns[3].text,
        "location": columns[4].text,
      }
      ufcEvents.append(event)
  
  driver.quit()
  return ufcEvents

def get_fights(event) -> list:
  browser_options = ChromeOptions()
  # browser_options.add_argument('--headless')
  browser_options.add_argument('--ignore-certificate-errors')

  driver = Chrome(options=browser_options)
  driver.get(event)

  fightCards = driver.find_elements(By.CSS_SELECTOR, "section[class='Card MMAFightCard']")
  for fightCard in fightCards:
    cardName = fightCard.find_element(By.TAG_NAME, "header").text
    # fights = fightCard.find_elements(By.CSS_SELECTOR, "div[class='AccordionPanel mb4']")
    fights = fightCard.find_elements(By.CSS_SELECTOR, "div[class='AccordionPanel__header pointer']")
    for fight in fights:
      fight.click()
  print(fightCards)


def main():
  eventData = get_events("https://www.espn.com/mma/schedule/_/league/ufc")
  for event in eventData:
    get_fights(event["link"])

if __name__ == '__main__':
  main()