from typing import Union
import numpy as np
from datetime import datetime, timedelta
import dateutil


class TrackRecord:
    def __init__(self, file_path):
        self.file_path = file_path
        self.record = dict()
        self.dateFormat = "%Y-%m-%d"

    def updateRecord(self, stock_ids: list[int], timestamp:str=None):
        if not timestamp:
            today = self
            date4YearsAgo = today - timedelta(days=365 * 4)
            timestamp = date4YearsAgo.strftime(self.dateFormat)
        
        for id in stock_ids:
            self.record[id] = timestamp

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

    def getDaysSinceLastUpdate(self, timestamp:str) -> int:
            currentDate = datetime.now()
            updateDate = datetime.strptime(timestamp, self.dateFormat)
            
            diff = currentDate - updateDate

            daysSinceUpdate = diff.days

            return daysSinceUpdate
    
    def getLastUpdateTimestamp(self, id) -> str:
        defaultTimestamp = self.getCurrentDate().strptime
        timestamp = self.record.get(id, defaultTimestamp)
        
        return timestamp
    
    def getMaxUpdateData(self, ids: list[int]) -> str:
        maxID = max(ids, key=lambda id: self.getDaysSinceLastUpdate(self.record[id]))
        timestamp = self.getLastUpdateTimestamp(maxID)
        period = self.getUpdatePeriod(maxID)
        
        return timestamp, period
    
    def getCurrentDate(self):
        currentDate = datetime.now()
        return currentDate

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
