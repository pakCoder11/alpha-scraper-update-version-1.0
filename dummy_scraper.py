from pandas.errors import PossibleDataLossError
import asyncio


def scrap_instagram_posts(scrape_comments, profile_url, num_posts): 
    """
    Scrapes Instagram posts from a given profile URL.

    :param scrape_comments: Whether to scrape comments (True/False).
    :param profile_url: The Instagram profile URL to scrape.
    :param num_posts: The number of posts to scrape.
    :return: A list of scraped posts.
    """

    print("---------------------------------------------")
    print("Scraping Instagram posts...")
    print("---------------------------------------------")

    print(f"The comments are { type(scrape_comments)}")
    print(f"The profile url is { type(profile_url)}")
    print(f"The number of posts to scrape is { type(num_posts)}")


async def write_comments_on_instagram_posts(login_dict, profiles, number_of_comments, comments_list):
    """Dummy async implementation that simulates writing comments."""
    print("---------------------------------------------")
    print("Dummy: Write Comments on Posts – started")
    print("---------------------------------------------")
    usernames = login_dict.get('usernames_list', [])
    print(f"Accounts: {usernames}")
    print(f"Profiles: {profiles}")
    print(f"Number of comments: {number_of_comments}")
    print(f"Comments list: {comments_list}")

    # Simulate some work with incremental logs
    total = max(1, min(number_of_comments, 5))
    for i in range(1, total + 1):
        print(f"Posting comment {i}/{total} ...")
        await asyncio.sleep(0.3)
    print("All comments posted in dummy mode.")


async def send_bulk_messages_to_followers(followers_list, messages_list, total_messages_to_send, time_gap): 
    """Dummy async implementation that simulates sending DMs."""
    print("---------------------------------------------")
    print("Dummy: Send Direct Messages – started")
    print("---------------------------------------------")
    print(f"Followers: {followers_list}")
    print(f"Messages: {messages_list}")
    print(f"Total messages to send: {total_messages_to_send}")
    print(f"Time gap (sec): {time_gap}")

    total = max(1, min(total_messages_to_send, 5))
    for i in range(1, total + 1):
        print(f"Sending message {i}/{total} ...")
        await asyncio.sleep(0.3)
    print("All messages sent in dummy mode.")
