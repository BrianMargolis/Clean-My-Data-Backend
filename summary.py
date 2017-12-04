#overall error rate, column totals and column rate
#For each number column, give the 95% CI for a normal distribution and the number of outliers on each side of it
#assuming numpy matrix in original shape
import numpy as np
from scipy import stats

def error_rates(data):
	#assumes matrices are marked with error codes
	shape = data.shape
	total_cell_count = shape[0]*shape[1]
	total_error_count = len(np.nonzero(data)[0])
	total_error_rate = float(total_error_count) / total_cell_count

	col_error_count = []
	col_error_rate = []

	for col_num in range(shape[1]):
		col = data[:, col_num].reshape(-1)
		error_count = len(np.nonzero(col)[0])
		error_rate = float(error_count) / shape[0]
		col_error_count.append(error_count)
		col_error_rate.append(error_rate)
	print [total_error_count, total_error_rate, col_error_count, col_error_rate]
	return [total_error_count, total_error_rate, col_error_count, col_error_rate]



def outliers(data):
	#assumes matrices contains original numeric data
	shape = data.shape
	total_stats = []

	for col_num in range(shape[1]):
		col = data[:, col_num].reshape(-1)
		mean, sigma = np.mean(col), np.std(col)
		conf_int = stats.norm.interval(0.95, loc=mean, scale=sigma)
		lower_indices = len(np.nonzero(col < conf_int[0])[1])
		upper_indices = len(np.nonzero(col > conf_int[1])[1])
		print conf_int
		print lower_indices, upper_indices
		# lower_outliers = [item in col if col.indices in lower_indices]
		# upper_outliers = [item in col if col.index in upper_indices]
		
		total_stats.append([conf_int, lower_indices, upper_indices])

	return total_stats

# error_rates(np.matrix([[0, 0, 0], [1, 1, 1], [0, 1, 1], [1, 1, 0]]))
# outliers(np.matrix([[1, 1, 2, 35], [3, 3, 1, 1], [40, 1, 2, 1], [1, 1, -500, 3], [4, 1, 70, 3]]))