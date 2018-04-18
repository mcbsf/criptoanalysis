import numpy as np

def population_correlation(data_matrix, x_index, y_index):
    """
    data_matrix is a numpy multi-dimensional array (matrix)
    x_index and y_index are the index for the first and second variables respectively
    it returns the correlation between two variables in a data_matrix
    """
    transposed_data = data_matrix.transpose()
    x_population = transposed_data[x_index]
    x_mean = np.mean(x_population)
    x_std = np.std(x_population)
    y_population = transposed_data[y_index]
    y_mean = np.mean(y_population)
    y_std = np.std(y_population)
    
    expectation = np.mean((x_population - x_mean) * (y_population - y_mean))
    std_product = x_std * y_std

    return expectation/std_product

    