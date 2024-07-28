# Twitter Scraper

This project is a Twitter scraper built using Selenium. It logs into Twitter, searches for tweets based on a specified query, and extracts tweets with their metadata. The extracted data is saved in a JSON file.

## Table of Contents

- [Setup](#setup)
- [Usage](#usage)
- [Files](#files)
- [Contributing](#contributing)
- [License](#license)

## Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/BenzrakMarouan/twitter_scraper.git
    cd twitter_scraper
    ```

2. **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Configure your credentials and settings:**
   - Open `config.py` and add your Twitter email, username, and password:
     ```python
     EMAIL = "your_email@gmail.com"
     USERNAME = "your_username"
     PASSWORD = "your_password"
     COOKIES_FILE = "twitter_cookies.pkl"
     JSON_FILE = "tweets_data.json"
     CHROMEDRIVER_PATH = 'chromedriver-win64/chromedriver.exe'
     ```

4. **Download ChromeDriver:**
   - Ensure you have the correct version of [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) matching your Chrome browser version.
   - Place the ChromeDriver executable in the specified path (`chromedriver-win64/chromedriver.exe`).

## Usage

To run the Twitter scraper, use the following command:

```sh
python main.py "your_search_query" 10 "latest"
