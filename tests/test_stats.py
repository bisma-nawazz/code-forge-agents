import pytest

from textstats import mean, median


def test_mean():
    assert mean([1, 2, 3]) == 2


def test_median_odd():
    assert median([3, 1, 2]) == 2


def test_median_even_is_mean_of_middle_pair():
    assert median([1, 2, 3, 4]) == 2.5


def test_median_even_unsorted():
    assert median([4, 1, 3, 2]) == 2.5
    assert median([10, -2]) == 4


def test_median_single():
    assert median([7]) == 7


def test_empty():
    with pytest.raises(ValueError):
        median([])
