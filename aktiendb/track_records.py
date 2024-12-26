from typing import Generator, Union
import numpy as np
import time


class TrackRecord:
    def __init__(self, file_path):
        self.file_path = file_path
        self.record = dict()

    def updateRecord(self, stock_ids: list[int]):
        currentTime: str = time.strftime("%Y-%m-%d_%H:%M:%S", time.gmtime())

        for id in stock_ids:
            self.record[id] = currentTime

        self.saveRecord()

    def saveRecord(self):
        with open(self.file_path, "w") as file:
            file.writelines([f"{id},{time}\n" for id, time in self.record.items()])

    def readRecord(self) -> dict[int, Union[str, None]]:
        with open(self.file_path, "r") as file:
            recordLines = [line.strip().split(",") for line in file.readlines()]

        for id, timestamp in recordLines:
            self.record[int(id)] = timestamp
        
        return self.record

    def getDaysSinceLastUpdate(self, timestamp) -> int:
            currentTime = time.mktime(time.gmtime())
            updateTime = time.mktime(time.strptime(timestamp, "%Y-%m-%d_%H:%M:%S"))

            timeSinceUpdate = (currentTime - updateTime) / (60 * 60 * 24)

            daysSinceUpdate = int(np.ceil(timeSinceUpdate))

            return daysSinceUpdate
    
    def getLastUpdateTimestamp(self, id) -> str:
        timestamp = self.record[id]
    
    def getCurrentDate(self):
        currentTime = time.strftime("%Y-%m-%d", time.gmtime())
        return currentTime

    def getUpdatePeriod(self, id) -> str:
        possibleIntervals = {
            1: "1d",
            5: "5d",
            31: "1mo",
            31 * 3: "3mo",
            31 * 6: "6mo",
            366: "1y",
            366 * 2: "2y",
            366 * 5: "5y",
            366 * 10: "10y",
        }
        if id not in self.record.keys():
            return "2y"
        
        timestamp = self.record[id]
        
        days = self.getDaysSinceLastUpdate(timestamp)
        
        for pDays, period in possibleIntervals.items():
            if pDays >= days:
                return period

        return "max"

if __name__ == "__main__":
    record = TrackRecord("./record.dat")
    print(record.readRecord())
    record.updateRecord((2, 3, 4))
    print(record.getUpdatePeriod(1))
