# =======================================================
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
from pathlib import Path

import source_code_downloader 

# ======================================================= 
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
    comment_wrappers = soup.find_all('div', class_=lambda x: x and 'DivCommentObjectWrapper' in x)

    print(f"The comment_wrappers are {len(comment_wrappers)}")

    comments_data = []
    
    for wrapper in comment_wrappers:
        # Find all comment items within the wrapper
        # comment_items = wrapper.find_all('div', class_='css-1gstnae-DivCommentItemWrapper') 
        comment_items = wrapper.find_all('div', class_=lambda x: x and 'DivCommentItemWrapper' in x)
        
        for comment_item in comment_items:
            # Extract username and profile link
            username_element = comment_item.select_one('[data-e2e^="comment-username-"] a')
            if not username_element:
                continue
                
            username = username_element.text.strip()
            username_url = "https://www.tiktok.com" + username_element['href'] if username_element.has_attr('href') else None
            
            # Extract comment text  
            try:

                comment_text_element = comment_item.select_one('div[data-e2e="comment-level-1"]')
                comment_text = comment_text_element.span.text

            except Exception as e:
                comment_text = ""

            # Extract likes count
            likes_element = comment_item.select_one('div[class*="DivLikeContainer"]')
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
            date_element = comment_item.select_one('div[class*="DivCommentSubContentWrapper"]')
            date_text = date_element.span.text.strip() if date_element else ""
            
            # Create comment dictionary
            comment_data = {
                'username_url': username_url,
                'username': username,
                'comment_text': comment_text,
                'likes/hearts': likes_count,
                'replies': replies_count,
                'date_time': date_text,
                'video_url': url
            }

            data_store.store_to_json(comment_data,'tiktok_comments_data.json')
            comments_data.append(comment_data)
    
    return comments_data

def click_on_all_replies_buttons():

    bot_functions.please_wait("./Screenshots/TikTok/comment.png") 
    bot_functions.ClickImageOnScreen("./Screenshots/TikTok/comment.png",1) 
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.press('enter') 
    time.sleep(2)

    bot_functions.ClickImageOnScreen("./Screenshots/TikTok/view.png",1) 
    time.sleep(2)
    counter = 0

    while(True): 

        bot_functions.ClickImageOnScreen("./Screenshots/TikTok/heart.png",1) 
        time.sleep(2)
        bot_functions.press_tab_key(15)
        time.sleep(2)
        bot_functions.ClickImageOnScreen("./Screenshots/TikTok/view.png",1) 
        time.sleep(3)

        counter += 1 

        if counter == 10:
            break

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

async def click_element_by_xpath(driver, xpath):
    try:
        element = await driver.find_element(By.XPATH, xpath)
        await element.click()
    except Exception as e:
        print(f"Error clicking element with XPath {xpath}: {e}")

def DataSavingContainer(): 
    
    try:
        data_store.save_data_to_excel("tiktok_comments_data.json","Tiktok_comments_data.xlsx") 
        data_store.excel_to_json("Tiktok_comments_data.xlsx","Tiktok_comments_data.json")    
    
    except FileNotFoundError: 
        print("File is not found ERROR_")

def DataRemovingContainer(): 

    # Delete output artifacts safely with clear messages
    root = Path(__file__).resolve().parent
    targets = [ 
        "tiktok_comments_data.json",
        "Tiktok_comments_data.json",
        "Tiktok_comments_data.xlsx",
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


# Define the asynchronous scraper function
async def scrape_comments_data_from_Tiktok_video(video_url):

    DataRemovingContainer() 

    xpaths_view_replies = [
    # --- Match 'View X replies' (any number) ---
    "//div[contains(@class,'DivViewRepliesContainer')]//span[contains(text(),'View') and contains(text(),'repl')]",
    "//span[contains(text(),'View') and contains(text(),'repl')]",
    "//span[matches(text(), 'View\\s+\\d+\\s+repl', 'i')]",  # advanced regex (if supported)

    # --- Match 'View replies' (no number) ---
    "//span[normalize-space(text())='View replies']",
    "//div[contains(@class,'DivViewRepliesContainer')]//span[contains(text(),'View replies')]",

    # --- Match 'View more replies' or 'More replies' ---
    "//span[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'more repl')]",
    "//div[contains(@class,'DivViewRepliesContainer')]//span[contains(text(),'More repl')]",

    # --- Match just 'Reply' (single reply button) ---
    "//span[normalize-space(text())='Reply']",
    "//button[contains(text(),'Reply')]",
    "//div//*[contains(text(),'Reply')]",

    # --- General fallback for any span containing 'repl' text ---
    "//span[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'repl')]",
    "//div[contains(@class,'DivViewRepliesContainer')]//*[contains(text(),'repl')]",

    # --- SVG-based parent (if text is missing or replaced by icon) ---
    "//div[contains(@class,'DivViewRepliesContainer')]//*[name()='svg']",
    "//div[contains(@class,'DivViewRepliesContainer')]",

    # --- Dynamic catch-all for text variations ---
    "//*[contains(text(),'View') and contains(text(),'repl')]",
    "//*[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'view repl')]",
    "//*[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'reply')]"
    ]

    cross_button_xpaths = [
    # --- By class names ---
    "//div[contains(@class,'DivXMarkWrapper')]",
    "//div[contains(@class,'e1jppm6i4')]",
    "//div[contains(@class,'css-2ldkve-5e6d46e3')]",

    # --- Target SVG directly ---
    "//div[contains(@class,'DivXMarkWrapper')]//svg",
    "//div[contains(@class,'DivXMarkWrapper')]//*[name()='svg']",
    "//svg[@fill='currentColor' and @viewBox='0 0 48 48']",

    # --- Target <path> inside SVG ---
    "//path[contains(@d,'21.1718 23.9999')]",
    "//svg//*[name()='path' and contains(@d,'21.1718')]",

    # --- Relative / hierarchical ---
    "//div[contains(@class,'DivXMarkWrapper')]/child::*[name()='svg']",
    "(.//div[contains(@class,'DivXMarkWrapper')])[1]",
    "(//div[contains(@class,'e1jppm6i4')]//*[name()='svg'])[1]",

    # --- Generic fallbacks ---
    "//svg//*[contains(@d,'L10.2931')]",
    "//div[.//*[name()='svg']]"
    ]
    counter = 0
    options = webdriver.ChromeOptions() 
    options.add_argument("--incognito")

    async with webdriver.Chrome(options=options) as browser:
        try:
                # Open the target website

                await browser.get(video_url,wait_load=False)
                await asyncio.sleep(7)  # Wait for the page to load

                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.press('tab') 

                # time.sleep(60)

                await press_view_buttons_on_screen(browser,cross_button_xpaths)
                await asyncio.sleep(2.0)  # Wait for the page to load after scrolling
                await click_element_by_xpath(browser, "//button[contains(@aria-label,'Read or add comments')]")
                
                click_on_all_replies_buttons()

                html_content = await browser.page_source
                await asyncio.sleep(2)
                comments_data_list = extract_comments(html_content,video_url)

                for comment_data in comments_data_list:
                    print(comment_data)

        except Exception as e:
            # Print any errors encountered during scraping
            print(f"Error scraping : {e}")
    
    DataSavingContainer()

async def scrape_comments_from_Tiktok_video_urls(video_urls):

    # this will scrape the data from Bulk videos ... 
    DataRemovingContainer()
    for video_url in video_urls:
        await scrape_comments_data_from_Tiktok_video(video_url)
    DataSavingContainer()

def scrape_comments_from_Titkok_video_using_custom_mode(video_url): 
    DataRemovingContainer()

    # code here ... 
    print("Scraping Process Starts/_ ...") 
    time.sleep(45) 

    click_on_all_replies_buttons()
    source_code_downloader.open_close_inspect_element_window()
    time.sleep(1)
    html_source_code = source_code_downloader.copy_code_using_inspect_element()
    comments_data_list = extract_comments(html_source_code,video_url)
    print(f"The scraped comments data is {comments_data_list}")
    source_code_downloader.open_close_inspect_element_window()
    time.sleep(1)
    pyautogui.hotkey('alt','f4')

    DataSavingContainer()

# Example usage:
if __name__ == "__main__":
    scrape_comments_from_Titkok_video_using_custom_mode("video_url_heere")

    # ================================================
    # OLD CODE ...
    # ================================================


    # print("Scraping Process Starts/_ ...")
    # time.sleep(7) 
    # click_on_all_replies_buttons()
    # with open("tiktok_search.html","r",encoding="utf-8") as file: 
        # html_source = file.read()

    # data = extract_comments(html_source,"url")


    # video_urls = ["https://www.tiktok.com/@chinese_artist176/video/7507673491211029803?is_from_webapp=1","https://www.tiktok.com/@ali.raza.11/video/7558381141565115666?is_from_webapp=1","https://www.tiktok.com/@ayesha.siddiqa974/video/7569606810773032214?is_from_webapp=1"]
    # asyncio.run(scrape_comments_from_Tiktok_video_urls(video_urls))
    # asyncio.run(scrape_comments_data_from_Tiktok_video("https://www.tiktok.com/@chinese_artist176/video/7507673491211029803?is_from_webapp=1"))
    # with open('tiktok_comments.html', 'r', encoding='utf-8') as file:
        # source_code = file.read()
    # list_ = extract_comments(source_code,"test_url") 
    # print(list_)