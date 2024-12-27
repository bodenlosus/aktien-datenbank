import sys
from aktiendb.updateDatabase import update
import schedule
import threading
import time
import logging
import pathlib

logger = logging.getLogger(__name__)

class StreamToLogger:
    def __init__(self, logger, log_level):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, message):
        if message.strip():  # Avoid logging empty lines
            self.logger.log(self.log_level, message.strip())

    def flush(self):
        pass  # Required for file-like object, no-op here

def job():
    print("updating database")
    try:
        update()
    except Exception as e:
        logger.exception(f"Error updating database: {e}")
    return

def updateService():
    while True:
        schedule.run_pending()
        time.sleep(60)

def main():
    updateTime = "01:00"
    
    print(sys.argv)
    
    sys.stdout = StreamToLogger(logger, logging.INFO)
    sys.stderr = StreamToLogger(logger, logging.ERROR)
    
    current_datetime = time.strftime("%Y-%m-%dT%H:%M:%S")
    log_file = pathlib.Path(f"./log/{current_datetime}.log")
    log_file.touch(exist_ok=True)
    
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,  # Set the logging level
        format='%(asctime)s - %(levelname)s - %(message)s',  # Define log format with timestamp
        datefmt='%Y-%m-%d %H:%M:%S'  # Define the timestamp format
    )
    
    service = threading.Thread(target=updateService)
    service.start()
    schedule.every().day.at("01:00").do(job)
    schedule.run_all()
    service.join()

if __name__ == "__main__":
    main()