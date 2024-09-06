import itertools
from typing import Union, Optional


def my_func():
    return "Hello World"


def is_leap_year(year):
    """Takes a year as an integer and returns
    true if it is a leap year and false if it
    is not a leap year.
    """
    if year % 100 == 0 and year % 400 == 0:
        return True
    elif year % 100 != 0 and year % 4 == 0:
        return True
    else:
        return False


def get_datetime_string(month, day, year):
    """This function recieves a month, day,
    and year as integers and formats a return
    string in the format 'MM-DD-YYY'.
    """
    datetime = ""
    if month < 10:
        datetime += "0"
    datetime += str(month)
    datetime += "-"
    if day < 10:
        datetime += "0"
    datetime += str(day)
    datetime += "-"
    datetime += str(year)
    return datetime


def my_datetime(num_sec):
    """This function recieves an integer representing
    the number of seconds after the epoch, which is
    January 1st, 1970. This function assumes it is
    initially midnight.
    """
    days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]   # Stores the days for each month

    EPOCH_DAY = 1
    EPOCH_MONTH = 1
    EPOCH_YEAR = 1970
    SEC_PER_DAY = 60 * 60 * 24
    MONTHS_PER_YEAR = 12

    day = EPOCH_DAY
    month = EPOCH_MONTH
    year = EPOCH_YEAR
    total_days = num_sec // SEC_PER_DAY

    # Iterates through every day and calculates date.
    while total_days > 0:
        total_days -= 1
        day += 1
        if month == 2 and is_leap_year(year):       # Account for leap year.
            if day > days_per_month[month - 1] + 1:
                day = 1
                month += 1
        elif day > days_per_month[month - 1]:
            day = 1
            month += 1
        if month > MONTHS_PER_YEAR:
            month = 1
            year += 1

    # Organizes the day, month, and year variables as a string.
    datetime = get_datetime_string(month, day, year)

    return datetime


def get_hex_digit(num):
    """Take a decimal number and turn it into a hex digit
    Only works properly for numbers between 0 and 15
    """
    match num:
        case 10:
            return "A"
        case 11:
            return "B"
        case 12:
            return "C"
        case 13:
            return "D"
        case 14:
            return "E"
        case 15:
            return "F"

    return chr(num + 48)


def is_negative_int(num):
    """Takes in an integer as num
    Returns the positive version of num and True if num is negative
    Return num and False if num is positive
    """
    return (num * -1, True) if num < 0 else (num, False)


def conv_endian(num, endian="big"):
    """Return a hexadecimal number converted from an integer

    Inputs can be negative

    The value of endian will determine whether the returned
    value is stored with big or little endianess

    Any value of endian other than big or little will return None

    In the returned value, each byte will be separated by a space

    Each byte will be two characters in length
    """
    if endian != "big" and endian != "little":
        return None

    num, is_negative = is_negative_int(num)

    # Convert The number in decimal to hex
    num_in_hex = ""
    while num != 0:
        remainder = num % 16
        num_in_hex = get_hex_digit(remainder) + num_in_hex
        num = num // 16

    # Make the return value have an even number of hex digits
    if len(num_in_hex) % 2 == 1:
        num_in_hex = "0" + num_in_hex

    # If little endian, reverse the order
    if endian == "little":
        little_endian = ""
        for i in range(2, len(num_in_hex) + 1, 2):
            little_endian = num_in_hex[i - 2:i] + little_endian
        num_in_hex = little_endian

    num_hex_spaces = ""
    # Put spaces between each two hex digits
    for i in range(2, len(num_in_hex) + 1, 2):
        num_hex_spaces += num_in_hex[i - 2:i] + " "

    # Trim space at the end
    num_hex_spaces = num_hex_spaces[: len(num_hex_spaces) - 1]

    # If the number should be negative, make it negative
    if is_negative:
        num_hex_spaces = "-" + num_hex_spaces

    return num_hex_spaces


def conv_num(num_str):
    """Return a base 10 number, converted from input string.

    All inputs may be made negative by prefixing '-'.
    Inputs may be floating point or integers.
    (Case-insensitive) hexadecimal input is allowed with prefix '0x'
        - after a possible negative sign
    Ill-formed strings always return 'None'. This includes:
        Multiple decimal points
        Unexpected alpha without proper 0x prefix
        Non-string and empty string values
    """
    # Empty strings or non-string inputs are always improper.
    if not isinstance(num_str, str) or len(num_str) == 0:
        return None
    # Well-formed negatives must always have '-' in the very front
    num_str, is_negative = _has_neg_prefix(num_str)
    # Well-formed hex must have 0x or 0X in the very front, OR after a `-`
    num_str, base = _has_hex_prefix(num_str)

    # We may be left with '' after any prefix or ill-formed numbers like '-'
    # These will drop through the helper and return None. Probably not worth
    # The extra logic to sort it out now?
    if len(num_str) == 0:
        return None

    decimal_index = None
    # Not sure I can use str.split(), so I'll use this to separate int/frac parts
    for i, char in enumerate(num_str):
        if char == ".":
            if base == 16:
                # Hex input must be integers only
                return None
            decimal_index = i
            break
    int_str = num_str[:decimal_index]
    frac_str = num_str[(decimal_index + 1):] if decimal_index is not None else None

    int_part = _tally_num(int_str, (len(int_str) - 1), base)
    frac_part = _tally_num(frac_str, -1, base) if frac_str else 0
    if int_part is None or frac_part is None:
        # Both should have at least 0 value or we had an ill-formed input
        return None
    number = int_part + frac_part

    if is_negative and number is not None:
        number = number * -1
    return number


def _has_neg_prefix(num_str: str) -> tuple[str, bool]:
    """Return input without possible leading '-', and bool for presence."""
    return (num_str[1:], True) if num_str.startswith("-") else (num_str, False)


def _has_hex_prefix(num_str: str) -> tuple[str, int]:
    """Return input without possible (0x | 0X), and int reflecting base"""
    if num_str[:2].lower().startswith("0x"):
        return (num_str[2:], 16)
    else:
        return (num_str, 10)


def _tally_num(num_str: str, exp_0: int, base: int) -> Optional[Union[int, float]]:
    """Return float/int from string of numbers, given an exponent to start at.

     Non-ASCII characters are considered ill-formed and cause return of None.

    Args:
        num_str: Any string, should be consecutive digits to be well-formed
        exp_0: Starting exponent to decrement from. Examples:
            -1 for fractional num_str, since '.1' is 1 * 10**-1
            2 for integer num_str length 3, since 123 starts with 1 * 10**2
        base: 10 or 16. Affects the tallying arithmetic, but also valid chars:
            10: 0-9
            16: 0-9, a-f, A-F

    Returns:
        int: well-formed integer num_str where the exponent is always positive
        frac: well-formed fractional num_str where the exponent starts negative
        None: any num_str not well formed: which has unexpected characters not
            resolved to a numeric value.
    """
    value = 0

    for exp, char in zip(itertools.count(exp_0, -1), num_str):
        code_pt = ord(char)
        # ASCII: 0-9 is at DEC 48 - 57 inclusive
        if 48 <= code_pt <= 57:
            value += (code_pt - 48) * (base**exp)
        elif base == 16:
            # ASCII: A-F is at DEC 65 - 70 inclusive
            if 65 <= code_pt <= 70:
                value += (code_pt - 55) * (base**exp)
            # ASCII: a-f is at DEC 97 - 102 inclusive
            elif 97 <= code_pt <= 102:
                value += (code_pt - 87) * (base**exp)
            else:
                return None
        else:
            # Any other character means its ill-formed
            return None
    return value
