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
#
# Script requires: 
#       SCANNII_API_KEY, SCANNII_API_SECRET to be setup as environment variables.
#       AWS credentials to be setup using `aws configure sso`
#
#########################################################################################################################################

import requests                     # Added to handle HTTP requests
import json                         # Added to handle JSON output properly
import os                           # Added to handle file paths, and environment variables
import boto3                        # Added to handle AWS S3 operations
import tarfile                      # Added to handle tar.gz archiving
from io import BytesIO              # Added to handle in-memory buffer

from urllib.parse import urlparse   # Added to parse URLs

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
def download_image(image): 
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

def upload_to_s3(image, bucket_name, s3_directory="catAPI-folder"):
    s3 = boto3.client('s3')
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

def archive_image(image):
    url = image['url']
    img_data = requests.get(url).content
    tar_buffer = BytesIO()
    
    with tarfile.open(fileobj=tar_buffer, mode='w:gz') as tar:
        info = tarfile.TarInfo(name=os.path.basename(url))
        info.size = len(img_data)
        tar.addfile(info, BytesIO(img_data))
    tar_buffer.seek(0)
    return tar_buffer.getvalue() # Returns a BytesIO object containing the tar.gz archive

def scan_image(image):
    url = image['url']
    img_data = requests.get(url).content

    # Load Scanii API credentials from environment variables
    SCANNII_API_KEY = os.environ.get("SCANNII_API_KEY")
    SCANNII_API_SECRET = os.environ.get("SCANNII_API_SECRET")

    # Scanii API call to scan the image
    response = requests.post("https://api-eu2.scanii.com/v2.2/files", auth=(SCANNII_API_KEY, SCANNII_API_SECRET), files={'file': img_data})
    print(response.json())

def upload_archive_to_s3(archive_bytes, image, bucket_name, s3_directory="catAPI-folder"):
    url = image['url']
    path = urlparse(url).path
    filename = os.path.basename(path) + ".tar.gz"
    ext = os.path.splitext(path)[1].lower().strip('.')
    s3_key = f"{s3_directory}/{ext}/{filename}"

    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Key=s3_key, Body=archive_bytes)
    print(f"Uploaded archive {filename} to S3 bucket {bucket_name} under {s3_key}")

# Main logic
imgs = get_images_urls()

for img in imgs:
    width = img['width']
    height = img['height']

    if width > 2000 or height > 2000:
        # Scan the image if dimensions exceed 2000 pixels
        scan_image(img)
    
    if width > 1000 or height > 1000:
        # Archive the image if dimensions exceed 1000 pixels
        archive = archive_image(img)
        upload_archive_to_s3(archive, img, "gorant-bucket")
    else:
        # Upload the image to S3 if dimensions are within limits
        upload_to_s3(img, "gorant-bucket")


# Save to a JSON file
# with open("output.json", "w") as f:
#     json.dump(imgs, f, indent=4)

# Download images into folders by format
# download_image(imgs)