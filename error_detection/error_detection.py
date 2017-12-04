import numpy as np
import error_detection.vector_operations as vector_ops
import error_detection.summary as summary


def duplicates(matrix, fuzzy=False, fuzzy_ratio_threshold=70):
    return extend_vector_op_to_matrix(matrix, vector_ops.duplicates, [fuzzy, fuzzy_ratio_threshold])


def wrong_types(matrix):
    return extend_vector_op_to_matrix(matrix, vector_ops.wrong_types)


def outliers(matrix):
    return extend_vector_op_to_matrix(matrix, vector_ops.outliers)


def extend_vector_op_to_matrix(matrix, vector_op, vector_op_args=()):
    return np.array([vector_op(column, *vector_op_args) for column in matrix.T]).T


def get_column_error_rates(error_matrix):
    return summary.get_column_error_rates(error_matrix)


def get_column_statistics(data_matrix, alpha=.95):
    return summary.get_column_statistics(data_matrix, alpha)
