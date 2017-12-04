import numpy as np
import error_detection.vector_operations as vector_ops


def duplicates(matrix, fuzzy=False, fuzzy_ratio_threshold=70):
    return extend_vector_op_to_matrix(matrix, vector_ops.duplicates, [fuzzy, fuzzy_ratio_threshold])


def wrong_types(matrix):
    return extend_vector_op_to_matrix(matrix, vector_ops.wrong_types)


def outliers(matrix):
    return extend_vector_op_to_matrix(matrix, vector_ops.outliers)


def extend_vector_op_to_matrix(input_matrix, vector_op, vector_op_args=()):
    output_matrix = []

    # Is transposing a huge matrix expensive?
    # https://stackoverflow.com/questions/19479384/is-numpy-transpose-reordering-data-in-memory/19479436#19479436
    # TLDR: no, it just changes the stride of the array.
    for columns in input_matrix.T:
        output_matrix.append(vector_op(columns, *vector_op_args))

    return np.array(output_matrix).T
