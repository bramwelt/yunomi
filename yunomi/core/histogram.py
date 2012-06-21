from math import sqrt

from yunomi.stats.exp_decay_sample import ExponentiallyDecayingSample
from yunomi.stats.uniform_sample import UniformSample
from yunomi.stats.snapshot import Snapshot


def enum(**enums):
    return type('Enum', (), enums)

class Histogram(object):
    DEFAULT_SAMPLE_SIZE = 1028
    DEFAULT_ALPHA = 0.015
    count = 0
    variance = [-1.0, 0.0]
    arrayCache = [0.0, 0.0]
    SampleType = enum(UNIFORM = UniformSample(DEFAULT_SAMPLE_SIZE),
                      BIASED = ExponentiallyDecayingSample(DEFAULT_SAMPLE_SIZE, DEFAULT_ALPHA))

    def __init__(self, sample):
        self.sample = sample
        self.clear()

    def clear(self):
        self.sample.clear()
        self.max_ = -2147483647.0
        self.min_ = 2147483647.0
        self.sum_ = 0.0
        self.variance = [-1.0, 0.0]

    def update(self, value):
        self.count += 1
        self.sample.update(value)
        self.set_max(value)
        self.set_min(value)
        self.sum_ += value
        self.update_variance(value)

    def get_count(self):
        return self.count

    def get_max(self):
        if self.get_count() > 0:
            return self.max_
        return 0.0

    def get_min(self):
        if self.get_count() > 0:
            return self.min_
        return 0.0

    def get_mean(self):
        if self.get_count() > 0:
            return self.sum_ / self.get_count()
        return 0.0

    def get_std_dev(self):
        if self.get_count() > 0:
            return sqrt(self.get_variance())
        return 0.0

    def get_variance(self):
        if self.get_count() <= 1:
            return 0.0
        return self.variance[1] / (self.get_count() - 1)

    def get_sum(self):
        return self.sum_

    def get_snapshot(self):
        return self.sample.get_snapshot()

    def set_max(self, new_max):
        if self.max_ < new_max:
            self.max_ = new_max

    def set_min(self, new_min):
        if self.min_ > new_min:
            self.min_ = new_min

    def update_variance(self, value):
        old = self.variance
        new = self.arrayCache
        if old[0] == -1.0:
            new[0] = value
            new[1] = 0.0
        else:
            new[0] = old[0] + (float(value - old[0]) / self.get_count())
            new[1] = old[1] + (float(value - old[0]) * (value - new[0]))
        self.arrayCache = old
        self.variance = new