#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <source_folder> <destination_folder> <retention_days>"
    exit 1
fi

SOURCE_FOLDER=$1
DESTINATION_FOLDER=$2
RETENTION_DAYS=$3

# Check if the destination folder exists, if not create it
if [ ! -d "$DESTINATION_FOLDER" ]; then
    mkdir -p "$DESTINATION_FOLDER"
    echo "Created destination folder: $DESTINATION_FOLDER"
fi

# Get the current date
CURRENT_DATE=$(date +%d-%m-%Y)

# Get the base name of the source folder
BASE_NAME=$(basename "$SOURCE_FOLDER")

# Create the backup file name
BACKUP_FILE="${BASE_NAME}-${CURRENT_DATE}.tar.gz"

# Create the backup
tar -czf "${DESTINATION_FOLDER}/${BACKUP_FILE}" -C "$SOURCE_FOLDER" .

echo "Backup completed: ${DESTINATION_FOLDER}/${BACKUP_FILE}"

# Find and delete backups older than the retention period
find "$DESTINATION_FOLDER" -name "${BASE_NAME}-*.tar.gz" | while read -r file; do
    # Extract the date from the filename
    FILE_DATE=$(echo "$file" | awk -F "[-.]" -v 'OFS=-' '{print $4, $3, $2}')
    FILE_DATE=$(date -d "$FILE_DATE" +%s)
    CURRENT_DATE=$(date +%s)
    AGE=$(( (CURRENT_DATE - FILE_DATE) / 86400 ))
    
    if [ "$AGE" -gt "$RETENTION_DAYS" ]; then
        rm "$file"
        echo "Deleted old backup: $file"
    fi
done

echo "Old backups older than ${RETENTION_DAYS} days have been deleted."