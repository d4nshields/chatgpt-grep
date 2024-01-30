#!/usr/bin/python3
import sys
import zipfile
import json
from datetime import datetime
import yaml

def find_chat_titles_and_dates_by_message(search_term, data):
    matches = []
    for chat in data:
        title = chat.get('title', '')
        update_time = chat.get('update_time', None)
        datetime_obj = datetime.fromtimestamp(update_time) if update_time else None
        for message_id, message_data in chat.get('mapping', {}).items():
            message_details = message_data.get('message', {})
            if not message_details:  # Skip if message details is None or empty
                continue
            message_content = message_details.get('content', {})
            parts = message_content.get('parts', [])
            message_text = ""
            for part in parts:
                if isinstance(part, dict):
                    if part.get('content_type') == 'image_asset_pointer':
                        continue  # Skip image entries
                    message_text += part.get('text', '')
                else:
                    message_text += part
            message_text = message_text.lower()
            if search_term.lower() in message_text:
                match = {
                    'datetime': datetime_obj,
                    'date': datetime_obj.strftime('%B %d, %Y %H:%M:%S') if datetime_obj else "Unknown time",
                    'title': title
                }
                matches.append(match)
                break
    # Sort by the datetime object
    matches.sort(reverse=True, key=lambda x: x['datetime'])
    # Remove the datetime object from final output
    for match in matches:
        del match['datetime']
    return matches

def main(zip_filepath, search_term):
    try:
        with zipfile.ZipFile(zip_filepath, 'r') as z:
            with z.open('conversations.json') as f:
                data = json.load(f)
        matches = find_chat_titles_and_dates_by_message(search_term, data)
        yaml_output = {
            search_term: matches
        }
        print(yaml.dump(yaml_output, default_flow_style=False))
    except FileNotFoundError:
        print(f"Error: The specified file '{zip_filepath}' for the path_to_export.zip argument could not be found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: gptgrep.py path_to_export.zip search_term")
    else:
        main(sys.argv[1], sys.argv[2])

