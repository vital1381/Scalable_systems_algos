from math import sqrt


class FloatingZScore:
    def __init__(self, decay, pop=[]):
        self.sqrAvg = self.avg = 0
        # The rate at which the historic data's effect will diminish.
        self.decay = decay
        for x in pop:
            self.update(x)

    def update(self, value):
        # Set initial averages to the first value in the sequence.
        if self.avg == 0 and self.sqrAvg == 0:
            self.avg = float(value)
            self.sqrAvg = float((value ** 2))
        # Calculate the average of the rest of the values using a
        # floating average.
        else:
            self.avg = self.avg * self.decay + value * (1 - self.decay)
            self.sqrAvg = self.sqrAvg * self.decay + (value ** 2) * (1 - self.decay)
        return self

    def std(self):
        # Somewhat ad-hoc standard deviation calculation.
        return sqrt(self.sqrAvg - self.avg ** 2)

    def score(self, obs):
        if self.std() == 0:
            return (obs - self.avg) * float("infinity")
        else:
            return (obs - self.avg) / self.std()


class ZScore:
    def __init__(self, pop=[]):
        self.number = float(len(pop))
        self.total = sum(pop)
        self.sqrTotal = sum(x ** 2 for x in pop)

    def update(self, value):
        self.number += 1.0
        self.total += value
        self.sqrTotal += value ** 2

    def avg(self):
        return self.total / self.number

    def std(self):
        return sqrt((self.sqrTotal / self.number) - self.avg() ** 2)

    def score(self, obs):
        return (obs - self.avg()) / self.std()


if __name__ == "__main__":
    pass
