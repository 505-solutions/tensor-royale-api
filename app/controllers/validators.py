import numpy as np


def agreement(results):
    # results is an array of 2d matrices which hold a result
    # each result is a 2d matrix
    # rows are confidences in each class
    # columns are the number of samples
    results = np.array(results)

    # we first want to get median across all resuls for each spot in a matrix
    median_result = np.median(results, axis=0)

    # we want to calculate absolute distance for each result from the median
    distances = np.abs(results - median_result)

    # we want to rank the distances for each result (lower distance first)
    ranked_distances = np.argsort(distances, axis=0)

    # we want to return True for each result in the first half of the ranking
    # and False for the second half
    # in the return index i is true if the value i appears in ranked_distances[:len(ranked_distances)//2]
    accepted = np.array([i in ranked_distances[:len(ranked_distances)//2] for i in range(len(ranked_distances))])

    return median_result, ranked_distances, accepted