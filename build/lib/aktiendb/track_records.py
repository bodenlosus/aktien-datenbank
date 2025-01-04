from typing import Dict, List, Union
import numpy as np
from datetime import datetime, timedelta
import dateutil


class TrackRecord:
    def __init__(self, file_path):
        self.file_path = file_path
        self.record: Dict[str, datetime] = dict()
        self.dateFormat = "%Y-%m-%d"

    def defaultDate(self):
        today = self.getCurrentDate()
        date4YearsAgo = today - timedelta(days=365 * 4)
        return date4YearsAgo
    
    def updateRecord(self, stock_ids: list[int], datetime:datetime=None):
        if not datetime:
            datetime = self.defaultDate()
        
        for id in stock_ids:
            self.record[id] = datetime

        self.saveRecord()

    def parseTimestamp(self, timestamp:str):
        return datetime.strptime(timestamp, self.dateFormat)
    
    def toTimestamp(self, datetime: datetime) -> str:
        return datetime.strftime(self.dateFormat)
    
    def saveRecord(self):
        with open(self.file_path, "w") as file:
            lines: List[str] = []
            
            for id, datetime in self.record.items():
                timestamp = self.toTimestamp(datetime)
                lines.append(f"{id},{timestamp}\n")
                
            file.writelines(lines)

    def readRecord(self) -> dict[int, Union[str, None]]:
        with open(self.file_path, "r") as file:
            recordLines = [line.strip().split(",") for line in file.readlines()]

        for id, timestamp in recordLines:
            self.record[int(id)] = self.parseTimestamp(timestamp)
        
        return self.record

    def getDaysSinceLastUpdate(self, id:int) -> int:
            currentDate = self.getCurrentDate()
            lastDate = self.getDaysSinceLastUpdate(id)
            diff = currentDate - lastDate

            daysSinceUpdate = diff.days

            return daysSinceUpdate
    
    def getLastUpdateDate(self, id) -> str:
        
        defaultTimestamp = self.defaultDate()
        
        dt = self.record.get(id, defaultTimestamp)
        
        return dt
    
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
            return "5y"
        
        days = self.getDaysSinceLastUpdate(id)
        
        for pDays, period in possibleIntervals.items():
            if pDays >= days:
                return period

        return "max"

if __name__ == "__main__":
    record = TrackRecord("./record.dat")
    print(record.readRecord())
    record.updateRecord((2, 3, 4))
    print(record.getUpdatePeriod(1))
