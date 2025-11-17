import json
import anthropic
from dotenv import load_dotenv
import os

def load_api_key():
    """
    Loads the API key from .env file
    
    Returns:
        str: API key or None if not found
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Get the API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not found in .env file!")
        print("\nPlease create a .env file with:")
        print("ANTHROPIC_API_KEY=your-api-key-here")
        return None
    
    return api_key


def convert_json_to_toon(json_file_path, toon_file_path):
    # Read the JSON file and write to the TOON file (use as a plain structured file)
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open(toon_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)

def give_me_reels_data_summary(toon_file_path, api_key):
    # Load TOON (treated as JSON)
    with open(toon_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Prepare the context for Claude Sonnet
    if isinstance(data, list) and len(data) > 15:
        content_sample = json.dumps(data[:10], ensure_ascii=False)
    else:
        content_sample = json.dumps(data, ensure_ascii=False)

    client = anthropic.Anthropic(api_key=api_key)
    system_prompt = ""  # Optional: briefly instruct model if needed
    user_prompt = (
        f"Here is Instagram reels data for a news account:\n{content_sample}\n"
        "Summarize the main user engagement and post content insights in 7-10 lines of plain text only."
    )

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=250,
        temperature=0.3,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.content

# Usage:
# API_KEY = load_api_key()

# convert_json_to_toon('Instagram_user_reels_data.json', 'Instagram_user_reels_data.toon')
# print(give_me_reels_data_summary('Instagram_user_reels_data.toon', api_key=API_KEY))
