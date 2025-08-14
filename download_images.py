import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Path to your HTML file
html_file = 'index.html'
# Directory to save images
output_dir = 'images'

os.makedirs(output_dir, exist_ok=True)

with open(html_file, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

img_tags = soup.find_all('img')
downloaded = set()

for img in img_tags:
    src = img.get('src')
    if not src or src.startswith('data:'):
        continue
    # Skip if already local
    if not (src.startswith('http://') or src.startswith('https://')):
        continue
    filename = os.path.basename(urlparse(src).path)
    filepath = os.path.join(output_dir, filename)
    if filename in downloaded or os.path.exists(filepath):
        continue
    try:
        print(f'Downloading {src}...')
        r = requests.get(src, timeout=10)
        r.raise_for_status()
        with open(filepath, 'wb') as out:
            out.write(r.content)
        downloaded.add(filename)
    except Exception as e:
        print(f'Failed to download {src}: {e}')

print('Download complete.')
