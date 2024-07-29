import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from sentiment_analysis import analyze_sentiment  # Import the sentiment analysis function

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def search_twitter(driver, query, search_type="latest"):
    try:
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='SearchBox_Search_Input']"))
        )
        search_input.clear()
        search_input.send_keys(query)
        search_input.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Timeline: Search timeline']"))
        )

        search_type_tab = "Latest" if search_type == "latest" else "Top"
        tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, search_type_tab))
        )
        tab.click()
    except Exception as e:
        logging.error(f"Error during search: {e}")

def extract_tweets(driver, num_posts, progress_bar=None, scroll_pause_time=1):
    tweets = []
    tweet_ids = set()
    last_height = driver.execute_script("return document.body.scrollHeight")

    while len(tweets) < num_posts:
        tweet_elements = driver.find_elements(By.CSS_SELECTOR, "article[role='article']")
        if not tweet_elements:
            logging.info("No tweets found, stopping.")
            break

        for tweet in tweet_elements:
            try:
                tweet_text_element = tweet.find_element(By.CSS_SELECTOR, "div[lang]")
                tweet_text = tweet_text_element.text
                if tweet_text in tweet_ids:
                    continue
                tweet_ids.add(tweet_text)

                username = tweet.find_element(By.CSS_SELECTOR, "div[dir='ltr'] > span > span").text
                timestamp = tweet.find_element(By.TAG_NAME, "time").get_attribute("datetime")
                link = tweet.find_element(By.CSS_SELECTOR, "a[role='link']").get_attribute("href")
                metadata = tweet.find_element(By.CSS_SELECTOR, "div[aria-label][role='group']").get_attribute("aria-label")
                
                reply_count, repost_count, like_count, bookmark_count, view_count = "0", "0", "0", "0", "0"
                for part in metadata.split(", "):
                    count, metric = part.split(" ")
                    if "replies" in metric:
                        reply_count = count
                    elif "reposts" in metric:
                        repost_count = count
                    elif "likes" in metric:
                        like_count = count
                    elif "bookmarks" in metric:
                        bookmark_count = count
                    elif "views" in metric:
                        view_count = count

                sentiment = analyze_sentiment(tweet_text)

                tweets.append({
                    "text": tweet_text,
                    "username": username,
                    "link": link,
                    "timestamp": timestamp,
                    "replies": reply_count,
                    "reposts": repost_count,
                    "likes": like_count,
                    "bookmarks": bookmark_count,
                    "views": view_count,
                    "sentiment": sentiment  # Add sentiment to the tweet data
                })
                if progress_bar:
                    progress_bar.update(1)
                if len(tweets) >= num_posts:
                    break
            except Exception as e:
                logging.error(f"Error extracting tweet: {e}")
                continue

        if len(tweets) < num_posts:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                logging.info("Reached the end of the page, stopping.")
                break
            last_height = new_height

    return tweets[:num_posts]
