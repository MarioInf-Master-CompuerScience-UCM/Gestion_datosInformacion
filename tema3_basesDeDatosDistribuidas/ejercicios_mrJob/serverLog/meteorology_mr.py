import json
from statistics import mean
from mrjob.job import MRJob


class Meteorology(MRJob):

    def mapper(self, key, line):
        chunks=line.split(" ")
        host=chunks[0]
        if len(chunks)!=10:
            return


        if chunks[-1].isnumeric()==False:
            response=( int(chunks[-2]), 0)

        else:
            response=( int(chunks[-2]), int(chunks[-1]) )
            
        yield (host, response)



    def reducer(self, key, values):
        data=list(values)
        numErrores=0
        tamTotal=0
        for d in data:
            tamTotal=tamTotal+d[1]
            if d[0]>=400 and d[0]<600:
                numErrores=numErrores+1

        result={
            'numeroPeticiones': len(data),
            'tamanoTotal': tamTotal,
            'numeroErrores': numErrores
        }

        yield (key, str(result))

if __name__ == '__main__':
    Meteorology.run()

