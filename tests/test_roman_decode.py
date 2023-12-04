"""
Test cases for roman_decode function.
"""
import pytest
from roman_encode_decode.main import roman_decode


# Happy path tests with various realistic test values
@pytest.mark.parametrize(
    "roman, expected, test_id",
    [
        ("I", "1", "id_happy_1"),
        ("IX", "9", "id_happy_2"),
        ("XII", "12", "id_happy_3"),
        ("L", "50", "id_happy_4"),
        ("C", "100", "id_happy_5"),
        ("D", "500", "id_happy_6"),
        ("M", "1000", "id_happy_7"),
        ("MMMCMXCIX", "3999", "id_happy_8"),
        ("i", "1", "id_happy_9"),
        ("ix", "9", "id_happy_10"),
        ("xii", "12", "id_happy_11"),
        ("l", "50", "id_happy_12"),
        ("c", "100", "id_happy_13"),
        ("d", "500", "id_happy_14"),
        ("m", "1000", "id_happy_15"),
        ("mmmcmxcix", "3999", "id_happy_16"),
    ],
    ids=lambda x: x[-1],
)
def test_roman_decode_happy_path(roman, expected, test_id):
    """
    Tests roman_decode function with various happy path scenarios.
    """
    # Act
    print(f"Testing {test_id} with {roman}")
    result = roman_decode(roman)

    # Assert
    assert result == int(expected)


# Edge cases
@pytest.mark.parametrize(
    "roman, expected, test_id",
    [
        ("IV", "4", "id_edge_1"),
        ("XL", "40", "id_edge_2"),
        ("XC", "90", "id_edge_3"),
        ("CD", "400", "id_edge_4"),
        ("CM", "900", "id_edge_5"),
        ("MCMXC", "1990", "id_edge_6"),
        ("MMXX", "2020", "id_edge_7"),
        ("iv", "4", "id_edge_8"),
        ("xl", "40", "id_edge_9"),
        ("xc", "90", "id_edge_10"),
        ("cd", "400", "id_edge_11"),
        ("cm", "900", "id_edge_12"),
        ("mcmxc", "1990", "id_edge_13"),
        ("mmxx", "2020", "id_edge_14"),
    ],
    ids=lambda x: x[-1],
)
def test_roman_decode_edge_cases(roman, expected, test_id):
    """
    Tests roman_decode function with various edge cases.
    """
    # Act
    print(f"Testing {test_id} with {roman}")
    result = roman_decode(roman)

    # Assert
    assert result == int(expected)  # expected """


def test_roman_decode_error_case_iiii():
    """
    Tests roman_decode function with error case of IIII.
    """
    roman = "IIII"
    with pytest.raises(ValueError, match="Invalid Roman numeral"):
        roman_decode(roman)


def test_roman_decode_error_case_vv():
    """
    Tests roman_decode function with error case of VV.
    """
    roman = "VV"
    with pytest.raises(ValueError, match="Invalid Roman numeral"):
        roman_decode(roman)


def test_roman_decode_error_case_ll():
    """
    Tests roman_decode function with error case of LL.
    """
    roman = "LL"
    with pytest.raises(ValueError, match="Invalid Roman numeral"):
        roman_decode(roman)


def test_roman_decode_error_case_dd():
    """
    Tests roman_decode function with error case of DD.
    """
    roman = "DD"
    with pytest.raises(ValueError, match="Invalid Roman numeral"):
        roman_decode(roman)


def test_roman_decode_error_case_ic():
    """
    Tests roman_decode function with error case of IC.
    """
    roman = "IC"
    with pytest.raises(ValueError, match="Invalid Roman numeral"):
        roman_decode(roman)


def test_roman_decode_error_case_im():
    """
    Tests roman_decode function with error case of IM.
    """
    roman = "IM"
    with pytest.raises(ValueError, match="Invalid Roman numeral"):
        roman_decode(roman)


def test_roman_decode_error_case_xm():
    """
    Tests roman_decode function with error case of XM.
    """
    roman = "XM"
    with pytest.raises(ValueError, match="Invalid Roman numeral"):
        roman_decode(roman)


def test_roman_decode_error_case_vl():
    """
    Tests roman_decode function with error case of VL.
    """
    roman = "VL"
    with pytest.raises(ValueError, match="Invalid Roman numeral"):
        roman_decode(roman)


def test_roman_decode_error_case_abc():
    """
    Tests roman_decode function with error case of abc.
    """
    roman = "abc"
    with pytest.raises(ValueError, match="Invalid Roman numeral"):
        roman_decode(roman)


def test_roman_decode_error_case_empty():
    """
    Tests roman_decode function with error case of empty string.
    """
    roman = ""
    with pytest.raises(ValueError, match="Invalid Roman numeral"):
        roman_decode(roman)
