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


currennt_time = time.strftime(time.localtime())

schedule.every().day.at(currennt_time).do(job)

while True:
    schedule.run_pending()
    time.sleep(60)