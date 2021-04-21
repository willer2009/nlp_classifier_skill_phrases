

class Interval:

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def contains(self, item):
        return item.start >= self.start and item.end <= self.end

    def __str__(self):
        if self is not None:
            return '[{}:{}]'.format(self.start, self.end)