import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def search_twitter(driver, query, search_type="latest"):
    search_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='SearchBox_Search_Input']"))
    )
    search_input.clear()
    search_input.send_keys(query)
    search_input.send_keys(Keys.RETURN)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Timeline: Search timeline']"))
    )

    if search_type == "latest":
        latest_tab = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Latest"))
        )
        latest_tab.click()
    elif search_type == "top":
        top_tab = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Top"))
        )
        top_tab.click()

def extract_tweets(driver, num_posts):
    tweets = []
    tweet_ids = set()
    last_height = driver.execute_script("return document.body.scrollHeight")

    while len(tweets) < num_posts:
        tweet_elements = driver.find_elements(By.CSS_SELECTOR, "article[role='article']")
        new_tweets_found = False
        for tweet in tweet_elements:
            try:
                tweet_text_element = tweet.find_elements(By.CSS_SELECTOR, "div[lang]")
                if not tweet_text_element:
                    continue
                tweet_text = tweet_text_element[0].text
                if tweet_text in tweet_ids:
                    continue
                tweet_ids.add(tweet_text)

                username_elements = tweet.find_elements(By.CSS_SELECTOR, "div[dir='ltr'] > span > span")
                if not username_elements:
                    continue
                username = username_elements[0].text

                timestamp_elements = tweet.find_elements(By.TAG_NAME, "time")
                if not timestamp_elements:
                    continue
                timestamp = timestamp_elements[0].get_attribute("datetime")

                link_elements = tweet.find_elements(By.CSS_SELECTOR, "a[role='link']")
                if not link_elements:
                    continue
                link = link_elements[0].get_attribute("href")
                
                tweets.append({
                    "text": tweet_text,
                    "username": username,
                    "link": link,
                    "timestamp": timestamp
                })
                new_tweets_found = True
                if len(tweets) >= num_posts:
                    break
            except Exception as e:
                print(f"Error extracting tweet: {e}")
                continue

        if not new_tweets_found:
            print("No new tweets found, stopping.")
            break

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Reached the end of the page, stopping.")
            break
        last_height = new_height

    return tweets[:num_posts]
