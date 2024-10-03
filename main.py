import os
import argparse
import logging

def sync_folders(source, replica, log_file):
    
    # Configure logging to write to the specified log file with INFO level and a specific format
    logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    if not os.path.isdir(source):
        logging.error(f"Source directory '{source}' does not exist.")
    if not os.path.isdir(replica):
        logging.error(f"Replica directory '{replica}' does not exist.")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronize two folders periodically.")
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("replica", help="Path to the replica folder")
    #parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file", help="Path to the log file")

    args = parser.parse_args()
    
    sync_folders(args.source, args.replica, args.log_file)