from mrjob.job import MRJob


class Happiness(MRJob):

    def mapper(self, key, line):
        chunks=line.split("\t")
        word=chunks[0]
        avg=float(chunks[2])
        rank=chunks[4]
        if avg < 2 and rank!="--":
            result=(word, avg)
            yield ("negativeWord", result)

    def reducer(self, key, values):
        listSorted = sorted(values, key=lambda tup: tup[1])
        for index in range(1,6):
            yield (listSorted[-index][0], listSorted[-index][1])


if __name__ == '__main__':
    Happiness.run()

