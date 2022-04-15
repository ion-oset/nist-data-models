from electos.datamodels.nist.utility.cases import Cases

import pytest


# --- Test data

CAMEL_CASE_SPLIT_TESTS = [
    ( "",       () ),
    ( "_",      () ),
    ( "a",      () ),
    ( "ab",     () ),
    ( "aB",     () ),
    ( "A",      ( "A", ) ),
    ( "AB",     ( "AB", ) ),
    ( "Ab",     ( "Ab", ) ),
    ( "ABC",    ( "ABC", ) ),
    ( "ABc",    ( "A", "Bc" ) ),
    ( "AbC",    ( "Ab", "C" ) ),
    ( "A_B",    ( "A", "_B" ) ),
    ( "A_BC",   ( "A", "_BC" ) ),
    ( "A_Bc",   ( "A", "_Bc" ) ),
    ( "A_b",    ( "A", "_b") ),
    ( "A_bc",   ( "A", "_bc") ),
    ( "_a",     () ),
    ( "_aB",    () ),
    ( "_A",     ( "_A", ) ),
    ( "_Ab",    ( "_Ab", ) ),
    ( "_A_B",   ( "_A", "_B" ) ),
    ( "_A_Bc",  ( "_A", "_Bc" ) ),
]


SNAKE_CASE_SPLIT_TESTS = [
    ( "",       () ),
    # Leading underscores are tokens
    # All other underscores get dropped
    ( "_",      ( "_", ) ),
    ( "__",     ( "__", ) ),
    ( "_a",     ( "_", "a" ) ),
    ( "_ab",    ( "_", "ab" ) ),
    ( "_a_b",   ( "_", "a", "b" ) ),
    ( "_a__b",  ( "_", "a", "b" ) ),
    ( "__a",    ( "__", "a", ) ),
    ( "_a0",    ( "_", "a0" ) ),
    ( "a",      ( "a", ) ),
    ( "ab",     ( "ab", ) ),
    ( "a_b",    ( "a", "b" ) ),
    ( "a__b",   ( "a", "b" ) ),
    ( "0",      () ),
    # ( "0a",     () ),
    # ( "0_a",    () ),
    # ( "_0",     () ),
    # ( "_0a",    () ),
    # ( "_a_0",   ( "_", "a", ) ),
]


CAMEL_TO_SNAKE_TESTS = [
    ( "A",          "a" ),
    ( "Ab",         "ab" ),
    ( "Abc",        "abc" ),
    ( "AB",         "ab" ),
    ( "ABc",        "a_bc" ),
    ( "AbC",        "ab_c" ),
    ( "ABC",        "abc" ),
    ( "AbcDefGhi",  "abc_def_ghi" ),
    ( "ABCDefGhi",  "abc_def_ghi" ),
    ( "Abc123",     "abc123"),
    ( "ABC123",     "abc_123"),
    ( "AbC123",     "ab_c_123"),
]


SNAKE_TO_CAMEL_TESTS = [
    ( "a",           "A" ),
    ( "ab",          "Ab" ),
    ( "abc",         "Abc" ),
    ( "a_b",         "AB" ),
    ( "a_bc",        "ABc" ),
    ( "ab_c",        "AbC" ),
    ( "abc_def_ghi", "AbcDefGhi" ),
]


# --- Test cases


@pytest.mark.parametrize("text,expected", CAMEL_CASE_SPLIT_TESTS)
def test_split_camel_case(text, expected):
    actual = tuple(Cases.split_camel_case(text))
    assert actual == expected


@pytest.mark.parametrize("text,expected", SNAKE_CASE_SPLIT_TESTS)
def test_split_snake_case(text, expected):
    actual = tuple(Cases.split_snake_case(text))
    assert actual == expected


@pytest.mark.parametrize("text,expected", CAMEL_TO_SNAKE_TESTS)
def test_camel_to_snake(text, expected):
    actual = Cases.camel_to_snake(text)
    assert actual == expected


@pytest.mark.parametrize("text,expected", SNAKE_TO_CAMEL_TESTS)
def test_snake_to_camel(text, expected):
    actual = Cases.snake_to_camel(text)
    assert actual == expected
