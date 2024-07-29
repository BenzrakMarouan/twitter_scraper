import argparse
import time
from config import EMAIL, USERNAME, PASSWORD, COOKIES_FILE, JSON_FILE, CHROMEDRIVER_PATH, DB_FILE
from setup import create_driver
from auth import login_to_twitter, load_cookies
from scraper import search_twitter, extract_tweets
from database import create_connection, create_table, insert_tweet
from tqdm import tqdm

def main(query, num_posts, search_type):
    driver = create_driver(CHROMEDRIVER_PATH)
    conn = create_connection(DB_FILE)
    create_table(conn)
    
    try:
        load_cookies(driver, COOKIES_FILE)
        
        driver.get("https://twitter.com/home")
        if "login" in driver.current_url:
            login_to_twitter(driver, EMAIL, USERNAME, PASSWORD, COOKIES_FILE)

        print("Successfully logged in to Twitter!")

        search_twitter(driver, query, search_type)

        print(f"Fetching {num_posts} tweets...")
        with tqdm(total=num_posts) as progress_bar:
            new_tweets = extract_tweets(driver, num_posts, progress_bar)

        for tweet in new_tweets:
            insert_tweet(conn, tweet)

        print(f"Fetched and saved {len(new_tweets)} new tweets.")
    finally:
        driver.quit()
        conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Twitter Scraper')
    parser.add_argument('query', type=str, help='The search query')
    parser.add_argument('num_posts', type=int, help='Number of posts to fetch')
    parser.add_argument('search_type', type=str, choices=['latest', 'top'], help='Search type: latest or top')
    args = parser.parse_args()
    
    main(args.query, args.num_posts, args.search_type)
