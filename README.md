
# Folder Synchronization Program

This Python program periodically synchronizes the contents of a source folder with a replica folder. It ensures that the replica folder is always an exact copy of the source folder by copying new and updated files, as well as deleting files and directories in the replica folder that no longer exist in the source. The synchronization process is logged to both the console and a specified log file. The user can stop the synchronization at any time by typing "stop" into the command line.

## Features
- **Automatic synchronization**: New and updated files in the source folder are copied to the replica folder.
- **Replica cleanup**: Files and directories in the replica that are no longer present in the source folder are deleted.
- **Logging**: Detailed logs of the synchronization process are written to a specified log file and displayed in the console.
- **Periodic execution**: The synchronization runs periodically at user-defined intervals.
- **Graceful shutdown**: The user can stop the synchronization process by typing "stop" into the command line.

## Requirements

- Python 3.x
- Required modules: `argparse`, `logging`, `shutil`, `hashlib`, `os`, `threading`

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Download or clone the repository containing the script.
3. Install any required Python modules using `pip` if necessary.

```bash
pip install argparse
```

## Usage

Run the script from the command line with the following arguments:

```bash
python sync_folders.py <source_folder> <replica_folder> <interval_in_seconds> <log_file>
```

### Arguments

- `source_folder`: The path to the source folder (the folder you want to copy files from).
- `replica_folder`: The path to the replica folder (the folder you want to synchronize with the source).
- `interval_in_seconds`: The interval at which the synchronization should occur, in seconds.
- `log_file`: The path to the log file where synchronization details will be recorded.

### Example

```bash
python sync_folders.py /path/to/source /path/to/replica 30 /path/to/logfile.log
```

This command will synchronize the contents of `/path/to/source` with `/path/to/replica` every 30 seconds and log the details in `/path/to/logfile.log`.

### Stopping the Program

To stop the program, type `stop` in the command line where the program is running.

## Logging

The program logs the following events:
- **File and directory creation**: Logs when new files or directories are copied from the source to the replica.
- **File updates**: Logs when files in the replica are updated to match changes in the source.
- **File and directory deletion**: Logs when files or directories are deleted from the replica because they no longer exist in the source.

## How it Works

1. The program first compares the source and replica directories.
2. New files or updated files (based on their content hash) from the source are copied to the replica.
3. Files or directories in the replica that do not exist in the source are deleted.
4. The program runs this synchronization process at a specified interval.
5. A separate thread listens for user input, allowing the user to stop the synchronization by typing "stop" into the console.
