import requests
import csv
import re
from datetime import datetime

url = "https://instagram-scraper-api2.p.rapidapi.com/v1/hashtag"

headers = {
    "x-rapidapi-key": "1d162e108amsh73fd4b7e6782dd4p12cbdejsn349e38f3955c",
    "x-rapidapi-host": "instagram-scraper-api2.p.rapidapi.com"
}

hashtags = ["trending", "hot", "latest", "new", "viral", "trend"]
unique_posts = set()
posts_data = []


def extract_hashtags(text):
    return re.findall(r'#(\w+)', text)


def remove_hashtags(text):
    return re.sub(r'#\w+', '', text).strip()


for hashtag in hashtags:
    querystring = {"hashtag": hashtag}
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    if 'data' in data and 'items' in data['data']:
        for item in data['data']['items']:
            post_id = item['id']
            if post_id not in unique_posts:
                unique_posts.add(post_id)
                caption = item['caption']['text'] if item.get('caption') and 'text' in item['caption'] else ''
                extracted_hashtags = extract_hashtags(caption)
                clean_caption = remove_hashtags(caption)
                timestamp = datetime.fromtimestamp(item['caption']['created_at']).strftime(
                    '%Y-%m-%d %H:%M:%S') if item.get('caption') and 'created_at' in item['caption'] else ''
                likes = item.get('like_count', 0)
                comments = item.get('comment_count', 0)
                posts_data.append(
                    [post_id, clean_caption, timestamp, likes, comments, hashtag, ', '.join(extracted_hashtags)])

    print(f"Results for #{hashtag}: {len(data['data']['items']) if 'data' in data and 'items' in data['data'] else 0}")

# Save to CSV
with open('instagram_posts.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Post ID', 'Caption', 'Timestamp', 'Likes', 'Comments', 'Search Hashtag', 'Post Hashtags'])
    writer.writerows(posts_data)

print(f"\nTotal unique posts collected: {len(unique_posts)}")