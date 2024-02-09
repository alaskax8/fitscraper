from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
from datetime import datetime
from pathlib import Path

def main():

    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    # executable_path param is not needed if you updated PATH
    browser = webdriver.Firefox(options=options)
    studios = ["muenchen-pasing", "muenchen-laim"]
    log_file = Path("logs/log-studio-percentage.csv")

    while True:
        studio_percentages = []
        for studio in studios:
            browser.get("https://www.fit-star.de/fitnessstudio/" + studio)
            html = browser.page_source
            soup = BeautifulSoup(html, features="html.parser")
            studio_percentages.append(soup.find("div", class_="fs-livedata-percentage").find("strong").get_text()[:-1])
        file_exists = log_file.is_file()
        with open(log_file, 'a', newline='') as csvfile:
                logwriter = csv.writer(csvfile, delimiter=';')
                if not file_exists:
                     logwriter.writerow(["Datetime"] + studios)
                logwriter.writerow([str(datetime.now())] + [int(studio_percentage) for studio_percentage in studio_percentages])
        print(studio_percentages)
        time.sleep(30)
    browser.quit()


if __name__ == '__main__':
    main()