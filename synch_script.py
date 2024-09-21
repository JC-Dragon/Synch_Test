import os
import shutil
import logging

# installs schedule in case it is not installed
try:
    import schedule
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "schedule"])

import schedule
import time
import argparse
import subprocess
import sys

# Set up logging
log_file = 'synch.log'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(log_file),
                        logging.StreamHandler(sys.stdout)
                    ])

# Set retry delay, for when a file is in use while synching, as a constant
RETRY_DELAY = 60  # in seconds

def synch_folders(source, destination):
    # Walk through the source directory
    for root, dirs, files in os.walk(source):
        relative_path = os.path.relpath(root, source)
        dest_path = os.path.join(destination, relative_path)

        # Create directories in the destination
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
            logging.info(f'Created directory: {dest_path}')

        # Copy files
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_path, file)
            # Prevents failure if synch happens while the file is in use
            while True:
                try:
                    # Checks if file exists by checking the path, if it does it compares the timestamps
                    if not os.path.exists(dest_file) or os.path.getmtime(src_file) > os.path.getmtime(dest_file):
                        shutil.copy2(src_file, dest_file)
                        logging.info(f'Copied file: {src_file} to {dest_file}')
                    break
                except PermissionError:
                    logging.warning(f'File {src_file} is in use. Retrying in {RETRY_DELAY} seconds...')
                    time.sleep(RETRY_DELAY)

    # Remove files and directories not present in the source
    for root, dirs, files in os.walk(destination):
        relative_path = os.path.relpath(root, destination)
        src_path = os.path.join(source, relative_path)

        for file in files:
            dest_file = os.path.join(root, file)
            src_file = os.path.join(src_path, file)
            if not os.path.exists(src_file):
                os.remove(dest_file)
                logging.info(f'Removed file: {dest_file}')

        for dir in dirs:
            dest_dir = os.path.join(root, dir)
            src_dir = os.path.join(src_path, dir)
            if not os.path.exists(src_dir):
                shutil.rmtree(dest_dir)
                logging.info(f'Removed directory: {dest_dir}')

def job(source, destination):
    synch_folders(source, destination)

def main():
    parser = argparse.ArgumentParser(description='Synchronize two folders periodically.')
    parser.add_argument('source', type=str, help='Source folder path')
    parser.add_argument('destination', type=str, help='Destination folder path')
    parser.add_argument('period', type=int, help='Synchronization period in minutes')
    args = parser.parse_args()

    schedule.every(args.period).minutes.do(job, source=args.source, destination=args.destination)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info('Synchronization stopped by user.')

if __name__ == "__main__":
    main()
