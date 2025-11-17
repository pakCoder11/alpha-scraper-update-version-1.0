import pandas as pd
import os
from pathlib import Path 
import anthropic
# from langchain_anthropic import ChatAnthropic
# from langchain.schema import HumanMessage, SystemMessage
import json
from dotenv import load_dotenv
from datetime import datetime

def DataTransformationFunction(input_file, output_file, username_col, comment_text_col, video_url_col):
    """
    Reads an Excel file, processes comment sentiment using give_me_sentiment(),
    and outputs a new Excel file with sentiment results.

    Args:
        input_file (str): Path to input Excel file
        output_file (str): Path where output Excel file will be saved
        username_col (str): Column name for username
        comment_text_col (str): Column name for comment text
        video_url_col (str): Column name for video URL

    Returns:
        str: Path to output file if successful, None if failed
    """

    try:
        # Read Excel file
        df = pd.read_excel(input_file)

        # Check required columns exist
        missing_cols = [c for c in [username_col, comment_text_col, video_url_col] if c not in df.columns]
        if missing_cols:
            print(f"Error: Missing columns in Excel file: {missing_cols}")
            return None

        # Prepare new dataframe for output
        output_data = []
        print("Processing sentiments...")

        # Loop through each comment and analyze sentiment
        for index, row in df.iterrows():
            username = row[username_col]
            comment_text = row[comment_text_col]
            video_url = row[video_url_col]

            try:
                sentiment = give_me_sentiment(str(comment_text))  # Call AI sentiment function
            except Exception as e:
                print(f"Error processing sentiment for row {index}: {e}")
                sentiment = "Neutral"  # fallback value

            output_data.append({
                "username": username,
                "comment_text": comment_text,
                "sentiment": sentiment,
                "video_url": video_url
            })

        # Create output DataFrame
        output_df = pd.DataFrame(output_data, columns=["username", "comment_text", "sentiment", "video_url"])

        # Save to Excel
        output_df.to_excel(output_file, index=False)
        print(f"✅ Sentiment data successfully saved to: {output_file}")
        return output_file

    except Exception as e:
        print(f"Error in DataTransformationFunction: {e}")
        return None

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

def give_me_sentiment(text):
    """
    Analyzes the sentiment of the given text using Claude Sonnet 3.5 API.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        str: Sentiment classification - "Good", "Bad", or "Neutral"
    """
    
    # Load API key from .env file
    api_key = load_api_key()
    
    if not api_key:
        return None
    
    # Initialize the Anthropic client
    client = anthropic.Anthropic(api_key=api_key)
    
    try:
        # Create the message request
        message = client.messages.create(
            model="claude-3-opus-20240229",  # Claude 3 Opus - widely available
            max_tokens=120,
            messages=[
                {
                    "role": "user",
                    "content": f"""Analyze the sentiment of the following text and respond with ONLY one word: "Good", "Bad", or "Neutral". No explanation needed.

Text: "{text}"

Sentiment:"""
                }
            ]
        )
        
        # Extract the sentiment from the response
        # The content is a list of TextBlock objects
        sentiment_text = ""
        for block in message.content:
            if hasattr(block, 'text'):
                sentiment_text += block.text
        
        sentiment_text = sentiment_text.strip()
        
        # Normalize the response
        sentiment_lower = sentiment_text.lower()
        if 'good' in sentiment_lower or 'positive' in sentiment_lower:
            return "Good"
        elif 'bad' in sentiment_lower or 'negative' in sentiment_lower:
            return "Bad"
        else:
            return "Neutral"
            
    except Exception as e:
        print(f"Error analyzing sentiment: {str(e)}")
        return None


def dummy_ai_function():
    """
    Generate a lightweight analysis_report.md from available data without calling external AI.
    Prefers instagram_posts_comments.xlsx if present. Falls back to the first .xlsx/.json found.
    """
    load_dotenv()
    base_dir = Path(__file__).parent

    # Preferred file
    preferred_excel = base_dir / 'instagram_posts_comments.xlsx'

    target_file = None
    if preferred_excel.exists() and preferred_excel.stat().st_size > 0:
        target_file = preferred_excel
    else:
        # find the first available .xlsx or .json in base_dir
        for p in sorted(base_dir.iterdir()):
            if p.is_file() and p.suffix.lower() in {'.xlsx', '.json'} and p.name != 'analysis_report.md':
                target_file = p
                break

    analyzed_summary = "No suitable data file found to analyze."
    if target_file:
        try:
            if target_file.suffix.lower() == '.xlsx':
                df = pd.read_excel(target_file)
                cols = list(df.columns)
                row_count = len(df)
                # Simple keyword-like counts on text columns if present
                text_cols = [c for c in cols if 'comment' in c.lower() or 'text' in c.lower() or 'caption' in c.lower()]
                preview = df.head(10).fillna("").to_dict('records')
                analyzed_summary = f"File: {target_file.name}\nRows: {row_count}\nColumns: {cols}\nTextColumns: {text_cols}\nSample: {json.dumps(preview, ensure_ascii=False)[:1200]}"
            else:
                with open(target_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # Compute simple stats
                if isinstance(data, list):
                    row_count = len(data)
                    sample = data[:10]
                elif isinstance(data, dict):
                    row_count = len(data)
                    sample = dict(list(data.items())[:10])
                else:
                    row_count = 1
                    sample = data
                analyzed_summary = f"File: {target_file.name}\nType: JSON\nItems: {row_count}\nSample: {json.dumps(sample, ensure_ascii=False)[:1200]}"
        except Exception as e:
            analyzed_summary = f"Failed to parse {target_file.name}: {e}"

    # Build markdown report
    md = f"""# Analysis Report\n\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n## Overview\nA quick high-level summary generated locally without external AI calls.\n\n## Data Summary\n{analyzed_summary}\n\n## Highlights\n- Basic structure inspected.\n- This is a dummy report. Integrate AI later for deeper insights.\n\n## Next Steps\n- Connect Anthropic API and run full sentiment/topic analysis.\n- Expand metrics and charts as needed.\n"""

    out_path = base_dir / 'analysis_report.md'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(md)

    return str(out_path)

def setup_api_connection(): 
    pass


def perform_sentiment_analysis() -> None:
    """
    Perform sentiment analysis on Excel file data using Claude API and generate a markdown report.
    """
    """
        
    Raises:
        FileNotFoundError: If the specified file doesn't exist
        ValueError: If required columns are missing
    """

    file_path = "instagram_posts_comments.xlsx"  # Default file path
    
    # Load environment variables
    load_dotenv()
    
    # Check if file exists
    if not Path(file_path).exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Read Excel file
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        raise ValueError(f"Error reading Excel file: {e}")
    
    # Check required columns
    required_columns = ['username', 'comment_text', 'time_of_comment']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Clean data
    df = df.dropna(subset=['comment_text'])
    df = df[df['comment_text'].str.strip().astype(bool)]
    
    # Initialize Claude client
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    try:
        llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            temperature=0.1,
            max_tokens=4000,
            anthropic_api_key=api_key
        )
    except Exception as e:
        raise ConnectionError(f"Failed to initialize Claude client: {e}")
    
    # Prepare data for analysis
    sample_data = df.head(50).to_dict('records') if len(df) > 50 else df.to_dict('records')
    
    # Create prompt
    prompt = f"""
    Hi Claude,

    I need you to perform a comprehensive sentiment analysis on social media data. Here's the data sample:

    {json.dumps(sample_data, indent=2)}

    Please analyze this data and provide:

    1. SENTIMENT DISTRIBUTION:
       - Count and percentage of positive, negative, and neutral sentiments
       - Overall sentiment score/trend

    2. TOP POSITIVE USERS:
       - At least 5 usernames with the most positive feedback
       - Brief explanation of why their feedback is positive
       
    4. CONTENT ANALYSIS:
       - Main topics and discussions people are having
       - What people are thinking about the subject matter

    5. KEYWORD EXTRACTION:
       - List of 15-20 most frequent and relevant keywords
       - Categorized by sentiment if possible
       - Include frequency or importance score

    6. MARKETING INSIGHTS:
       - Recommendations for content strategy based on the analysis
       - Suggestions for engagement and community building

    Please provide the analysis in a structured, markdown-friendly format with clear sections.
    Be specific and data-driven in your insights.
    """
    
    try:
        # Call Claude API
        response = llm.invoke([
            SystemMessage(content="You are an expert data analyst specializing in sentiment analysis and social media analytics. Provide detailed, actionable insights."),
            HumanMessage(content=prompt)
        ])
        
        analysis_result = response.content
        
        # Generate markdown report
        md_content = f"""# Sentiment Analysis Report

## Dataset Overview
- **Total Records**: {len(df)}
- **Date Range**: {df['time_of_comment'].min()} to {df['time_of_comment'].max()}
- **Unique Users**: {df['username'].nunique()}

## Analysis Results

{analysis_result}

## Data Summary
- **Records Analyzed**: {len(df)}
- **Analysis Date**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Source File**: {file_path}

*This report was generated automatically using Claude AI sentiment analysis.*
"""
        
        # Save report
        output_file = "sentiment_analysis_report.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"✅ Analysis completed successfully!")
        print(f"📊 Report saved as: {output_file}")
        print(f"📋 Total records analyzed: {len(df)}")
        
    except Exception as e:
        raise Exception(f"Error during API call or analysis: {e}")
        
# Example usage:
# if __name__ == "__main__":
    # DataTransformationFunction("sentiment_check.xlsx", "Tiktok_video_data_analysis.xlsx", "username", "comment_text", "video_url")