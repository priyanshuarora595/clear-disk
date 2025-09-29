# Clear Disk Utility

This Python script (`clear_disk.py`) fills up disk space by making multiple copies of a specified file until only a user-defined buffer of free space remains. It is useful for testing disk-full scenarios or simulating low disk space conditions.

## Features

- Multithreaded file copying for speed
- Customizable buffer (in GB) to leave free space
- User prompts for file and destination directory
- Progress output for each file copy

## Usage

1. **Run the script:**

   ```bash
   python3 clear_disk.py
   ```
2. **Follow the prompts:**

   - Enter the path of the file you want to copy repeatedly.
   - Enter the destination directory where the copies will be created.
3. The script will calculate how many copies can be made, leaving the specified buffer (default: 0.3 GB), and fill the disk accordingly.

## Example

```
Enter path of the file to copy: /Users/you/sample.txt
Enter the path to dump all files: /Users/you/disk_fill/
Free space: 100.00 GB
Usable space after buffer: 99.70 GB
File size: 1.00 MB
Number of copies to create: 102400
Copied file 1/102400 to /Users/you/disk_fill/copy_0.txt
... (progress output) ...
Disk filling completed successfully!
```

## Parameters

- **buffer_size_gb**: Amount of free space (in GB) to leave on the disk (default: 0.3 GB).
- **max_workers**: Number of threads for copying files (default: 16 in main, 8 in function default).

## Safety Notes

- **Warning:** This script will fill your disk and may cause system instability if the buffer is set too low. Use with caution and only on non-critical systems or test environments.
- To stop the process, use `Ctrl+C` in the terminal.

## Requirements

- Python 3.7+
