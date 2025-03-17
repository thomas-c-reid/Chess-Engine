def index_to_algebraic(index):
    """
    Converts a numeric index (0-63) to algebraic notation.
    :param index: int, the square index (0 for a1, 63 for h8)
    :return: str, the square in algebraic notation (e.g., 'a1', 'h8')
    """
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    file = files[index % 8]
    rank = index // 8 + 1
    return f"{file}{rank}"
