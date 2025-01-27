import json
from statistics import mean
from mrjob.job import MRJob


class Meteorology(MRJob):

    def mapper(self, key, line):
        chunks=line.split(",")
        if chunks[0] == "date-time":
            return;

        competDate=chunks[0]
        chunksDate=competDate.split(" ")
        chunksDate=chunksDate[0].split("/")
        dateKey=chunksDate[1]+"/"+chunksDate[0]

        batteryLevel=float(chunks[8])
        yield (dateKey, batteryLevel)



    def reducer(self, key, values):
        data=list(values);
        result={
            'max': max(data),
            'avg': mean(data),
            'min': min(data)
        }
        yield (key, str(result))

if __name__ == '__main__':
    Meteorology.run()

