import json
import csv
from datetime import datetime
import pytz

# Load JSON data
with open("careem_home_response.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Prepare output CSV
output_file = "careem_food_home_image_urls.csv"
fieldnames = ["surface", "placement_type", "image_url", "scrape_timestamp", "tz"]

# Timezone setup
tz = pytz.timezone("Asia/Dubai")
now = datetime.now(tz)
scrape_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
tz_str = str(now.tzinfo)

rows = []

def find_image_urls(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "image_urls" and isinstance(v, list):
                for url in v:
                    rows.append({
                        "surface": "careem food home",
                        "placement_type": "food homepage modules",
                        "image_url": url,
                        "scrape_timestamp": scrape_timestamp,
                        "tz": tz_str
                    })
            else:
                find_image_urls(v)
    elif isinstance(obj, list):
        for item in obj:
            find_image_urls(item)

find_image_urls(data)

# Write to CSV
with open(output_file, "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Extracted {len(rows)} image URLs to {output_file}")