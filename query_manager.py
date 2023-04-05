import json

draft_summary = "your_draft_summary_here"  # Replace with your actual draft_summary
lines = ["query1", "query2", "query3"]  # Replace with your actual queries

custom_texts = [
    f"Continue {draft_summary} developing the concept for {{line}}. Please write a detailed text of at least 55 words and provide an example of at least 60 words.",
    f"Elaborate further on the concept of {{line}} in the context of {draft_summary}. Write a comprehensive passage with a minimum of 55 words and include an example that is at least 60 words long.",
    f"Expand upon {draft_summary} by diving deeper into the idea of {{line}}. Craft a descriptive passage of at least 55 words and support it with an illustrative example consisting of a minimum of 60 words.",
]

query_data = []

for line in lines:
    line = line.strip()
    query_data.append({"line": line, "custom_texts": [text.format(line=line) for text in custom_texts]})

with open("queries.json", "w") as f:
    json.dump(query_data, f)
