import urllib.request, json, os

def download_logo(term, path):
    print(f"Downloading {term}...")
    try:
        # We can use simple DuckDuckGo image search to get standard recognizable logos, or reliable SVG icons.
        pass
    except Exception as e:
        print(e)

# Let's just use highly reliable raw github URLs for these!
urls = {
    'tving_logo.png': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/tving.png',
    'iqiyi_logo.png': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/iqiyi.png',
    'disney_logo.png': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/disneyplus.png'
}

for name, url in urls.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req).read()
        with open(name, 'wb') as f:
            f.write(data)
        print(f"Saved {name}: {len(data)} bytes")
    except Exception as e:
        print(f"Error {name}: {e}")

