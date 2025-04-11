import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL with the 500 most commonly used words
url = "https://www.smart-words.org/500-most-commonly-used-english-words.html"

try:
    # Fetch the webpage content
    response = requests.get(url)
    response.raise_for_status()  # check for HTTP errors
    html = response.text
except Exception as e:
    print("Error fetching the webpage. Make sure you have internet access.", e)
    exit()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
list_items = soup.find_all('li')

# Initialize an empty list to store (frequency rank, word) tuples
words = []
rank = 500

# Process each <li> tag
for li in list_items:
    # Filter out elements that have a class attribute (navigation, empty items, etc.)
    if not li.has_attr('class'):
        text = li.get_text(strip=True)
        # Only consider non-empty text
        if text:
            words.append((rank, text))
            rank -= 1

# Create a Pandas DataFrame from the list
df = pd.DataFrame(words, columns=["Frequency_Rank", "Word"])

# Save the DataFrame to an Excel file
excel_filename = "500_common_words.xlsx"
df.to_excel(excel_filename, index=False)

print(f"Excel file '{excel_filename}' created successfully with {len(df)} words.")
