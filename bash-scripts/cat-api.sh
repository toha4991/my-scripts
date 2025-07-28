#!/bin/bash

# Requirements:
# - curl
# - jq
# - aws CLI
# - ImageMagick (for `identify`)
# - tar
# - Environment variables: SCANNII_API_KEY, SCANNII_API_SECRET

BUCKET="gorant-bucket"
S3_PREFIX="catAPI-folder"
TMP_DIR="./catapi_tmp"
mkdir -p "$TMP_DIR"

# Fetch 100 images (10 requests of 10)
echo "Fetching image metadata..."
images=$(mktemp)
for i in {1..10}; do
  curl -s "https://api.thecatapi.com/v1/images/search?limit=10" >> "$images"
done

# Flatten JSON array
jq -s 'add' "$images" > "$images.json"
rm "$images"
images="$images.json"

# Process each image
jq -c '.[]' "$images" | while read -r img; do
  url=$(echo "$img" | jq -r '.url')
  width=$(echo "$img" | jq -r '.width')
  height=$(echo "$img" | jq -r '.height')
  filename=$(basename "$url")
  ext="${filename##*.}"
  ext_lower=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
  filepath="$TMP_DIR/$filename"

  echo "Processing $filename (width: $width, height: $height)..."

  # Download image
  curl -s "$url" -o "$filepath"

  # Scan if dimensions > 2000
  if [ "$width" -gt 2000 ] || [ "$height" -gt 2000 ]; then
    echo "Scanning $filename with Scanii..."
    curl -s -u "$SCANNII_API_KEY:$SCANNII_API_SECRET" \
      -F "file=@$filepath" \
      https://api-eu2.scanii.com/v2.2/files | jq
  fi

  # Archive if dimensions > 1000
  if [ "$width" -gt 1000 ] || [ "$height" -gt 1000 ]; then
    archive_path="$TMP_DIR/${filename}.tar.gz"
    tar -czf "$archive_path" -C "$TMP_DIR" "$filename"
    s3_key="$S3_PREFIX/$ext_lower/${filename}.tar.gz"
    echo "Uploading archive to S3: $s3_key"
    aws s3 cp "$archive_path" "s3://$BUCKET/$s3_key"
    rm "$archive_path"
  else
    s3_key="$S3_PREFIX/$ext_lower/$filename"
    echo "Uploading image to S3: $s3_key"
    aws s3 cp "$filepath" "s3://$BUCKET/$s3_key"
  fi

  rm "$filepath"
done

rm "$images"
rmdir "$TMP_DIR"
echo "Done."