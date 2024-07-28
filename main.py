import argparse
import time
from config import EMAIL, USERNAME, PASSWORD, COOKIES_FILE, JSON_FILE, CHROMEDRIVER_PATH
from setup import create_driver
from auth import login_to_twitter, load_cookies
from scraper import search_twitter, extract_tweets
from utils import load_existing_data, save_to_json

def main(query, num_posts, search_type):
    driver = create_driver(CHROMEDRIVER_PATH)
    try:
        load_cookies(driver, COOKIES_FILE)
        
        driver.get("https://twitter.com/home")
        if "login" in driver.current_url:
            login_to_twitter(driver, EMAIL, USERNAME, PASSWORD, COOKIES_FILE)

        print("Successfully logged in to Twitter!")

        existing_tweets = load_existing_data(JSON_FILE)
        existing_texts = {tweet['text'] for tweet in existing_tweets}

        search_twitter(driver, query, search_type)

        new_tweets = extract_tweets(driver, num_posts)

        unique_new_tweets = [tweet for tweet in new_tweets if tweet['text'] not in existing_texts]

        all_tweets = existing_tweets + unique_new_tweets
        save_to_json(all_tweets, JSON_FILE)

        print(f"Fetched {len(unique_new_tweets)} new unique tweets:")
        for tweet in unique_new_tweets:
            print(tweet)
            print("------")

    finally:
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Twitter Scraper')
    parser.add_argument('query', type=str, help='The search query')
    parser.add_argument('num_posts', type=int, help='Number of posts to fetch')
    parser.add_argument('search_type', type=str, choices=['latest', 'top'], help='Search type: latest or top')
    args = parser.parse_args()
    
    main(args.query, args.num_posts, args.search_type)
