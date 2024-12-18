import os
from datetime import datetime

def write_log(log_folder, message):
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_file_name = datetime.now().strftime("%Y-%m-%d_%H-%M.log")
    log_file_path = os.path.join(log_folder, log_file_name)

    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
