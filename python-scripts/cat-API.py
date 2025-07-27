#########################################################################################################################################
# Make a script for getting pictures from API - https://developers.thecatapi.com/view-account/ylX4blBYT9FaoVd6OhvR?report=bOoHBz-8t
# Get 100 pictures:
#
# Based on type: static or gif put in folders in s3 bucket
#
# If "width" or "height" more than 1000 pixels picture should be archived by tar gz
# and
# If "width" or "height" more than 2000 pixels picture should be scanned by https://docs.scanii.com/
#
#########################################################################################################################################

# import os TODO: Uncomment if needed
import requests
import json # Added to handle JSON output properly
import os # Added to handle file paths
import boto3 # Added to handle AWS S3 operations

from urllib.parse import urlparse # Added to parse URLs

def get_images_urls():
    images = [] # Initialize an empty list to store images
    for i in range(10):
        response = requests.get("https://api.thecatapi.com/v1/images/search?limit=10")
        if response.status_code == 200:
            images.extend(response.json())  # Extend the images list with the new data
        else:
            print(f"Failed to fetch images: {response.status_code}")
    return images

# Function to download images and save them locally in folders based on their format
def download_images(images): 
    for image in images:
        url = image['url']
        
        # Extract file extension
        path = urlparse(url).path
        ext = os.path.splitext(path)[1].lower().strip('.')  # e.g., 'jpg', 'png'

        # Create folder if it doesn't exist
        folder = f"images/{ext}"
        os.makedirs(folder, exist_ok=True)

        # Create a filename from the URL
        filename = os.path.basename(path)
        filepath = os.path.join(folder, filename)

        # Download and save the image
        try:
            img_data = requests.get(url).content
            with open(filepath, 'wb') as f:
                f.write(img_data)
            print(f"Saved: {filepath}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")

def upload_to_s3(images, bucket_name, s3_directory="catAPI-folder"):
    s3 = boto3.client('s3')
    
    for image in images:
        url = image['url']
        path = urlparse(url).path
        filename = os.path.basename(path)
        ext = os.path.splitext(path)[1].lower().strip('.')
        
        # Create folder structure in S3
        s3_key = f"{s3_directory}/{ext}/{filename}"
        
        # Download the image
        img_data = requests.get(url).content
        
        # Upload to S3
        s3.put_object(Bucket=bucket_name, Key=s3_key, Body=img_data)
        print(f"Uploaded {filename} to S3 bucket {bucket_name} under {s3_key}")

imgs = get_images_urls()

# Save to a JSON file
# with open("output.json", "w") as f:
#     json.dump(imgs, f, indent=4)

# Download images into folders by format
# download_images(imgs)

# Upload to S3 bucket
upload_to_s3(imgs, "gorant-bucket")