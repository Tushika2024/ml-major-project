import logging
import os
from datetime import datetime

log_file_name=f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"## log file name with timestamp
logs_dir_path=os.path.join(os.getcwd(),"logs",log_file_name)## logs directory path where log files will be stored
os.makedirs(logs_dir_path,exist_ok=True)## if logs directory does not exist, create it
log_file_path=os.path.join(logs_dir_path,log_file_name)## complete log file path

logging.basicConfig(
    filename=log_file_path,
    format='[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# if __name__ == "__main__":
#     logging.info("Logging setup complete.")