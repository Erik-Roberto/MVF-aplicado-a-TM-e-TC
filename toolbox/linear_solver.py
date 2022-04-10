import numba as nb
import numpy as np


import config as conf
TOL = conf.tolerancia
MAX_ITERATIONS = conf.it_max


@nb.njit
def solve_linear_system(A, B, vector_initial, qtd_col, main_col = 2):
    """
    Solves a penta diagonal linear system using the TDMA method iteratively.
    """
    it = 0
    vector_old = vector_initial.copy()
    error = 10
    while error > TOL and it < MAX_ITERATIONS:
        B_mod = convert_to_tdm(A, B, vector_old, qtd_col)
        vector = tdma_mod(A, B_mod, main_col)
        error = error_max(vector, vector_old)
        vector_old = vector.copy()
        it += 1
    return vector


@nb.njit
def tdma_mod(A, B, main_col = 2):
    """
    Solves a tri diagonal linear system using the TDMA method.
    """
    #TODO: Find a way to make this more efficient with numpy operations.
    rows = len(B)
    vector = np.zeros(shape = rows, dtype = np.float64)
    A_mod = np.zeros(shape = rows, dtype = np.float64)
    B_mod = np.zeros(shape = rows, dtype = np.float64)
    
    A_mod[0] = A[0][3]/A[0][main_col]
    B_mod[0] = B[0]/A[0][main_col]
    for i in range(1, rows):
        A_mod[i] = A[i][3]/(A[i][main_col] - A_mod[i-1]*A[i][1])
        B_mod[i] = (B[i] - B_mod[i-1]*A[i][1])/(A[i][main_col] - A_mod[i-1]*A[i][1])
    
    vector[-1] = B_mod[-1]

    for i in range(rows - 2, -1, -1):
        vector[i] = B_mod[i] - A_mod[i]*vector[i+1]

    return vector

@nb.njit
def error_max(vector1, vector2) -> float:
    """
    Computes the maximum error between two vectors.
    """
    return np.max(np.abs(vector1 - vector2)/np.abs(vector1))


@nb.njit
def convert_to_tdm(A, B, estimate_vector, qtd_col,  omit_cols = (0, 4)):
    """
    Converts a matrix A and a vector B to a TDM system.
    """
    assert len(omit_cols) == 2, "omit_cols must be a tuple of length 2."
    
    rows = len(A)
    B_mod = np.zeros(shape = rows, dtype = np.float64)
    

    #TODO: Find a better way to do this.
    for i in range(qtd_col):
        left_diag = - A[i][omit_cols[1]]*estimate_vector[i + qtd_col]
        B_mod[i] = B[i] + left_diag

    for i in range(qtd_col, rows - qtd_col):
        left_diag = - A[i][omit_cols[1]]*estimate_vector[i + qtd_col]
        right_diag = - A[i][omit_cols[0]]*estimate_vector[i - qtd_col]
        B_mod[i] = B[i] + left_diag + right_diag

    for i in range(rows - qtd_col, rows):
        right_diag = - A[i][omit_cols[0]]*estimate_vector[i - qtd_col]
        B_mod[i] = B[i] + right_diag
    
    return B_mod


def convert_to_sparse_matrix(matrix, qtd_col):
    """
    Converts a matrix to a sparse matrix.
    """
    rows = len(matrix)
    sparse_matrix = np.zeros(shape = (rows, rows), dtype = np.float64)
    for i in range(rows):
        if i >= qtd_col:
            # First line of the matrix (without left values).
            sparse_matrix[i][i - qtd_col] = matrix[i][0]
        if i >= 1:
            # Lines without left values beyond n_cols.
            sparse_matrix[i][i - 1] = matrix[i][1]
        
        if i + 1 < len(matrix[i]):
            # Lines without right values beyond n_cols.
            sparse_matrix[i][i + 1] = matrix[i][3]
        
        if i + qtd_col < len(matrix[i]):
            # Last line of the matrix (without right values).
            sparse_matrix[i][i + qtd_col] = matrix[i][4]

        sparse_matrix[i][i] = matrix[i][2]
    
    return sparse_matrix
