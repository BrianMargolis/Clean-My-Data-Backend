import numpy as np
import json
from scipy import stats


def get_column_error_rates(error):
    error_rates = [float(np.count_nonzero(col)) / len(col) for col in error.T]
    return list(np.around(error_rates, 3).astype(str))


def get_column_summary_statistics(matrix, alpha=.95):
    statistics = SummaryStats()

    for i, col in enumerate(matrix.data.T):
        data_type = matrix.types[i]
        if data_type.data_type == data_type.NUMBER and data_type.is_consistent:
            col = col.astype(float)
            mean = np.mean(col)
            standard_deviation = np.std(col)
            conf_int = stats.norm.interval(alpha, loc=mean, scale=standard_deviation)
            low_outliers = np.count_nonzero(col < conf_int[0])
            high_outliers = np.count_nonzero(col > conf_int[1])

            statistics.append(i, mean, standard_deviation, conf_int, low_outliers, high_outliers)


    return statistics



class SummaryStats:
    def __init__(self):
        self.columns = []
        self.mean = []
        self.standard_deviation = []
        self.confidence_interval = []
        self.low_outliers = []
        self.high_outliers = []

    def append(self, column_index, mean, standard_deviation, confidence_interval, low_outliers, high_outliers):
        if not np.isnan([mean, standard_deviation, low_outliers, high_outliers]).any():
            mean, standard_deviation, low_outliers, high_outliers = np.around([mean, standard_deviation, low_outliers, high_outliers], 3)
            confidence_interval = ", ".join(np.around(confidence_interval, 3).astype(str))

            self.columns.append(column_index)
            self.mean.append(mean)
            self.standard_deviation.append(standard_deviation)
            self.confidence_interval.append(confidence_interval)
            self.low_outliers.append(low_outliers)
            self.high_outliers.append(high_outliers)

    def to_dictionary(self):
        return self.__dict__
