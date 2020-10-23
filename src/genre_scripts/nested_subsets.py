import numpy as np
import pandas as pd


class NestedSubsets:
    """Generate nested subsets of a data set.
    Input: a pd.DataFrame, an optional step_size, and an optional percentage.
    Step_size overrides percentage.

    Output: an iterator whose elements are nested subsets of the input,
    decreasing in size. The decrease in size is step_size or the
    prescribed percentage of the input."""

    def __init__(self, data, step_size=None, percentage=0.1):
        self.data = data
        self.sample = data.sample(data.shape[0])  # full data set
        self.step_size = int(percentage * data.shape[0])
        if step_size:
            self.step_size = step_size  # minium subsample size
        self.remainder_size = self.sample.shape[0] % self.step_size  # remainder subset
        self.sample_size = self.sample.shape[0]  # initial subsample size

    def __iter__(self):
        return self

    def __next__(self):
        if self.sample_size == 0:
            raise StopIteration
        current_sample = self.sample  # update the subsample to output
        self.sample_size = max(
            self.sample_size - self.step_size, 0
        )  # new subsample size
        self.sample = self.sample.sample(self.sample_size)
        return current_sample

    def get_step_size(self):
        return self.step_size

    def get_number_of_steps(self):
        return int(self.data.shape[0] // self.step_size)
