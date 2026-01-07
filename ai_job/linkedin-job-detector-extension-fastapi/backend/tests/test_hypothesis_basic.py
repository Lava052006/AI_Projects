"""Basic test to verify Hypothesis property-based testing is working."""

from hypothesis import given, strategies as st


@given(st.integers())
def test_hypothesis_basic(x):
    """Basic property test to verify Hypothesis is working."""
    # Property: adding zero to any integer returns the same integer
    assert x + 0 == x


@given(st.text())
def test_string_length_property(s):
    """Test that string length is always non-negative."""
    assert len(s) >= 0


@given(st.lists(st.integers()))
def test_list_reverse_property(lst):
    """Test that reversing a list twice returns the original list."""
    assert list(reversed(list(reversed(lst)))) == lst