import asyncio
from bs4 import BeautifulSoup
import re
from datetime import datetime
import data_store 
import bot_functions
from selenium_driverless import webdriver
import json
import urllib.request 
import os

# Push a log line to the Flask app so it can broadcast via Socket.IO
def push_log(msg):
    try:
        data = json.dumps({"message": str(msg)}).encode("utf-8")
        req = urllib.request.Request(
            "http://127.0.0.1:5000/api/push-log",
            data=data,
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=1.5).read()
    except Exception:
        # swallow any network error to avoid breaking scraping flow
        pass

# Make file logging append and also emit to Live Logs
def write_logs_to_file(str):
    try:
        with open('logs.txt', 'a', encoding='utf-8') as f:
            f.write(str + "\n")
    except Exception:
        pass
    try:
        push_log(str)
    except Exception:
        pass


def scrape_tweets(html_code):
    # Set up headers to mimic a browser request

    print(len(html_code))
    
    try:
        # Parse the HTML content
        soup = BeautifulSoup(html_code, 'html.parser')
        
        # Find all tweet cells
        tweet_cells = soup.find_all('div', {'data-testid': 'cellInnerDiv'})
        
        all_tweets = []
        print(f"Found {len(tweet_cells)} tweet cells")
        
        for tweet in tweet_cells:
            tweet_data = {}
            
            # Extract Account URL and Username
            user_element = tweet.find('div', {'data-testid': 'User-Name'})
            if user_element:
                account_link = user_element.find('a', href=True)
                if account_link:
                    tweet_data['Account URL'] = f"https://twitter.com{account_link['href']}"
                    username_span = account_link.find('span', class_=lambda c: c and 'r-poiln3' in c)
                    if username_span:
                        tweet_data['Username'] = username_span.get_text().strip()
            
            # Extract Tweet Text
            tweet_text_element = tweet.find('div', {'data-testid': 'tweetText'})
            if tweet_text_element:
                # Get all text content
                full_text = ""
                hashtags = []
                mentions = []
                
                # Process all spans and links to build the tweet text
                for element in tweet_text_element.find_all(['span', 'a']):
                    if element.name == 'a' and 'hashtag_click' in element.get('href', ''):
                        # This is a hashtag
                        hashtag_text = element.get_text().strip()
                        # Add space before hashtag if not at beginning of text
                        if full_text and not full_text.endswith(' '):
                            full_text += ' '
                        full_text += hashtag_text
                        # Add space after hashtag
                        full_text += ' '
                        
                        if hashtag_text.startswith('#'):
                            hashtags.append(hashtag_text)
                        else:
                            hashtags.append(f"#{hashtag_text}")

                            
                    elif element.name == 'a' and 'src=mention' in element.get('href', ''):
                        # This is a mention
                        mention = element.get_text().strip()
                        # Add space before mention if not at beginning of text
                        if full_text and not full_text.endswith(' '):
                            full_text += ' '
                        full_text += mention
                        # Add space after mention
                        full_text += ' '
                        
                        mentions.append(mention)

                    else:
                        # Regular text
                        text = element.get_text().strip()
                        if text:
                            full_text += text
                
                tweet_data['Tweet Text'] = full_text.strip()  # Remove any trailing spaces
                tweet_data['Hashtags'] = hashtags.join(', ') if hashtags else None  
            # Extract Time
            time_element = tweet.find('time')
            if time_element and 'datetime' in time_element.attrs:
                tweet_data['Time'] = time_element['datetime']
            
            # Extract engagement metrics (replies, reposts, likes, bookmarks, views)
            engagement_div = tweet.find('div', {'aria-label': re.compile(r'.*replies.*reposts.*likes.*bookmarks.*views.*'), 'role': 'group'})
            if engagement_div:
                aria_label = engagement_div.get('aria-label', '')
                # Parse metrics from aria-label attribute
                metrics_pattern = re.compile(r'(\d+) replies, (\d+) reposts, (\d+) likes, (\d+) bookmarks, (\d+) views')
                metrics_match = metrics_pattern.search(aria_label)
                
                if metrics_match:
                    tweet_data['Replies'] = int(metrics_match.group(1))
                    tweet_data['Reposts'] = int(metrics_match.group(2))
                    tweet_data['Likes'] = int(metrics_match.group(3))
                    tweet_data['Bookmarks'] = int(metrics_match.group(4))
                    tweet_data['Views'] = int(metrics_match.group(5))
            
            # Only add if we have meaningful data
            if tweet_data.get('Tweet Text') and tweet_data.get('Username'):
                all_tweets.append(tweet_data)
            
            if len(tweet_data) > 0:
                data_store.store_to_json(tweet_data, 'tweets_data.json')

                write_logs_to_file("-------------------")
                for key, value in tweet_data.items():
                    write_logs_to_file(f"{key}: {value}")
                write_logs_to_file("-------------------")
            
            else: 
                print("No data found ...")

    except Exception as e:
        print(f"Error scraping tweets: {e}")
        # return []

    print("Function completed ...")

# Define the asynchronous scraper function
async def scrape_tweets_using_selenium(account_url,down_scroll_limit):
    # Use a headless Chrome browser for scraping 
    # only scrape tweets from profiles ... 
    # try: 

    #     os.remove('tweets_data.json')
    #     os.remove('Tweets_Data.xlsx')
    # except Exception as e:
    #     print(f"Error deleting files: {e}")

    options = webdriver.ChromeOptions() 
    options.add_argument('--icognito')  # Run in headless mode

    async with webdriver.Chrome() as browser:
            try:
                # Open the target website
                await browser.get(url=account_url)
                await asyncio.sleep(10.0)  # Wait for the page to load

                bot_functions.press_tab_key(4)
                await asyncio.sleep(3.0)  # Wait for the page to load

                for _ in range(0,down_scroll_limit):

                    bot_functions.press_down_keys(100)
                    await asyncio.sleep(3.0)  # Wait for the page to load

                    html_code = await browser.page_source 
                    print(len(html_code))

                    scrape_tweets(html_code)

                    await asyncio.sleep(1.0)  # Wait for the page to load 
                    print(_)
                
            except Exception as e:
                # Print any errors encountered during scraping
                print(f"Error scraping : {e}")
    
    data_store.save_data_to_excel('tweets_data.json','Tweets_Data.xlsx')
    data_store.excel_to_json('Tweets_Data.xlsx','tweets_data.json')

async def backend_function(profile_url: str, scroll_count: int):
    """
    Wrapper coroutine that runs tweets scraping, then converts JSON to Excel.
    This ensures UI receives completion only after files are saved.
    """
    try:
        print("Tweets Scraper – initializing")
        await scrape_tweets_using_selenium(profile_url, scroll_count)
        print("Tweets Scraper – converting JSON to Excel...")
        try:
            data_store.json_to_excel('tweets_data.json', 'Tweets_Data.xlsx')
            print("Tweets Scraper – Excel saved: Tweets_Data.xlsx")
        except Exception as e:
            print(f"Tweets Scraper – Excel conversion failed: {e}")
    except Exception as e:
        print(f"Tweets Scraper – failed: {e}")

if __name__ == "__main__":
    account_url = "https://x.com/nvidianewsroom"
    asyncio.run(scrape_tweets_using_selenium(account_url,2))
    