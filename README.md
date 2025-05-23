# This repo's purpose

this are the scripts that I used in my everyday work

### PDF to Text converter

To run the script use the following command:

```python 
python pdf2txt.py path/to/your/file.pdf 2 5
```

where the first argument is the path to PDF file, the second is number of the page. In case you want to convert a range of pages add the third argument(in the example it's the range 2-5)

### Telegram to csv file

script takes a telegram chat and extracts all the URLs from it sending them to a csv file

## Bash scripts

### backup-filename-date.sh 
- creates a backup and scans for old files based on date in filename
- 
### backup-metadata.sh 
- creates a backup and scans for old files based on metadata

## PowerShell scripts

### backup-wsl-distro.ps1
- creates a backup and scans for old files so only the newest backup files remain
