from typing import Callable

import numpy as np
import error_detection.error_detection_vector_ops as vector_ops
from error_detection.Matrix import Matrix


def duplicates(matrix: Matrix, fuzzy: bool = False, fuzzy_ratio_threshold: int = 70) -> np.ndarray:
    """
    Find duplicates by column in a matrix.

    :param matrix: a Matrix object
    :param fuzzy: boolean representing whether to use fuzzy matching or not
    :param fuzzy_ratio_threshold: threshold for fuzzy matching. Between 0 and 100. Higher values indicate stricter matching.

    :return: boolean ndarray of same size as matrix.data representing locations of duplicates
    """
    return extend_vector_op_to_matrix(matrix, vector_ops.duplicates, [fuzzy, fuzzy_ratio_threshold])


def wrong_types(matrix: Matrix) -> np.ndarray:
    """
    Find incorrect types by column in a matrix. Determines type of column by majority vote, then marks the minority as incorrect. Supports two data types: number and string.

    :param matrix: a Matrix object

    :return: boolean ndarray of same size as matrix.data representing locations of incorrect types
    """
    return extend_vector_op_to_matrix(matrix, vector_ops.wrong_types)


def outliers(matrix: Matrix) -> np.ndarray:
    """
    Find outliers in a matrix using an isolation forest.

    :param matrix: a Matrix object

    :return: boolean ndarray of same size as matrix.data representing locations of outliers
    """
    return extend_vector_op_to_matrix(matrix, vector_ops.outliers)


def extend_vector_op_to_matrix(matrix: Matrix, vector_op: Callable, vector_op_args: list = ()) -> np.ndarray:
    """
    Applies a vector operation to each column of a matrix.

    :param matrix: a Matrix object
    :param vector_op: the vector operation to use (from error_detection_vector_ops)
    :param vector_op_args: optional arguments to pass to vector_op.

    :return: The resultant matrix.
    """
    output = []
    for i, column in enumerate(matrix.data.T):
        output.append(vector_op(column, matrix.types[i], *vector_op_args))

    return np.array(output).T
