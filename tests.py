import unittest
import datetime
import random
from task import conv_num, conv_endian, my_datetime


class TestCase(unittest.TestCase):
    def test1(self):
        self.assertTrue(True)


class TestConv_Endian(unittest.TestCase):
    # The first 7 tests are what was included in the assignment
    def test_pos_big(self):
        """Tests a positive integer with big endianess
        PASS: correctly converts positive integers to big endian
        FAIL: does not correctly convert positive integers to big endian
        """
        str_in = 954786
        endianess = "big"
        expected = "0E 91 A2"
        self.assertEqual(conv_endian(str_in, endianess), expected)

    def test_pos_no_endian(self):
        """Tests a positive integer with no argument for endian
        PASS: correctly converts positive integers to big endian
        FAIL: does not correctly convert positive integers to big endian
        """
        str_in = 954786
        expected = "0E 91 A2"
        self.assertEqual(conv_endian(str_in), expected)

    def test_neg_no_endian(self):
        """Tests a negative integer with no argument for endian
        PASS: correctly converts negative integers to big endian
        FAIL: does not correctly convert negative integers to big endian
        """
        str_in = -954786
        expected = "-0E 91 A2"
        self.assertEqual(conv_endian(str_in), expected)

    def test_pos_little(self):
        """Tests a positive integer with little endianess
        PASS: correctly converts positive integers to little endian
        FAIL: does not correctly convert positive integers to little endian
        """
        str_in = 954786
        endianess = "little"
        expected = "A2 91 0E"
        self.assertEqual(conv_endian(str_in, endianess), expected)

    def test_neg_little(self):
        """Tests a negative integer with little endianess
        PASS: correctly converts negative integers to little endian
        FAIL: does not correctly convert negative integers to little endian
        """
        str_in = -954786
        endianess = "little"
        expected = "-A2 91 0E"
        self.assertEqual(conv_endian(str_in, endianess), expected)

    def test_named_args(self):
        """Tests a negative integer with little endianess and named args
        PASS: correctly converts negative integers to little endian
        FAIL: does not correctly convert negative integers to little endian
        """
        str_in = -954786
        endianess = "little"
        expected = "-A2 91 0E"
        self.assertEqual(conv_endian(num=str_in, endian=endianess), expected)

    def test_bad_endian(self):
        """Tests a bad value for endian
        PASS: correctly rejects bad endian value
        FAIL: does not correctly reject bad endian value
        """
        str_in = -954786
        endianess = "small"
        expected = None
        self.assertEqual(conv_endian(num=str_in, endian=endianess), expected)

    # Tests I have written myself
    def test_small_big(self):
        """Tests whether small positive values with big endian
        PASS: correctly converts small positive values to big endian
        FAIL: does not correctly convert small positive values to big endian
        """
        str_in = 1
        endianess = "big"
        expected = "01"
        self.assertEqual(conv_endian(str_in, endianess), expected)

    def test_neg_small_big(self):
        """Tests whether small negative values with big endian
        PASS: correctly converts small negative values to big endian
        FAIL: does not correctly convert small negative values to big endian
        """
        str_in = -1
        endianess = "big"
        expected = "-01"
        self.assertEqual(conv_endian(str_in, endianess), expected)

    def test_small_little(self):
        """Tests whether small positive values with little endian
        PASS: correctly converts small positive values to little endian
        FAIL: does not correctly convert small positive values to little endian
        """
        str_in = 1
        endianess = "little"
        expected = "01"
        self.assertEqual(conv_endian(str_in, endianess), expected)

    def test_neg_small_little(self):
        """Tests whether small negative values with little endian
        PASS: correctly converts small negative values to little endian
        FAIL: does not correctly convert small negative values to little endian
        """
        str_in = -1
        endianess = "little"
        expected = "-01"
        self.assertEqual(conv_endian(str_in, endianess), expected)

    def test_four_byte(self):
        """Tests whether larger values get converted to big endian correctly
        PASS: correctly converts larger values to big endian
        FAIL: does not correctly convert larger values to big endian
        """
        str_in = 841237594
        endianess = "big"
        expected = "32 24 44 5A"
        self.assertEqual(conv_endian(str_in, endianess), expected)


class TestConv_Num(unittest.TestCase):
    # These 9 tests are taken from the Canvas assignment page. Not mine!
    def test_ex0_int(self):
        str_in = "12345"
        expected = 12345
        self.assertEqual(conv_num(str_in), expected)

    def test_ex1_neg_float(self):
        str_in = "-123.45"
        expected = -123.45
        self.assertEqual(conv_num(str_in), expected)

    def test_ex2_float_no_lead(self):
        str_in = ".45"
        expected = 0.45
        self.assertEqual(conv_num(str_in), expected)

    def test_ex3_float_no_end(self):
        str_in = "123."
        expected = 123.0
        self.assertEqual(conv_num(str_in), expected)

    def test_ex4_hex_upper(self):
        str_in = "0xAD4"
        expected = 2772
        self.assertEqual(conv_num(str_in), expected)

    def test_ex5_hex_lower(self):
        # Note the hex prefix must also be case insensitive!
        str_in = "0Xad4"
        expected = 2772
        self.assertEqual(conv_num(str_in), expected)

    def test_ex6_bad_alpha(self):
        str_in = "12345A"
        expected = None
        self.assertEqual(conv_num(str_in), expected)

    def test_ex7_bad_decimal(self):
        str_in = "12.3.45"
        expected = None
        self.assertEqual(conv_num(str_in), expected)

    # These tests are not from Canvas anymore.
    # By the spec, empty strings and wrong types are 'None' returns.
    def test_empty(self):
        str_in = ""
        expected = None
        self.assertEqual(conv_num(str_in), expected)

    def test_wrong_input_type(self):
        not_str_in = bytes.fromhex("09F911029D74E35BD84156C5635688C0")
        expected = None
        self.assertEqual(conv_num(not_str_in), expected)

    # Tests for short strings, might confuse my shoddy prefix handling
    # Ints and float of length 1 & 2 (numeric content) are all tested for safety
    def test_short_i1(self):
        str_in = "1"
        expected = 1
        self.assertEqual(conv_num(str_in), expected)

    def test_short_i2(self):
        str_in = "12"
        expected = 12
        self.assertEqual(conv_num(str_in), expected)

    def test_short_neg_i1(self):
        str_in = "-1"
        expected = -1
        self.assertEqual(conv_num(str_in), expected)

    def test_short_neg_i2(self):
        str_in = "-12"
        expected = -12
        self.assertEqual(conv_num(str_in), expected)

    def test_short_f1(self):
        str_in = ".1"
        expected = 0.1
        self.assertEqual(conv_num(str_in), expected)

    def test_short_neg_f1(self):
        str_in = "-.1"
        expected = -0.1
        self.assertEqual(conv_num(str_in), expected)

    def test_short_f2(self):
        str_in = ".14"
        expected = 0.14
        self.assertEqual(conv_num(str_in), expected)

    def test_short_neg_f2(self):
        str_in = "-.19"
        expected = -0.19
        self.assertEqual(conv_num(str_in), expected)

    # Tests that are just prefixes without numeric content
    # Instructor confirmed these cases should be None
    def test_only_neg(self):
        str_in = "-"
        expected = None
        self.assertEqual(conv_num(str_in), expected)

    def test_only_hex(self):
        str_in = "0x"
        expected = None
        self.assertEqual(conv_num(str_in), expected)

    def test_only_hex_neg(self):
        str_in = "-0x"
        expected = None
        self.assertEqual(conv_num(str_in), expected)

    # More Hex tests
    # By the spec, fractional Hex is not allowed
    def test_frac_hex(self):
        str_in = "0xad4.ff"
        expected = None
        self.assertEqual(conv_num(str_in), expected)

    def test_neg_hex(self):
        str_in = "-0x1E240"
        expected = -123456
        self.assertEqual(conv_num(str_in), expected)

    # Can't think of any reason why upper AND lower wouldn't work, but eh
    def test_spongecase_hex(self):
        str_in = "0XdaBbAD00"
        expected = 3669732608
        self.assertEqual(conv_num(str_in), expected)

    def test_hex_0(self):
        str_in = "0X0"
        expected = 0
        self.assertEqual(conv_num(str_in), expected)

    def test_hex_neg_0(self):
        str_in = "-0X0"
        expected = 0
        self.assertEqual(conv_num(str_in), expected)

    # These tests probe the bounds of the ASCII -> value mapping logic
    # Anything +/- 1 the ranges of 0-9, a-f, and A-F must return None
    def test_no_under_0(self):
        str_in = "9/10"
        expected = None
        self.assertEqual(conv_num(str_in), expected)

    def test_no_above_9(self):
        str_in = "650:"
        expected = None
        self.assertEqual(conv_num(str_in), expected)

    def test_no_below_A(self):
        str_in = "0x5@90"
        expected = None
        self.assertEqual(conv_num(str_in), expected)

    def test_no_above_F(self):
        str_in = "0XadG4"
        expected = None
        self.assertEqual(conv_num(str_in), expected)

    def test_no_below_a(self):
        str_in = "0x5`90"
        expected = None
        self.assertEqual(conv_num(str_in), expected)

    def test_no_above_f(self):
        str_in = "0Xadg4"
        expected = None
        self.assertEqual(conv_num(str_in), expected)


class TestMy_Datetime(unittest.TestCase):
    # These first four tests are taken from the Canvas assignment page.
    def test_zero_seconds(self):
        """Tests whether the number of seconds that equates
        to the epoch date (0 seconds) returns the epoch date.
        """
        num_sec = 0
        expected = "01-01-1970"
        self.assertEqual(my_datetime(num_sec), expected)

    def test_year_after_leap(self):
        """Tests whether the number of seconds that equates
        to the year after a leap year returns the correct
        date.
        """
        num_sec = 123456789
        expected = "11-29-1973"
        self.assertEqual(my_datetime(num_sec), expected)

    def test_year_between_leaps(self):
        """Tests whether the number of seconds that equates
        to the year between leap years returns the correct
        date.
        """
        num_sec = 9876543210
        expected = "12-22-2282"
        self.assertEqual(my_datetime(num_sec), expected)

    def test_leap_day(self):
        """Tests whether the number of seconds that equates
        to the extra day in a leap year returns the correct
        date with February 29th as the month and day.
        """
        num_sec = 201653971200
        expected = "02-29-8360"
        self.assertEqual(my_datetime(num_sec), expected)


def build_my_datetime_test_func(expected, test_case, func_under_test, message):
    def test(self):
        result = func_under_test(test_case)
        self.assertEqual(expected, result, message.format(test_case, expected, result))
    return test


def generate_my_datetime_testcases(tests_to_generate=500):
    """This function generates a random number of seconds
    and formatted expected return string to build random
    tests that verify the output of the my_datetime function.
    """
    for i in range(tests_to_generate):
        # Generate random number of seconds
        num_sec = random.randrange(253370764800)

        # Format expected string
        date = str(datetime.date.fromtimestamp(num_sec))
        year = date[slice(4)]
        month = date[slice(5, 7, 1)]
        day = date[slice(8, 10, 1)]
        expected = month + "-" + day + "-" + year

        # Build test function
        message = 'Test case: {}, Expected: {}, Result: {}'
        new_test = build_my_datetime_test_func(expected, num_sec, my_datetime, message)
        setattr(TestMy_Datetime, 'test_{}'.format(num_sec), new_test)


if __name__ == "__main__":
    generate_my_datetime_testcases()
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
