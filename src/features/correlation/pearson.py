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
    
    # To calculate the expectation means to calculate the cov(x_population, y_population)
    # This can also be done using numpy. For that use: np.cov(x_population, y_population, bias=True)
    # bias=True indicates that we are calculating the population covariance
    # np.cov returns a bxb matrix, where b is the amount of vectors passed as parameter, in our case b=2
    expectation = np.mean((x_population - x_mean) * (y_population - y_mean))
    std_product = x_std * y_std

    return expectation/std_product

def sample_correlation(data_matrix, x_index, y_index):
    # Sample information
    sample_len = len(data_matrix[0][0])
    sample_sum = data_matrix.sum(axis=0)

    # Feature information
    transposed_data = data_matrix.transpose()
    x_population = transposed_data[x_index]
    y_population = transposed_data[y_index]
    xy = np.multiply(x_population, y_population)
    x_pow = np.multiply(x_population, x_population)
    y_pow = np.multiply(y_population, y_population)

    # Sample correlation calculation
    numerator = (sample_len * xy.sum()) - (sample_sum[x_index] * sample_sum[y_index])
    x_denominator = (sample_len * x_pow.sum()) - (x_population.sum() ** 2)
    y_denominator = (sample_len * y_pow.sum()) - (y_population.sum() ** 2)
    denominator = (x_denominator * y_denominator) ** (1/2)
    
    return numerator/denominator
