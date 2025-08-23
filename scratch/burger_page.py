import json
import csv
from datetime import datetime
import pytz

# Load JSON data
with open("careem_burger_response.json", "r", encoding="utf-8") as f:
    data = json.load(f)

output_file = "careem_burger_image_urls.csv"
fieldnames = ["surface", "placement_type", "image_url", "scrape_timestamp", "tz"]

tz = pytz.timezone("Asia/Dubai")
now = datetime.now(tz)
scrape_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
tz_str = str(now.tzinfo)

rows = []

def find_image_urls(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            # For lists of image URLs
            if k == "image_urls" and isinstance(v, list):
                for url in v:
                    rows.append({
                        "surface": "careem burger",
                        "placement_type": "burger modules",
                        "image_url": url,
                        "scrape_timestamp": scrape_timestamp,
                        "tz": tz_str
                    })
            # For single image_url fields
            elif k == "image_url" and isinstance(v, str):
                rows.append({
                    "surface": "careem burger",
                    "placement_type": "burger modules",
                    "image_url": v,
                    "scrape_timestamp": scrape_timestamp,
                    "tz": tz_str
                })
            else:
                find_image_urls(v)
    elif isinstance(obj, list):
        for item in obj:
            find_image_urls(item)

find_image_urls(data)

with open(output_file, "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Extracted {len(rows)} image URLs to {output_file}")