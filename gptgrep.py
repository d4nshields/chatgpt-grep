#!/usr/bin/python3
import sys
import zipfile
import json
from datetime import datetime
import yaml
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Search for terms in ChatGPT data and retrieve contextual conversation history.')
    parser.add_argument('zip_filepath', type=str, help='Path to the zip file containing the export.')
    parser.add_argument('search_term', type=str, help='Term to search within the conversations.')
    parser.add_argument('--context', type=str, default='0,0', help='Comma-separated values indicating the number of parent and child context nodes to include. Format: n,m')
    return parser.parse_args()

def get_message_text(message):
    """Extract text from a message."""
    # Check if 'parts' exists in 'content' and if not, return an empty string
    parts = message.get('content', {}).get('parts', [])
    return " ".join(part if isinstance(part, str) else part.get('text', '') for part in parts)

def collect_context(mapping, message_id, parent_depth, child_depth):
    parent_context = []
    child_context = []
    # Collect parent context
    current_id = message_id
    while current_id in mapping and 'parent' in mapping[current_id] and parent_depth > 0:
        current_id = mapping[current_id]['parent']
        if current_id in mapping:
            message = mapping[current_id].get('message')
            if message:
                parent_context.insert(0, get_message_text(message))  # Insert at the beginning to reverse order
        parent_depth -= 1

    # Collect child context
    def collect_children(current_id, depth):
        if depth == 0 or current_id not in mapping or 'children' not in mapping[current_id]:
            return
        for child_id in mapping[current_id]['children']:
            message = mapping[child_id].get('message')
            if message:
                child_context.append(get_message_text(message))
            collect_children(child_id, depth - 1)

    collect_children(message_id, child_depth)

    return parent_context, child_context

def find_chat_titles_and_dates_by_message(search_term, data, context_depths):
    matches = []
    parent_depth, child_depth = context_depths
    for chat in data:
        title = chat.get('title', '')
        update_time = chat.get('update_time', None)
        datetime_obj = datetime.fromtimestamp(update_time) if update_time else None
        mapping = chat.get('mapping', {})
        for message_id, message_data in mapping.items():
            message_details = message_data.get('message', {})
            if not message_details:  # Skip if message details are None or empty
                continue
            message_text = get_message_text(message_details)
            if search_term.lower() in message_text.lower():
                parent_context, child_context = collect_context(mapping, message_id, parent_depth, child_depth)
                formatted_time = datetime_obj.strftime('%B %d, %Y %H:%M:%S') if datetime_obj else "Unknown time"
                match = {
                    'date': formatted_time,
                    'title': title,
                    'context': {
                        'prev': parent_context,
                        'match': message_text,  # Ensure matched message is always included
                        'next': child_context
                    }
                }
                matches.append(match)
                break
 #   matches.sort(reverse=True, key=lambda x: x['date'])
    return matches

def main():
    args = parse_arguments()
    context_depths = [int(x) for x in args.context.split(',')]
    try:
        with zipfile.ZipFile(args.zip_filepath, 'r') as z:
            with z.open('conversations.json') as f:
                data = json.load(f)
        matches = find_chat_titles_and_dates_by_message(args.search_term, data, context_depths)
        yaml_output = {args.search_term: matches}
        print(yaml.dump(yaml_output, default_flow_style=False, sort_keys=False))
    except FileNotFoundError:
        print(f"Error: The specified file '{args.zip_filepath}' for the path_to_export.zip argument could not be found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: gptgrep.py path_to_export.zip search_term")
    else:
        main()
