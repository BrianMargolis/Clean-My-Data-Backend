import numpy as np
from scipy import stats


def get_column_error_rates(error):
    return [float(np.count_nonzero(col)) / len(col) for col in error.T]


def get_column_statistics(data, alpha=.95):
    statistics = []

    for col in data.T:
        mean = np.mean(col)
        standard_deviation = np.std(col)
        conf_int = stats.norm.interval(alpha, loc=mean, scale=standard_deviation)
        low_outliers = np.count_nonzero(col < conf_int[0])
        high_outliers = np.count_nonzero(col < conf_int[1])

        column_statistics = ColumnStats(mean, standard_deviation, conf_int, low_outliers, high_outliers)

        statistics.append(column_statistics)

    return statistics


class ColumnStats:
    def __init__(self, mean, standard_deviation, confidence_interval, low_outliers, high_outliers):
        self.mean = mean
        self.standard_deviation = standard_deviation
        self.confidence_interval = confidence_interval
        self.low_outliers = low_outliers
        self.high_outliers = high_outliers
