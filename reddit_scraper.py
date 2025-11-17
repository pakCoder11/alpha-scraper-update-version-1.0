from bs4 import BeautifulSoup
import pyautogui 
import bot_functions
import data_store
import asyncio
from selenium_driverless import webdriver
import bot_functions
from selenium_driverless.types.by import By 
import time 
import re

def scrap_reddit_post_details(html_source):
    """
    Scrapes Reddit post details from HTML source using BeautifulSoup.
    
    Args:
        html_source (str): The full HTML source code of the Reddit post page.
    
    Returns:
        dict: A dictionary containing Post Title, Author, Total Upvotes, Time, and Reddit Community.
    """
    soup = BeautifulSoup(html_source, 'html.parser')
    
    # (1) Post Title - from shreddit-title's 'title' attribute
    title_tag = soup.find('shreddit-title')
    post_title = title_tag.get('title', '').strip() if title_tag else None
    
    # (2) Author - from <a> tag with aria-label containing "Author"
    author_tag = soup.find('a', {'aria-label': lambda x: x and 'Author' in x})
    author = author_tag.get_text(strip=True) if author_tag else None
    
    # (3) Total Upvotes - from faceplate-number inside action-row
    upvotes = None  

    faceplates = soup.find_all('faceplate-number', {"pretty" : ""})
    upvotes = faceplates[1]["number"]

    # (4) Time - from <time> tag's visible text (e.g., "15h ago")
    time_tag = soup.find('time')
    time_ago = time_tag.get_text(strip=True) if time_tag else None
    
    # (5) Reddit Community - from faceplate-hovercard's aria-label where data-id="community-hover-card"
    community_card = soup.find('faceplate-hovercard', {'data-id': 'community-hover-card'})
    community_url = None
    if community_card and community_card.get('aria-label'):
        community_name = community_card['aria-label']  # e.g., "r/ChatGPT"
        if community_name.startswith('r/'):
            community_url = f"https://www.reddit.com/{community_name}/"
    
    # Pack into dictionary
    result = {
        "Post Title": post_title,
        "Author": author,
        "Total Upvotes": upvotes,
        "Post Time": time_ago,
        "Reddit Community": community_url
    }
    
    return result

def scrape_shreddit_comments(html_source_code,post_data_dictionary):
    """
    Extracts comments from <shreddit-comment> blocks.
    Returns a list of dicts with keys: 'username', 'comment', 'comment_time'.
    """

    # remove the old instance of a file ...
    try:
        os.remove("reddit_comments_data.json")
    
    except Exception as e:
        pass

    soup = BeautifulSoup(html_source_code, 'html.parser')

    # Find all <shreddit-comment ...> tags
    for comment_tag in soup.find_all('shreddit-comment'):
        # (1) Username: prefer <faceplate-tracker noun="comment_author"> -> <a> text
        username = ''
        tracker = comment_tag.find('faceplate-tracker', attrs={'noun': 'comment_author'})
        if tracker:
            anchor = tracker.find('a')
            if anchor:
                username = anchor.get_text(strip=True)

        # Fallback: author attribute on <shreddit-comment>
        if not username:
            username = comment_tag.get('author', '') or ''

        # (2) Comment time: extract from <time> 'datetime' if available, else visible text
        comment_time = ''
        time_tag = comment_tag.find('time')
        if time_tag:
            # print(time_tag.text)
            comment_time = time_tag.text

        # (3) Comment text: <div slot="comment"> then aggregate <p> texts
        comment_text = ''
        content_div = comment_tag.find('div', attrs={'slot': 'comment'})
        if content_div:
            paragraphs = content_div.find_all('p')
            if paragraphs:
                comment_text = '\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
            else:
                # Fallback to all text inside the slot div
                comment_text = content_div.get_text(strip=True)


        comments_data_dictionary = {
              'username': username,
            'comment': comment_text,
            'comment_time': comment_time,
        }

        merged_data = {**post_data_dictionary, **comments_data_dictionary} 
        # print(f"The scraped comments data: {merged_data}")
        data_store.store_to_json(merged_data,"reddit_comments_data.json")

async def parse_links(html: str, base_url: str):
    try:
        soup = BeautifulSoup(html, "html.parser")
    except Exception as e:
        raise RuntimeError(f"HTML parsing failed: {e}") from e

    results = []

    # Find all <a> tags with data-testid="post-title" AND class="absolute inset-0"
    for a in soup.find_all("a"):

        try:
            # Check attribute presence
            if a.get("data-testid") != "post-title":
                continue

            classes = a.get("class") or []
            # class can be string or list; normalize to list
            if isinstance(classes, str):
                classes = classes.split()

            if not {"absolute", "inset-0"}.issubset(set(classes)):
                continue

            href = a.get("href")
            url = f"https://www.reddit.com{href}"
            results.append(url)
        
        except Exception:
            # Continue on individual element issues
            # continue
            pass

    return results

async def press_view_buttons_on_screen(driver,xpath_list):
    for xpath in xpath_list:
        try:
            element = await driver.find_element(By.XPATH, xpath)
            await element.click()
        except Exception as e:
            # print(f"Error clicking element with XPath {xpath}: {e}") 
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

# Define the asynchronous scraper function
async def scrape_comments_data_from_reddit(keyword,limit):
    # Use a headless Chrome browser for scraping 

    # ... existing code ...
    from pathlib import Path

    # Delete output artifacts safely with clear messages
    root = Path(__file__).resolve().parent
    targets = [
        "reddit_posts_urls.txt",
        "Reddit_comments_data.json",
        "Reddit_comments_data.xlsx",
    ]

    for name in targets:
        p = root / name
        try:
            if p.exists():
                p.unlink()
                print(f"Deleted: {p.name}")
            else:
                print(f"Not found: {p.name}")
        except PermissionError:
            print(f"Permission denied (is it open?): {p.name}")
        except Exception as e:
            print(f"Failed to delete {p.name}: {e}")

    # time.sleep(10)

    view_more_replies_xpaths = [
    # 1️⃣ Match button that contains "more replies"
    "//button[contains(., 'more replies')]",

    # 2️⃣ Match button span text directly containing "more replies"
    "//button//span[contains(text(), 'more replies')]",

    # 3️⃣ Match button span that starts with a number and ends with 'more replies'
    "//button//span[matches(normalize-space(text()), '^[0-9]+\\s+more replies$')]",

    # 4️⃣ Match button that has a descendant faceplate-number and text "more replies"
    "//button[.//faceplate-number and contains(., 'more replies')]",

    # 5️⃣ Match button with both SVG and text "more replies"
    "//button[.//svg and contains(., 'more replies')]",

    # 6️⃣ Match button based on class attribute and text
    "//button[contains(@class, 'text-tone-2') and contains(., 'more replies')]",

    # 7️⃣ Match button where any descendant span contains both number and 'more replies'
    "//button//span[contains(., 'more replies') and normalize-space(.) != '']",

    # 8️⃣ Match exact text pattern inside span (number + more replies)
    "//span[matches(., '^[0-9]+\\s+more replies$')]/ancestor::button",

    # 9️⃣ Match by faceplate-number sibling relationship
    "//faceplate-number/following-sibling::span[contains(., 'more replies')]/ancestor::button",

    # 🔟 Match button that has visible text matching number + 'more replies'

    "//button[normalize-space(.)[matches(., '^[0-9]+\\s+more replies$')]]"
    ]
    counter = 0

    options = webdriver.ChromeOptions() 
    options.add_argument("--incognito")
    query_to_search = f"https://www.reddit.com/search/?q={keyword}"

    async with webdriver.Chrome(options=options) as browser:
            try:
                # Open the target website

                await browser.get(query_to_search,wait_load=False)
                await asyncio.sleep(20)  # Wait for the page to load

                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.press('tab')

                for _ in range(0,limit):

                    bot_functions.press_down_keys(120)
                    # await press_view_buttons_on_screen(browser,view_more_replies_xpaths)
                    html_content = await browser.page_source

                    reddit_posts_parsed_links = await parse_links(html_content, query_to_search)
                    with open("reddit_posts_urls.txt", "a+") as file:
                        for url in reddit_posts_parsed_links:
                            file.write(url + "\n")
                
                await asyncio.sleep(2)  # Wait for the page to load
                # now start redirecting to url  one by one and scrape the comments
                for url in reddit_posts_parsed_links:
                    await browser.get(url,wait_load='networkidle')
                    await asyncio.sleep(2)  # Wait for the page to load
                    
                    await press_view_buttons_on_screen(browser,view_more_replies_xpaths)
                    await asyncio.sleep(2)  # Wait for the page to load

                    html_content = await browser.page_source
                    post_details = scrap_reddit_post_details(html_content)
                    scrape_shreddit_comments(html_content,post_details)

                    if counter == limit:
                        break

                    counter += 1
                    print(f"The counter is {counter}")

            except Exception as e:
                # Print any errors encountered during scraping
    
                print(f"Error scraping : {e}")

    data_store.save_data_to_excel("reddit_comments_data.json","Reddit_comments_data.xlsx") 
    data_store.excel_to_json("Reddit_comments_data.xlsx","Reddit_comments_data.json")    

# Example usage:
if __name__ == "__main__":
    asyncio.run(scrape_comments_data_from_reddit("donald trump",2))
