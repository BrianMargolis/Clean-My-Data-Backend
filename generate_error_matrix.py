import numpy as np
def generate_error_matrix(input_matrix, criteria):
	shape = input_matrix.shape
	error_matrix = []
	for col_num in range(shape[1]):
		col = input_matrix[:, col_num]
		output_col = criteria(col)
		error_matrix.append(output_col)
	error_matrix = np.array(error_matrix).transpose()
	return error_matrix

# def plus(x):
# 	new_x = [i+1 for i in x]
# 	return new_x


# print generate_error_matrix(np.array([[1, 2, 3], [4, 5, 6]]), plus)