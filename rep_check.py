from collections import Counter
import json

with open("individual_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract all titles
titles = [article["title"] for article in data if "title" in article]

# Count occurrences of each title
title_counts = Counter(titles)

# Find and print duplicates
duplicates = {title: count for title, count in title_counts.items() if count > 1}

counter = 0

if duplicates:
    print("Duplicate titles found:")
    for title, count in duplicates.items():
        counter += 1
        print(f"- \"{title}\" appears {count} times")
else:
    print("No duplicate titles found.")

print(counter)
