import json
import pytest
from gptgrep import find_chat_titles_and_dates_by_message

# Load sanitized test data
@pytest.fixture
def chat_data():
    with open('tests/test_data/sanitized_data.json', 'r') as file:
        data = json.load(file)
    return data

def test_find_chat_titles_and_dates_by_message(chat_data):
    search_term = "super-tight"
    context_depths = "0,0"
    results = find_chat_titles_and_dates_by_message(search_term, chat_data, context_depths)
    expected_titles = ["Great Day Ahead!"]
    assert all(item['title'] in expected_titles for item in results), "Titles do not match expected results"


