"""
Sample program demonstrating the roman_encode and roman_decode functions and
how to test them using pytest and coverage.
"""
import emoji


def acceptable_characters(
    input_string: str, characters_that_are_acceptable: str
) -> bool:
    """
    Checks if all characters in the input string are acceptable.

    Args:
        input_string (str): The string to be validated.
        characters_that_are_acceptable (str): The string containing all acceptable characters.

    Returns:
        bool: True if all characters in the input string are acceptable, False otherwise.
    """
    if not input_string:
        return False
    validation = set(input_string)
    return validation.issubset(characters_that_are_acceptable)


def roman_decode(roman: str) -> int:
    """
    Decodes a Roman numeral string into an integer.

    Args:
        roman (str): The Roman numeral string to be decoded.

    Returns:
        int: The integer representation of the input Roman numeral.

    Raises:
        ValueError: If the input Roman numeral is invalid.

    Examples:
        >>> roman_decode("I")
        1
        >>> roman_decode("IX")
        9
        >>> roman_decode("MMMCMXCIX")
        3999
    """

    roman_digits: str = "ivxlcdm"
    all_good_characters: bool = acceptable_characters(
        roman.upper(), roman_digits.upper()
    )
    if not all_good_characters:
        raise ValueError("Invalid Roman numeral")
    if "IIII" in roman.upper():
        raise ValueError("Invalid Roman numeral")
    if "VV" in roman.upper():
        raise ValueError("Invalid Roman numeral")
    if "LL" in roman.upper():
        raise ValueError("Invalid Roman numeral")
    if "DD" in roman.upper():
        raise ValueError("Invalid Roman numeral")
    if "IC" in roman.upper():
        raise ValueError("Invalid Roman numeral")
    if "IM" in roman.upper():
        raise ValueError("Invalid Roman numeral")
    if "XM" in roman.upper():
        raise ValueError("Invalid Roman numeral")
    if "VL" in roman.upper():
        raise ValueError("Invalid Roman numeral")
    roman_values = (
        ("I", 1),
        ("IV", 4),
        ("V", 5),
        ("IX", 9),
        ("X", 10),
        ("XL", 40),
        ("L", 50),
        ("XC", 90),
        ("C", 100),
        ("CD", 400),
        ("D", 500),
        ("CM", 900),
        ("M", 1000),
    )
    total = 0
    working = roman.upper()
    for symbol, value in reversed(roman_values):
        while working.startswith(symbol):
            total += value
            working = working[len(symbol) :]
    return total


def roman_encode(num: int) -> str:
    """
    Encodes an integer into a Roman numeral string.

    Args:
        num (int): The integer to be encoded.

    Returns:
        str: The Roman numeral representation of the input integer.

    Raises:
        ValueError: If the input integer is less than 1 or greater than 3,999.

    Examples:
        >>> roman_encode(1)
        'I'
        >>> roman_encode(9)
        'IX'
        >>> roman_encode(3999)
        'MMMCMXCIX'
    """

    roman_digits = "ivxlcdm"
    return_roman = ""

    if num <= 0:
        raise ValueError("Number too small for Roman numeral encoding. Less than 1")
    if num > 3999:
        raise ValueError(
            "Number too large for Roman numeral encoding. Greater than 3,999"
        )
    for rdix in range(0, len(roman_digits), 2):
        if num == 0:
            break
        num, r = divmod(num, 10)
        v, r = divmod(r, 5)
        if r == 4:
            return_roman += roman_digits[rdix + 1 + v] + roman_digits[rdix]
        else:
            return_roman += r * roman_digits[rdix] + (
                roman_digits[rdix + 1] if (v == 1) else ""
            )
    return (return_roman[-1::-1]).upper()


def main():  # pragma: no cover
    """
    Main function to test the roman_encode and roman_decode functions.

    This function is not tested by pytest or coverage. If you want to
    test this function, you will need to write a test for it and remove
    the pragma: no cover comment above.
    """
    # Test cases for roman_decode
    for value1 in "MCMXC", "MMVIII", "MDCLXVI", "lxviv":
        print(f"Input:{value1} Output: {roman_decode(value1)}")
    del value1  # Remove value1 from the namespace

    # Test cases for roman_encode
    for value2 in 2, 16, 95, 242, 575, 1024, 3999:
        print(f"Input: {value2} Output: {roman_encode(value2)}")
    del value2  # Remove value2 from the namespace

    # Test cases for acceptable_characters
    for value3 in (
        ["MCMXC", "IVXLCDM"],
        ["MCMXA", "IVXLCDM"],
        ["mcmxa", "IVXLCDM"],
        ["mcmxc", "IVXLCDM"],
        ["mcmxi", "ivxlcdm"],
        ["mcmxc", "ivxlcdm"],
    ):
        print(f"Input: {value3} Output: {acceptable_characters(value3[0], value3[1])}")
    del value3  # Remove value3 from the namespace

    print(emoji.emojize("Done :white_check_mark:", language="alias"))


if __name__ == "__main__":
    # This code only runs when this module is executed as a script.
    # It does not run when imported as a module.
    #
    # This code is not tested by coverage. The exclusion is in the
    # pyproject.toml file.
    main()
