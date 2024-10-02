import os
import argparse

path = '.\source'

def sync_folders(source, replica):
  if os.path.isdir(source):
    print(f"{source} exists")
  else:
    print(f"{source} does not exists")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Synchronize two folders periodically.")
  parser.add_argument("source", help="Path to the source folder")
  parser.add_argument("replica", help="Path to the replica folder")
  #parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
  #parser.add_argument("log_file", help="Path to the log file")

  args = parser.parse_args()
  sync_folders(args.source, args.replica)
 
 