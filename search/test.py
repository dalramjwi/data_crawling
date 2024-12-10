import requests
from bs4 import BeautifulSoup
import json

# URL for scraping
url = "https://trends24.in/korea/"
response = requests.get(url)
response.encoding = 'utf-8'  # Ensure UTF-8 encoding

soup = BeautifulSoup(response.text, "html.parser")

# Locate the main timeline container
timeline_container = soup.find(id="timeline-container")

# Extract data from each list container
trending_data = []
seen_keywords = set()  # Set to keep track of unique keywords

for list_container in timeline_container.find_all(class_="list-container"):
    for item in list_container.find_all("li"):
        trend_name = item.find("a").text
        tweet_count_tag = item.find("span", class_="tweet-count")
        tweet_count = tweet_count_tag.text if tweet_count_tag else "N/A"
        
        # Check if the keyword is already added to avoid duplicates
        if trend_name not in seen_keywords:
            trending_data.append({
                "keyword": trend_name,
                "tweet_count": tweet_count
            })
            seen_keywords.add(trend_name)  # Mark keyword as seen

# Save to JSON with UTF-8 encoding to prevent character issues
with open("trending_topics.json", "w", encoding="utf-8") as file:
    json.dump(trending_data, file, ensure_ascii=False, indent=4)

print("Data successfully saved to trending_topics.json")