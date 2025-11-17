import json
import pandas as pd
import re
import os
import numpy as np
import math

def append_dict_to_json(data, filename):
    """
    Appends a dictionary or list of dictionaries to a JSON file.
    Creates the file if it does not exist.
    """
    # Ensure data is a list of dicts
    if isinstance(data, dict):
        data = [data]

    # If file does not exist, create it with an empty list
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([], f)

    # Read existing data
    with open(filename, 'r', encoding='utf-8') as f:
        try:
            existing = json.load(f)
        except json.JSONDecodeError:
            existing = []

    # Append new data
    existing.extend(data)

    # Write back to file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

def clean_data(df):
    # Drop rows where all values are null
    cleaned_df = df.dropna()

    return cleaned_df

    # Save the cleaned DataFrame to a file
    # cleaned_df.to_excel(output_file, index=False)  # Change the filename and format as needed

def store_to_json(dict_data, file_path):
    # Open the file in append mode
    with open(file_path, 'a') as f:
        # Use json.dump to write the dictionary to the file
        json.dump(dict_data, f)
        # Write a newline character after each dictionary
        f.write('\n')

def read_dicts_from_json(file_path):
    dicts = []
    with open(file_path, 'r') as f:
        for line in f:
            dicts.append(json.loads(line))
    return dicts


def json_to_excel(json_file_path, excel_file_path):
    # Read the JSON file into a DataFrame
    df = pd.read_json(json_file_path, lines=True)

    # Write the DataFrame to an Excel file
    df.to_excel(excel_file_path, index=False)

def data_storage(main_list):
    # Convert list of lists into a single list
    single_list = [item for sublist in main_list for item in sublist]
    
    # Create a DataFrame from the list
    df = pd.DataFrame(single_list)
    # main_df = clean_data(df)
    
    # Save the DataFrame to an Excel file
    df.to_excel('insta-viral-posts-data.xlsx', index=False)

def save_data_to_excel(input_file_name,output_file_name):

    # Check if data.json exists and is not empty
    if os.path.exists(input_file_name) and os.path.getsize(input_file_name) > 0:
        with open(input_file_name, 'r') as f:
            data = [json.loads(line) for line in f.readlines()]

        # Create a DataFrame from the data
        df = pd.DataFrame(data)

        # Save the DataFrame to an Excel file
        df.to_excel(output_file_name, index=False)

        # Delete the original data.json file
        os.remove(input_file_name)

    else:
        print(f"{input_file_name} does not exist or is empty.")


# Add this custom JSON encoder class
class NaNEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, float) and np.isnan(obj):
            return None
        return super().default(obj)

def replace_nan_with_zero(input_file, output_file):
    # Load JSON with special handling for NaN
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f, parse_constant=lambda x: 0 if x == 'NaN' else x)

    # Replace any NaN values that slipped through
    def fix_values(obj):
        if isinstance(obj, dict):
            return {k: fix_values(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [fix_values(v) for v in obj]
        elif isinstance(obj, float) and math.isnan(obj):
            return 0
        return obj

    fixed_data = fix_values(data)

    # Save the cleaned JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(fixed_data, f, indent=2)

    return fixed_data


def excel_to_json(excel_file_path, json_file_path):
    """
    Converts an Excel file to a JSON file in the format: [ {}, {}, ... ]
    Each dictionary uses column names as keys.
    """
    df = pd.read_excel(excel_file_path)
    # Convert DataFrame to records
    data_list = df.to_dict(orient='records')
    # Use custom encoder to handle NaN values
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2, cls=NaNEncoder)
    replace_nan_with_zero(json_file_path, json_file_path)

def url_cleaners():
    # Define a regular expression pattern for URLs
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    # Open the input file and the output file
    with open('data.txt', 'r', encoding='utf-8') as infile, open('output.txt', 'w',encoding='utf-8') as outfile:
        for line in infile:
            # If the line is blank, write 'NaN' to the output file
            if line.strip() == '':
                outfile.write('NaN\n')
            else:
                # Remove URLs from the line and write it to the output file
                cleaned_line = re.sub(url_pattern, '', line)
                outfile.write(cleaned_line)


def process_social_links():
    # Read the Excel file
    df = pd.read_excel('New Arrival main file.xlsx')

    # Create new columns for each social media platform
    platforms = ['Instagram', 'Linkedin', 'Youtube', 'TikTok', 'Facebook', 'Twitter', 'Snapchat']
    for platform in platforms:
        df[platform + ' URL'] = None

    # Process the 'Social Links' column
    for i, link in enumerate(df['Social Links']):
        if pd.isnull(link):
            continue
        for platform in platforms:
            if platform.lower() in link.lower():
                df.loc[i, platform + ' URL'] = link

    # Save the DataFrame to a new Excel file
    df.to_excel('output.xlsx', index=False)

# Call the function
# process_social_links()
# Call the function
# Call the function
# url_cleaner()
# D = read_dicts_from_json('data.json')
# data_storage(D)
# url_cleaners() #clean the txt 
# process_social_links()
# save_data_to_excel('Instagram Business Data1.xlsx') 
# excel_to_json('instagram_posts_with_likes.xlsx','test_nan_data.json')
# save_data_to_excel('data.json','profile_followers_data.xlsx') 
# excel_to_json('profile_followers_data.xlsx','profile_followers_data.json')