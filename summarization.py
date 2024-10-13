import pandas as pd
import google.generativeai as genai
import os
import time
import math
import numpy as np

# Initialize the Gemini API
def initialize_gemini():
    # Configure the API key
    genai.configure(api_key="..")  # Replace with your actual API key 

    # Create the model with specified configuration
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "max_output_tokens": 2048,
        "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=(
            "I will give you news articles. Summarize each article so an average human being "
            "can read it in under 60 seconds. Also in a new line print the reliability score of this information "
            "(It should be a number between 1-100 with 1 being the lowest and 100 being the highest) and similarly "
            "add sentiment and the political bias."
        ),
    )

    # Start a chat session
    chat_session = model.start_chat(history=[])
    
    return chat_session

# Fetch response from Gemini, with retries and error handling
def get_gemini_response(chat_session, description, retries=3):
    # Check for NaN or empty values in the content
    if isinstance(description, float) and np.isnan(description):
        print("Content is NaN. Returning 'unavailable'.")
        return "unavailable"
    
    try:
        response = chat_session.send_message(description)
        return response
    except Exception as e:
        print(f"Error: {str(e)}")
        # Retry logic if there is an error
        if retries > 0:
            print("Retrying request after 10 seconds...")
            time.sleep(10)  # Retry delay
            return get_gemini_response(chat_session, description, retries - 1)
        else:
            print("Max retries reached. Returning 'unavailable'.")
            return "unavailable"

# Load the CSV file directly from the code
def load_news_data():
    # Load the CSV file (replace 'news_data.csv' with your actual file path)
    data = pd.read_csv('news_data.csv')
    return data[['title', 'description', 'content']]

# Append summarized content to CSV
def append_to_csv(summary):
    # Open the file in append mode without adding extra newlines
    with open('summarized_news_data.csv', 'a', newline='') as f:
        pd.DataFrame([summary], columns=['summary']).to_csv(f, header=False, index=False)

# Main script
def main():
    # Load the CSV data with titles and descriptions
    news_data = load_news_data()

    # Limit to the first 50 articles
    news_data = news_data.head(100)

    # Initialize Gemini API session
    chat_session = initialize_gemini()

    # Control the number of articles processed
    requests_made = 0
    total_articles = 50

    # Loop through the articles
    for index, row in news_data.iterrows():
        # Skip the 37th article and append NaN
        if index == 36:  # Since index is zero-based, index 36 corresponds to the 37th article
            print(f"Skipping the 37th news article and filling with NaN.")
            append_to_csv(np.nan)
            continue

        print(f"Processing News Article {index + 1}/{total_articles}")

        # Pass the content to Gemini for response
        gemini_response = get_gemini_response(chat_session, row['content'])

        if isinstance(gemini_response, str):
            # If the response is "unavailable" or an invalid response, use it as is
            summary = gemini_response
        elif hasattr(gemini_response, 'text'):
            # Parse the response if valid
            summary = gemini_response.text
        else:
            summary = "unavailable"

        # Append the summary to the CSV file after each article is processed
        append_to_csv(summary)

        # Display Gemini response in terminal
        print(f"Summary: {summary}")

        # Increment the requests counter
        requests_made += 1

        # After 15 requests, introduce a longer delay
        if requests_made >= 15:
            print("Processed 15 articles. Waiting for 60 seconds before continuing...")
            time.sleep(60)  # 60-second delay after every 15 requests
            requests_made = 0

        # Introduce a delay between each request to stay within the rate limits
        time.sleep(4)  # 4-second delay between requests (fits into 15 RPM)

if __name__ == "__main__":
    main()