# This repo's purpose

this are the scripts that I used in my everyday work

## Python scripts

### PDF to Text converter

To run the script use the following command:

```python 
python pdf2txt.py path/to/your/file.pdf 2 5
```

where the first argument is the path to PDF file, the second is number of the page. In case you want to convert a range of pages add the third argument(in the example it's the range 2-5)

### Telegram to csv file

script takes a telegram chat and extracts all the URLs from it sending them to a csv file

### add-double-brackets.py

A script that adds double brackets of user's choice to a string.

```bash
 Example:
    input: "Ethernet, ARP, PPP, Frame Relay"
    output: "[[Ethernet]], [[ARP]], [[PPP]], [[Frame]], [[Relay]]"
```
## Bash scripts

### backup-filename-date.sh 
- creates a backup and scans for old files based on date in filename

### backup-metadata.sh 
- creates a backup and scans for old files based on metadata

### start-containers-clean.sh
in wsl distro after a container is stoped/deleted the ports are still binded by a process like in the following output:
```bash
COMMAND   PID         USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
exe     32765                12u  IPv6 300758      0t0  TCP *:5000 (LISTEN)
exe     44522                12u  IPv6 427540      0t0  TCP *:http-alt (LISTEN)
```
the script helps to automate the process of cleaning up so I can re-run containers on the same ports

## PowerShell scripts

### backup-wsl-distro.ps1
- creates a backup and scans for old files so only the newest backup files remain

## Batch scripts

### start-ubuntu-vm.bat & stop-ubuntu-vm.bat

the `start` script runs a virtual box machine (i.e. ubuntu server) in background and the `stop` script stops it