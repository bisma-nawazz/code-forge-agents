from fractions import Fraction

import pytest
from hypothesis import example, given
from hypothesis import strategies as st

from textstats import mean, median

finite_floats = st.floats(allow_nan=False, allow_infinity=False)
# Bounded so that a non-integral mean of ints stays representable as a float.
ints = st.integers(min_value=-(2**1000), max_value=2**1000)
numbers = st.one_of(ints, finite_floats)
float_lists = st.lists(finite_floats, min_size=1)
int_lists = st.lists(ints, min_size=1)


@given(st.one_of(float_lists, int_lists))
@example([0.1, 0.1, 0.1])
@example([1e308, 1e308])
@example([10**400])
def test_mean_is_bounded_by_min_and_max(values):
    assert min(values) <= mean(values) <= max(values)


@given(float_lists)
@example([0.1, 0.1, 0.1])
@example([1e308, 1e308])
def test_mean_of_floats_is_correctly_rounded(values):
    exact = sum(map(Fraction, values)) / len(values)
    assert mean(values) == float(exact)


@given(numbers, st.integers(min_value=1, max_value=50))
@example(0.1, 3)
@example(1e308, 2)
def test_mean_of_repeated_value_is_that_value(x, n):
    assert mean([x] * n) == x


@given(st.one_of(float_lists, int_lists))
@example([1e308, 1e308])
@example([-1e308, -1e308])
@example([10**400, 10**400])
def test_median_is_bounded_by_min_and_max(values):
    assert min(values) <= median(values) <= max(values)


@given(st.one_of(float_lists, int_lists), st.randoms())
def test_median_ignores_order(values, rnd):
    shuffled = list(values)
    rnd.shuffle(shuffled)
    assert median(shuffled) == median(values)


@given(st.one_of(float_lists, int_lists))
def test_median_splits_values_in_half(values):
    m = median(values)
    assert sum(v < m for v in values) <= len(values) // 2
    assert sum(v > m for v in values) <= len(values) // 2


@given(numbers, st.integers(min_value=1, max_value=50))
@example(2**53 + 1, 2)
@example(1e308, 2)
def test_median_of_repeated_value_is_that_value(x, n):
    assert median([x] * n) == x


@given(st.one_of(float_lists, int_lists))
def test_functions_accept_any_iterable(values):
    assert mean(iter(values)) == mean(values)
    assert median(iter(values)) == median(values)


@pytest.mark.parametrize("func", [mean, median])
@pytest.mark.parametrize("empty", [[], (), iter([]), (x for x in [])])
def test_empty_input_raises_value_error(func, empty):
    with pytest.raises(ValueError):
        func(empty)


def test_huge_input():
    values = [1e308] * 1_000_000
    assert mean(values) == 1e308
    assert median(values) == 1e308
