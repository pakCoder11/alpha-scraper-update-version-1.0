from selenium_driverless import webdriver
import asyncio
from multiprocessing import Pool
from math import ceil
from bs4 import BeautifulSoup
from selenium_driverless.types.by import By
import pyautogui
import bot_functions

async def scroll_down_all_pages(browser):

    element = await browser.find_element(By.XPATH, "//span[contains(text(), 'All')]")
    await element.click()  # Click on the "Videos" tab 
    limit = 0

    while(True): 

        bot_functions.press_down_keys(75)
        await asyncio.sleep(2.0)  # Wait for the page to load after scrolling
        next_btn = await browser.find_element(By.XPATH, "//span[contains(text(), 'Next')]")

        if next_btn:
            await next_btn.click()  # Click on the "Next" button
            html_content = await browser.page_source
            
        else:

            if limit > 10:
                break

async def scroll_down_all_videos(browser,limit):

    element = await browser.find_element(By.XPATH, "//span[contains(text(), 'Videos')]")
    await element.click()  # Click on the "Videos" tab

    await asyncio.sleep(2.0)  # Wait for the page to load after clicking 
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')

    for i in range(limit): 

        bot_functions.press_down_keys(100) 
        await asyncio.sleep(2.0)  # Wait for the page to load after scrolling
        body = await browser.find_element(By.TAG_NAME, 'body')

        try: 
            element = await browser.find_element(By.XPATH, "//span[contains(text(), 'More results')]")
            await element.click()  # Click on the "More results" button
        
        except Exception as e: 
            print(e)

# Define the asynchronous scraper function
async def async_scraper():
    # Use a headless Chrome browser for scraping 

    options = webdriver.ChromeOptions() 
    options.add_argument("--incognito")

    # options.add_argument('--headless')  # Run in headless mode

    async with webdriver.Chrome(options=options) as browser:
            try:
                # Open the target website
                await browser.get(url="https://www.facebook.com/groups/1806350770218584/user/61583468674869/")
                await asyncio.sleep(4)  # Wait for the page to load
                html_content = await browser.page_source 
                await asyncio.sleep(20)  # Wait for the page to load

                with open('tiktok_search.html', 'w', encoding='utf-8') as file:
                    file.write(html_content)
            except Exception as e:
                # Print any errors encountered during scraping
                print(f"Error scraping : {e}")

# Wrapper for running the async scraper in a process
def scraper_wrapper(url_list):
    # Run the asynchronous scraper
    asyncio.run(async_scraper(url_list))

def read_links_from_file(file_path):
    # Read URLs from a file and return as a list
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

# Function to divide the URL list into chunks
def divide_urls(url_list, num_chunks):
    # Calculate the size of each chunk
    chunk_size = ceil(len(url_list) / num_chunks)
    # Divide the list into chunks
    return [url_list[i:i + chunk_size] for i in range(0, len(url_list), chunk_size)]

if __name__ == "__main__":
    # Read the list of URLs to scrape from a file

    for _ in range(0,10):
        asyncio.run(async_scraper())
        break
