import requests

# List of image URLs
urls = [
    "https://v5.airtableusercontent.com/v3/u/33/33/...", # Add full URL list here
    # Add more URLs
]

# Directory where images will be saved
save_directory = "./downloaded_images/"

# Download each image
for i, url in enumerate(urls, start=1):
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"{save_directory}image_{i}.jpg", 'wb') as f:
            f.write(response.content)
        print(f"Downloaded image_{i}.jpg")
    else:
        print(f"Failed to download {url}")