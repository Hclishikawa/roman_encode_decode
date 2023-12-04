"""
Test cases for acceptable_characters function.
"""
import pytest
from roman_encode_decode.main import acceptable_characters


# Parametrized test for happy path scenarios
@pytest.mark.parametrize(
    "test_id, input_string, acceptable_chars, expected",
    [
        ("happy-ascii-lowercase", "hello", "abcdefghijklmnopqrstuvwxyz", True),
        ("happy-ascii-uppercase", "HELLO", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", True),
        ("happy-numeric", "12345", "0123456789", True),
        ("happy-alphanumeric", "abc123", "abcdefghijklmnopqrstuvwxyz0123456789", True),
        ("happy-special-chars", "@!#", "@!#$%^&*", True),
        ("happy-empty-string", "", "abcdefghijklmnopqrstuvwxyz", False),
        ("happy-all-acceptable", "abc", "abc", True),
    ],
)
def test_acceptable_characters_happy_path(
    test_id, input_string, acceptable_chars, expected
):
    """
    Tests acceptable_characters function with various happy path scenarios.
    """
    # Act
    result = acceptable_characters(input_string, acceptable_chars)

    # Assert
    assert result == expected, f"Failed {test_id}"


# Parametrized test for edge cases
@pytest.mark.parametrize(
    "test_id, input_string, acceptable_chars, expected",
    [
        ("edge-single-char", "a", "a", True),
        (
            "edge-all-chars",
            "abcdefghijklmnopqrstuvwxyz",
            "abcdefghijklmnopqrstuvwxyz",
            True,
        ),
        ("edge-none-acceptable", "abc", "def", False),
        ("edge-empty-acceptable", "a", "", False),
        ("edge-space-in-acceptable", " ", " ", True),
        ("edge-space-not-acceptable", "a b", "abc", False),
    ],
)
def test_acceptable_characters_edge_cases(
    test_id, input_string, acceptable_chars, expected
):
    """
    Tests acceptable_characters function with various edge cases.
    """
    # Act
    result = acceptable_characters(input_string, acceptable_chars)

    # Assert
    assert result == expected, f"Failed {test_id}"


# Parametrized test for error cases
@pytest.mark.parametrize(
    "test_id, input_string, acceptable_chars, expected_exception",
    [
        ("error-input-not-string", 123, "abc", TypeError),
        ("error-acceptable-not-string", "abc", 123, TypeError),
    ],
)
def test_acceptable_characters_error_cases(
    test_id, input_string, acceptable_chars, expected_exception
):
    """
    Tests acceptable_characters function with various error cases.
    """
    _ = test_id
    # Act and Assert
    with pytest.raises(expected_exception):
        _ = acceptable_characters(input_string, acceptable_chars)
