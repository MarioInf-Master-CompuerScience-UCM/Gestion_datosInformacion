from mrjob.job import MRJob


class MRWordCount(MRJob):

    def mapper(self, key, line):
        for word in line.split():
            yield (word, 1)

    def reducer(self, key, values):
        yield (key, sum(values))


if __name__ == '__main__':
    MRWordCount.run()

