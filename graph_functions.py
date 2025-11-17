import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

def visualize_instagram_user_reels_data(file_path):
    # Load Excel data
    df = pd.read_excel(file_path)

    # Detect username for captions
    username = df['username'].iloc[0] if 'username' in df.columns else "UnknownUser"

    # Ensure graphs directory exists
    graphs_dir = "graphs"
    os.makedirs(graphs_dir, exist_ok=True)

    # 1. Likes Distribution (Histogram & BoxPlot)
    plt.figure(figsize=(8,5))
    sns.histplot(df['likes_count'], bins=10, color='skyblue', kde=True)
    plt.title(f'Distribution of Likes on Reels for {username}')
    plt.xlabel('Likes Count')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(f"{graphs_dir}/likes_histogram.png")
    plt.close()

    plt.figure(figsize=(8,5))
    sns.boxplot(y=df['likes_count'], color='lightgreen')
    plt.title(f'Likes Count Spread for {username}')
    plt.ylabel('Likes Count')
    plt.tight_layout()
    plt.savefig(f"{graphs_dir}/likes_boxplot.png")
    plt.close()

    # 2. Word Cloud for Reel Captions
    captions_text = ' '.join(str(caption) for caption in df['reel_caption'].dropna())
    wc = WordCloud(width=800, height=400, background_color='white').generate(captions_text)
    plt.figure(figsize=(10,6))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Frequent Words in Captions for {username}')
    plt.savefig(f"{graphs_dir}/captions_wordcloud.png")
    plt.close()

    # 3. Hashtag Frequency Bar Chart
    hashtags_series = df['hashtags'].dropna().str.split()
    hashtag_flat = [tag for sublist in hashtags_series for tag in sublist]
    hashtag_freq = pd.Series(hashtag_flat).value_counts().head(10)
    plt.figure(figsize=(8,5))
    sns.barplot(x=hashtag_freq.values, y=hashtag_freq.index, palette='mako')
    plt.title(f'Top 10 Hashtags Used by {username}')
    plt.xlabel('Frequency')
    plt.ylabel('Hashtag')
    plt.tight_layout()
    plt.savefig(f"{graphs_dir}/hashtags_barchart.png")
    plt.close()

    # 4. Account Activity (Number of Posts over Time)
    if 'system_time' in df.columns:
        post_dates = pd.to_datetime(df['system_time'], errors='coerce')
        plt.figure(figsize=(8,5))
        post_dates.value_counts().sort_index().plot(kind='bar', color='coral')
        plt.title(f'Posting Activity Over Time for {username}')
        plt.xlabel('Date')
        plt.ylabel('Number of Posts')
        plt.tight_layout()
        plt.savefig(f"{graphs_dir}/activity_bar.png")
        plt.close()

    print(f"Graphs saved in '{graphs_dir}' folder.")

# Usage example:
# visualize_instagram_user_reels_data('Instagram_user_reels_data.xlsx')
