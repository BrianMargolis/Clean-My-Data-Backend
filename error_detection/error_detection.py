import numpy as np
import error_detection.error_detection_vector_ops as vector_ops


def duplicates(matrix, fuzzy=False, fuzzy_ratio_threshold=70):
    return extend_vector_op_to_matrix(matrix, vector_ops.duplicates, [fuzzy, fuzzy_ratio_threshold])


def wrong_types(matrix):
    return extend_vector_op_to_matrix(matrix, vector_ops.wrong_types)


def outliers(matrix):
    return extend_vector_op_to_matrix(matrix, vector_ops.outliers)


def extend_vector_op_to_matrix(matrix, vector_op, vector_op_args=()):
    # return np.array([vector_op(column, *vector_op_args) for column in matrix.data.T]).T
    o = []
    for i, column in enumerate(matrix.data.T):
        o.append(vector_op(column, matrix.types[i], *vector_op_args))

    return np.array(o).T
