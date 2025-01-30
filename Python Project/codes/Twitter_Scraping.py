from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
import time
import pandas as pd


# we get sth like this: 228,Cristobal,28,"41,017",5 hrs
# convert tweet count string into int; duration (5 hrs) in to int
def clean_data(count, duration):
    count_cleaned = int(count.replace(",", ""))
    duration_cleaned = duration.replace("hrs", "").strip()
    return count_cleaned, duration_cleaned

def twitter_scrap():
    # Settings for Chrome web browser
    # download and working safely if needed
    options = Options()
    download_dir = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    service = Service ('chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)

    # start with the website
    driver.get("https://trends24.in/united-states/")
    time.sleep(3)

    # Dynamic: press button to find location of resource
    try:
        table_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-link-table"]'))
        )
        table_button.click()
        print("Going to the Twitter Table...")
    except Exception as e:
        print("Error1:", e)

    # wait for loading the information
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "rank"))
        )
        print("Rank information loading...")
    except Exception as e:
        print("Error2:", e)

    # soup all columns needed
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    ranks = soup.find_all('td', class_='rank')
    trends = soup.find_all('td', class_='topic')
    positions = soup.find_all('td', class_='position')
    counts = soup.find_all('td', class_='count')
    durations = soup.find_all('td', class_='duration')

    # get all information to a temporary list, and also clean the data
    rows = []
    for rank, trend, position, count, duration in zip(ranks, trends, positions, counts, durations):
        tweet_count_cleaned, duration_cleaned = clean_data(count.text.strip(), duration.text.strip())
        rows.append({
            # without cleaning
            # 'Rank': rank.text.strip(),
            # 'Trending Topic': trend.text.strip(),
            # 'Top Position': position.text.strip(),
            # 'Tweet Count': count.text.strip(),
            # 'Duration': duration.text.strip()
            'Rank': int(rank.text.strip()),
            'Trending Topic': trend.text.strip(),
            'Top Position': int(position.text.strip()),
            'Tweet Count': tweet_count_cleaned,
            'Duration': duration_cleaned
        })

    # create dataframe schema and put information into the dataframe
    df = pd.DataFrame(columns=['Rank', 'Trending Topic', 'Top Position', 'Tweet Count', 'Duration'])
    df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)

    # print to see dataframe, close web browser as well
    print(df)
    driver.quit()

    # save dataframe as a csv file
    csv_filename = "Twitter_trends.csv"
    df.to_csv(csv_filename, index=False)
    print("Getting Twitter data done!")

if __name__ == '__main__':
    twitter_scrap()