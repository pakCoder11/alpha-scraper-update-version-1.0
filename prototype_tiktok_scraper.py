import asyncio
import re
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import source_code_downloader 
import bot_functions
import time
import pyautogui

def extract_comments(html_content,url):
    """
    Scrape comments from TikTok videos.
    
    Args:
        html_content (str): HTML content of the TikTok video page
        
    Returns:
        list: A list of dictionaries containing comment details
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all comment wrapper divs
    comment_wrappers = soup.find_all('div', class_='css-13wx63w-DivCommentObjectWrapper')
    
    comments_data = []
    
    for wrapper in comment_wrappers:
        # Find all comment items within the wrapper
        comment_items = wrapper.find_all('div', class_='css-1gstnae-DivCommentItemWrapper')
        
        for comment_item in comment_items:
            # Extract username and profile link
            username_element = comment_item.select_one('[data-e2e^="comment-username-"] a')
            if not username_element:
                continue
                
            username = username_element.text.strip()
            username_url = "https://www.tiktok.com" + username_element['href'] if username_element.has_attr('href') else None
            
            # Extract comment text
            comment_text_element = comment_item.select_one('span[data-e2e^="comment-level-"] p')
            comment_text = comment_text_element.text.strip() if comment_text_element else ""
            
            # Extract likes count
            likes_element = comment_item.select_one('.css-1nd5cw-DivLikeContainer span')
            likes_count = 0
            if likes_element:
                try:
                    likes_count = int(likes_element.text.strip())
                except ValueError:
                    # Handle case where likes might be abbreviated (e.g., "1.2K")
                    likes_text = likes_element.text.strip()
                    if 'K' in likes_text:
                        likes_count = int(float(likes_text.replace('K', '')) * 1000)
            
            # Extract replies count
            replies_count = 0
            reply_text_element = comment_item.select_one('[aria-label^="Reply"]')
            if reply_text_element and reply_text_element.parent:
                # Look for nearby elements that might contain replies count
                for element in reply_text_element.parent.find_all('span'):
                    if element.text and element.text != 'Reply':
                        try:
                            # Check if it contains any digits
                            if re.search(r'\d', element.text):
                                replies_count = int(re.search(r'\d+', element.text).group())
                                break
                        except (ValueError, AttributeError):
                            pass
            
            # Extract date and time
            date_element = comment_item.select_one('.css-1lglotn-DivCommentSubContentWrapper span')
            date_text = date_element.text.strip() if date_element else ""
            
            # Convert relative date to ISO format (approximation)
            date_time = ""
            if date_text:
                current_date = datetime.now()
                if "hour" in date_text.lower():
                    hours = int(re.search(r'\d+', date_text).group()) if re.search(r'\d+', date_text) else 1
                    date_time = (current_date.replace(microsecond=0) - timedelta(hours=hours)).isoformat() + "Z"
                elif "day" in date_text.lower():
                    days = int(re.search(r'\d+', date_text).group()) if re.search(r'\d+', date_text) else 1
                    date_time = (current_date.replace(microsecond=0) - timedelta(days=days)).isoformat() + "Z"
                elif "min" in date_text.lower():
                    mins = int(re.search(r'\d+', date_text).group()) if re.search(r'\d+', date_text) else 1
                    date_time = (current_date.replace(microsecond=0) - timedelta(minutes=mins)).isoformat() + "Z"
                elif "-" in date_text:
                    # This looks like a month-day format (like "5-6")
                    # For simplicity, using current year
                    date_time = f"{current_date.year}-{date_text.replace('-', '-')}-00:00:00Z"
                else:
                    date_time = current_date.replace(microsecond=0).isoformat() + "Z"
            
            # Create comment dictionary
            comment_data = {
                'username': username,
                'username_url': username_url,
                'comment_text': comment_text,
                'likes/hearts': likes_count,
                'replies': replies_count,
                'date_time': date_time,
                'video_url': url
            }
            
            comments_data.append(comment_data)
    
    return comments_data


def read_source_code(file_path):
    """
    Read HTML source code from a file
    
    Args:
        file_path (str): Path to the file containing HTML source code
        
    Returns:
        str: HTML content as a string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return ""
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""

def save_comments_to_json(comments, output_file="tiktok_comments.json"):
    """
    Save scraped comments to a JSON file
    
    Args:
        comments (list): List of comment dictionaries
        output_file (str): Path to save the JSON output
    """
    try:
        with open(output_file, 'a+', encoding='utf-8') as file:
            json.dump(comments, file, indent=2, ensure_ascii=False)
        print(f"Comments successfully saved to {output_file}")
    except Exception as e:
        print(f"Error saving comments to file: {e}")


def press_tabs_on_screen(max_limit):

    for _ in range(0,max_limit):

        bot_functions.press_tab_key(25) 
        time.sleep(2) 

        while(True):

            if bot_functions.LocateImageOnScreen("./Screenshots/view.png") == True:
                bot_functions.ClickImageOnScreen("./Screenshots/view.png",1)
                pyautogui.moveTo(10,10)
            
            else: 
                break 

            time.sleep(2)

async def scraping_robot(browser):

    # File containing the HTML source code
    
    # Read the HTML content from the file
    # html_content = read_source_code(source_file) 
    # 

    maximum_limit_of_tab_key_presses = 3

    # print("TIKTOK COMMENTS SCRAPER \n \n")
    # print("Please open Google Chrome browser in a maximized window and make sure you are signed in to your TikTok account. After 10 seconds, the scraper will automatically start working on your browser.")
    # time.sleep(10)
    # source_code_downloader.open_close_inspect_element_window() 

    with open("videos.txt", "r", encoding="utf-8") as file:
        # Read the first line from the file
        urls = file.readlines()
    
    urls = [url.strip() for url in urls]

    for url in urls:
        print(f"Processing URL: {url}")
        # bot_functions.redirect_url(url)
        await browser.get(url)
        await asyncio.sleep(5)
        press_tabs_on_screen(maximum_limit_of_tab_key_presses)

        # html_code = source_code_downloader.download_source_code()
        html_code = await browser.page_source

        if html_code:
            # Scrape comments from the HTML content
            comments = scrap_tiktok_comments(html_code,url)

            # Print the number of comments found
            print(f"Found {len(comments)} comments")
            
            # Save comments to a JSON file
            save_comments_to_json(comments)
            
            # Display the first 3 comments (or all  if less than 3)
            print("\nSample comments:")
            for i, comment in enumerate(comments[:10]):
                print(f"\nComment {i+1}:")
                print(json.dumps(comment, indent=2, ensure_ascii=False))
        else:
            print("No HTML content to process. Check the source file.")
    
    # pyautogui.hotkey('ctrl', 'w')  # Close the current tab
