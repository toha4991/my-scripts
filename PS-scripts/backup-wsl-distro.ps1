$distroName = "workdistro"
$backupPath = "C:\wsl\backups\wsl-backup-$distroName-$((Get-Date).ToString('yyyy-MM-dd')).tar"

# Export the WSL distro
wsl --export $distroName $backupPath

# Optional: Keep only the latest 5 backups
$backupFolder = "C:\wsl\backups\"
Get-ChildItem -Path $backupFolder -Filter "wsl-backup-*.tar" | 
    Sort-Object LastWriteTime -Descending | 
    Select-Object -Skip 5 | 
    Remove-Item
