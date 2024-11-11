from updateDatabase import update
import schedule

import time

def job():
    print("updating database")
    try:
        update()
    except Exception as e:
        print(f"Error occurred during update: {e}")
    return

schedule.every().day.at("01:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)