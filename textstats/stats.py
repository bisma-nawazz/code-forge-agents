from statistics import mean


def median(values):
    ordered = sorted(values)
    if not ordered:
        raise ValueError("median of empty data")
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    # (a + b) / 2 overflows to inf near the float limit and loses precision
    # for large ints; mean() sums exactly and rounds once.
    return mean(ordered[middle - 1 : middle + 1])
