import os
import argparse
import logging
import shutil
import hashlib
import threading

def sync_folders(source, replica):
    """
    Synchronizes the contents of the source directory with the replica directory.
    This function ensures that the replica directory is an exact copy of the source directory.
    It performs the following actions:
    1. Copies new and updated files from the source to the replica.
    2. Deletes files and directories in the replica that do not exist in the source.
    3. Logs the synchronization process to both the console and a specified log file.

    Args:
      source (str): The path to the source directory.
      replica (str): The path to the replica directory.
      log_file (str): The path to the log file where synchronization logs will be written.
    """
    # Check if the source directory exist
    if not os.path.isdir(source):
      logging.error(f"Source directory '{source}' does not exist.")
    
    # Synchronize the source and replica folders
    for root, dirs, files in os.walk(source):
      relative_path = os.path.relpath(root, source)
      replica_dir = os.path.join(replica, relative_path)

      if not os.path.exists(replica_dir):
        os.mkdir(replica_dir)
        logging.info(f"Created directory '{replica_dir}'.")

      for file in files:
        source_file = os.path.join(root, file)
        replica_file = os.path.join(replica_dir, file)

        if not os.path.exists(replica_file):
          shutil.copy2(source_file, replica_file)
          logging.info(f"Copied file '{source_file}' to '{replica_dir}'.")
        else:
          source_hash = hashlib.md5(open(source_file, 'rb').read()).hexdigest()
          replica_hash = hashlib.md5(open(replica_file, 'rb').read()).hexdigest()
          if source_hash != replica_hash:
            shutil.copy2(source_file, replica_file)
            logging.info(f"Updated file '{source_file}' in '{replica_dir}'.")
    
    # Delete files and directories in the replica that do not exist in the source
    for root, dirs, files in os.walk(replica):
      relative_path = os.path.relpath(root, replica)
      source_dir = os.path.join(source, relative_path)

      if not os.path.exists(source_dir):
        shutil.rmtree(root)
        logging.info(f"Deleted directory '{root}'.")
      
      for file in files:
        replica_file = os.path.join(root, file)
        source_file = os.path.join(source_dir, file)

        if not os.path.exists(source_file):
          os.remove(replica_file)
          logging.info(f"Deleted file '{replica_file}'.")

def run_periodically(interval, stop_event, *sycn_args):
  """
  This function runs a synchronization task in a separate thread at regular intervals.
  It continues to run the task until the `stop_event` is set. After each synchronization
  run, it waits for the specified interval before starting the next run.
  """
  while not stop_event.is_set():
    print("Starting synchronization...")
    task_thread = threading.Thread(target=sync_folders, args=sycn_args)
    task_thread.start()
    task_thread.join()
    print("Synchronization complete.\n")

    stop_event.wait(interval)

def listen_for_stop(stop_event):
  """
  Listens for user input to stop a synchronization process.
  This function continuously prompts the user to enter 'stop' to stop the synchronization.
  When 'stop' is entered, the stop_event is set, which can be used by other threads to
  detect that the synchronization should be stopped.
  """
  while not stop_event.is_set():
    user_input = input("Enter 'stop' to stop the synchronization: \n").strip().lower()
    if user_input == "stop":
      stop_event.set()
      print("Synchronization stopped.")

def main():
  parser = argparse.ArgumentParser(description="Synchronize two folders periodically.")
  parser.add_argument("source", help="Path to the source folder")
  parser.add_argument("replica", help="Path to the replica folder")
  parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
  parser.add_argument("log_file", help="Path to the log file")

  # Parse the command-line arguments
  args = parser.parse_args()

  # Configure logging to write to both the specified log file and the console
  logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", handlers=[
        logging.FileHandler(args.log_file),
        logging.StreamHandler()
    ])

  stop_event = threading.Event()

  input_thread = threading.Thread(target=listen_for_stop, args=(stop_event,))
  input_thread.start()

  task_thread = threading.Thread(target=run_periodically, args=(args.interval, stop_event, args.source, args.replica))
  task_thread.start()

  input_thread.join()
  task_thread.join()

if __name__ == "__main__":
  main()
