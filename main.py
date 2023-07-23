import subprocess
import time
import traceback
from datetime import datetime

import schedule

def run_script():
    try:
        subprocess.run(["./venv/Scripts/python", "./VisaResheduler.py"], check=True)
    except Exception as e:
        # Log the error with a timestamp to a log file
        print("s")
        with open("error_log.txt", "a") as log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{timestamp} - Error occurred:\n")
            log_file.write(traceback.format_exc())
            log_file.write("\n")

run_script()
schedule.every(30).minutes.do(run_script)

while True:
    schedule.run_pending()
    time.sleep(1200)
