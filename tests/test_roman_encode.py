"""
Test cases for roman_encode function
"""
import pytest
from roman_encode_decode.main import roman_encode


# Happy path tests with various realistic test values
@pytest.mark.parametrize(
    "input_value, expected_output, test_id",
    [
        (1, "I", {"id": "happy_case_1"}),
        (2, "II", {"id": "happy_case_2"}),
        (3, "III", {"id": "happy_case_3"}),
        (4, "IV", {"id": "happy_case_4"}),
        (5, "V", {"id": "happy_case_5"}),
        (6, "VI", {"id": "happy_case_6"}),
        (9, "IX", {"id": "happy_case_9"}),
        (10, "X", {"id": "happy_case_10"}),
        (27, "XXVII", {"id": "happy_case_27"}),
        (58, "LVIII", {"id": "happy_case_58"}),
        (1994, "MCMXCIV", {"id": "happy_case_1994"}),
        (3999, "MMMCMXCIX", {"id": "happy_case_3999"}),
    ],
)
def test_roman_encode_happy_path(input_value, expected_output, test_id):
    """
    Test happy path cases for roman_encode function
    """
    # Act
    print(f"Testing {test_id} with {input_value}")
    result = roman_encode(input_value)

    # Assert
    assert result == expected_output


# Edge cases
@pytest.mark.parametrize(
    "input_value, expected_output, test_id",
    [
        (1, "I", {"id": "edge_case_minimum"}),
        (3999, "MMMCMXCIX", {"id": "edge_case_maximum"}),
    ],
)
def test_roman_encode_edge_cases(input_value, expected_output, test_id):
    """
    Test edge cases for roman_encode function
    """
    # Act
    print(f"Testing {test_id} with {input_value}")
    result = roman_encode(input_value)

    # Assert
    assert result == expected_output


# Error cases
@pytest.mark.parametrize(
    "input_value, expected_exception, test_id",
    [
        (0, ValueError, {"id": "error_case_below_minimum"}),
        (-1, ValueError, {"id": "error_case_negative"}),
        (4000, ValueError, {"id": "error_case_above_maximum"}),
    ],
)
def test_roman_encode_error_cases(input_value, expected_exception, test_id):
    """
    Test error cases for roman_encode function
    """
    # Act & Assert
    print(f"Testing {test_id} with {input_value}")
    with pytest.raises(expected_exception):
        roman_encode(input_value)
