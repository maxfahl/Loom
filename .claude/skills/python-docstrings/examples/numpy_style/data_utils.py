import numpy as np

def calculate_mean(data: list[float]) -> float:
    """Calculate the arithmetic mean of a list of numbers.

    Parameters
    ----------
    data : list of float
        A list containing numerical data points.

    Returns
    -------
    float
        The calculated mean of the data.

    Raises
    ------
    ValueError
        If the input `data` list is empty.

    Examples
    --------
    >>> calculate_mean([1, 2, 3, 4, 5])
    3.0
    >>> calculate_mean([10.5, 20.5])
    15.5
    """
    if not data:
        raise ValueError("Input data cannot be empty.")
    return np.mean(data)

def normalize_vector(vector: np.ndarray) -> np.ndarray:
    """Normalize a NumPy vector to unit length.

    Parameters
    ----------
    vector : numpy.ndarray
        The input vector to be normalized.

    Returns
    -------
    numpy.ndarray
        The normalized vector.

    Raises
    ------
    ValueError
        If the input vector is all zeros.
    """
    norm = np.linalg.norm(vector)
    if norm == 0:
        raise ValueError("Cannot normalize a zero vector.")
    return vector / norm
