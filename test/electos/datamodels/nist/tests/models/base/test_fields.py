"""Verify that Pydantic strict types work as expected."""

import pytest

from electos.datamodels.nist.models.base import NistModel

from pydantic import StrictBool, StrictFloat, StrictInt, StrictStr
from pydantic import ValidationError

from tests.utility import raises, raises_none


# --- Exception contexts

RAISES_NONE = raises_none()
RAISES_TYPE = raises(ValidationError, match = "type_error.")
RAISES_STRICT_BOOL = raises(ValidationError, match = "value_error.strictbool")


# --- Test classes

class LooselyTyped(NistModel):

    boolean: bool
    integer: int
    number: float
    string: str


class StrictlyTyped(NistModel):

    boolean: StrictBool
    integer: StrictInt
    number: StrictFloat
    string: StrictStr


# --- Test data

TYPED_FIELD_PARAMETERS = {
    "default": {
        "Boolean":  False,
        "Integer":  0,
        "Number":   0.0,
        "String":   "text",
    },
}


# Default value for most loosely typed field tests
TYPED_FIELD_RESULTS = {
    # Expected result for most loosely typed field tests.
    "default": {
        "boolean":  False,
        "integer":  0,
        "number":   0.0,
        "string":   "text",
    },
}


# --- Test cases

# (input parameters, expected results, exception)
LOOSELY_TYPED_FIELD_TESTS = [
    # All fields with expected types
    (
        {},
        TYPED_FIELD_RESULTS["default"],
        RAISES_NONE,
    ),
    # boolean: integer input
    (
        {
            "Boolean": 0,
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_NONE,
    ),
    # boolean: float input
    (
        {
            "Boolean": 0.0,
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_NONE,
    ),
    # boolean: string input
    (
        {
            "Boolean": "",
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_TYPE,
    ),
    # boolean: extended string input (yuck)
    (
        {
            "Boolean": "0",
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_NONE,
    ),
    # boolean: extended string input (yuck)
    (
        {
            "Boolean": "no",
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_NONE,
    ),
    # boolean: list input
    (
        {
            "Boolean": [],
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_TYPE,
    ),
    # boolean: dictionary input
    (
        {
            "Boolean": {},
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_TYPE
    ),
    # integer: boolean input (yuck)
    (
        {
            "Integer": False,
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_NONE,
    ),
    # integer: float input
    (
        {
            "Integer": 0.0,
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_NONE,
    ),
    # integer: string input
    (
        {
            "Integer": "0",
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_NONE,
    ),
    # number: boolean input
    (
        {
            "Number": False,
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_NONE,
    ),
    # number: integer input
    (
        {
            "Number": 0,
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_NONE,
    ),
    # number: string input
    (
        {
            "Number": "0.0",
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_NONE,
    ),
    # string: boolean input
    (
        {
            "String": False,
        },
        {
            "boolean": False,
            "integer": 0,
            "number":  0.0,
            "string":  "False",
        },
        RAISES_NONE,
    ),
    # string: integer input
    (
        {
            "String": 0,
        },
        {
            "boolean": False,
            "integer": 0,
            "number":  0.0,
            "string":  "0",
        },
        RAISES_NONE,
    ),
    # string: float input
    (
        {
            "String": 0.0,
        },
        {
            "boolean": False,
            "integer": 0,
            "number":  0.0,
            "string":  "0.0",
        },
        RAISES_NONE,
    ),
]


# (input parameters, expected results, exception)
STRICTLY_TYPED_FIELD_TESTS = [
    # All fields with expected types
    (
        {},
        TYPED_FIELD_RESULTS["default"],
        RAISES_NONE,
    ),
    # boolean: integer input
    (
        {
            "Boolean": 0,
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_STRICT_BOOL,
    ),
    # boolean: float input
    (
        {
            "Boolean": 0.0,
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_STRICT_BOOL,
    ),
    # boolean: string input
    (
        {
            "Boolean": "",
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_STRICT_BOOL,
    ),
    # boolean: extended string input (yuck)
    (
        {
            "Boolean": "0",
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_STRICT_BOOL,
    ),
    # boolean: extended string input (yuck)
    (
        {
            "Boolean": "no",
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_STRICT_BOOL,
    ),
    # boolean: list input
    (
        {
            "Boolean": [],
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_STRICT_BOOL,
    ),
    # boolean: dictionary input
    (
        {
            "Boolean": {},
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_STRICT_BOOL,
    ),
    # integer: boolean input (yuck)
    (
        {
            "Integer": False,
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_TYPE,
    ),
    # integer: float input
    (
        {
            "Integer": 0.0,
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_TYPE,
    ),
    # integer: string input
    (
        {
            "Integer": "0",
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_TYPE,
    ),
    # number: boolean input
    (
        {
            "Number": False,
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_TYPE,
    ),
    # number: integer input
    (
        {
            "Number": 0,
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_TYPE,
    ),
    # number: string input
    (
        {
            "Number": "0.0",
        },
        TYPED_FIELD_RESULTS["default"],
        RAISES_TYPE,
    ),
    # string: boolean input
    (
        {
            "String": False,
        },
        {
            "boolean": False,
            "integer": 0,
            "number":  0.0,
            "string":  "False",
        },
        RAISES_TYPE,
    ),
    # string: integer input
    (
        {
            "String": 0,
        },
        {
            "boolean": False,
            "integer": 0,
            "number":  0.0,
            "string":  "0",
        },
        RAISES_TYPE,
    ),
    # string: float input
    (
        {
            "String": 0.0,
        },
        {
            "boolean": False,
            "integer": 0,
            "number":  0.0,
            "string":  "0.0",
        },
        RAISES_TYPE,
    ),
]


# --- Tests

@pytest.mark.parametrize("parameters,expected,raises", LOOSELY_TYPED_FIELD_TESTS)
def test_loosely_typed_fields(parameters, expected, raises):
    with raises as ex:
        inputs = TYPED_FIELD_PARAMETERS["default"].copy()
        inputs.update(parameters)
        model = LooselyTyped(**inputs)
        actual = model.dict()
        assert actual == expected


@pytest.mark.parametrize("parameters,expected,raises", STRICTLY_TYPED_FIELD_TESTS)
def test_strictly_typed_fields(parameters, expected, raises):
    with raises as ex:
        inputs = TYPED_FIELD_PARAMETERS["default"].copy()
        inputs.update(parameters)
        model = StrictlyTyped(**inputs)
        actual = model.dict()
        assert actual == expected
