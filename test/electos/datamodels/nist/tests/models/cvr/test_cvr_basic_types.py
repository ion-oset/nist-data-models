import pytest

from electos.datamodels.nist.models.cvr import *

from pydantic import ValidationError

from tests.utility import raises, raises_none


# --- Exception contexts

RAISES_NONE = raises_none()
RAISES_MISSING = raises(ValidationError, match = "value_error.missing")
RAISES_INVALID = raises(ValidationError, match = "value_error.const")
RAISES_TYPE = raises(ValidationError, match = "type_error.")


# --- Test data

FILE_CREATE_TESTS = [
    (
        {},
        RAISES_MISSING,
    ),
    (
        {
            "@type":    "CVR.File",
        },
        RAISES_MISSING,
    ),
    (
        {
            "Data":     "dGV4dA==",
        },
        RAISES_MISSING,
    ),
    (
        {
            "@type":    "CVR.Undefined",
            "Data":     "",
        },
        RAISES_INVALID,
    ),
    (
        {
            "@type":    "CVR.File",
            "Data":     "dGV4dA==",
        },
        RAISES_NONE,
    ),
    (
        {
            "@type":    "CVR.File",
            "Data":     "dGV4dA==",
            "FileName": "filename.txt",
            "MimeType": "text/plain",
        },
        RAISES_NONE,
    ),
    pytest.param(
        {
            "@type":    "CVR.File",
            "Data":     0,
        },
        RAISES_TYPE,
        # marks = pytest.mark.xfail,
    ),
]


FILE_ASSIGN_TESTS = [
    (
        ( "model__type", "@type", "CVR.File" ),
        RAISES_NONE,
    ),
    (
        ( "data", "Data", "PHA+dGV4dDwvcD4=" ),
        RAISES_NONE,
    ),
    (
        ( "file_name", "FileName", "filename.html" ),
        RAISES_NONE,
    ),
    (
        ( "mime_type", "MimeType", "text/html" ),
        RAISES_NONE,
    ),
    (
        ( "model__type", "@type", "CVR.Image" ),
        RAISES_INVALID,
    ),
    (
        ( "model__type", "@type", "CVR.BadType" ),
        RAISES_INVALID,
    ),
    pytest.param(
        ( "data", "Data", "*invalid-base64*"),
        RAISES_MISSING,
        marks = pytest.mark.xfail,
    ),
]


# --- Test fixtures

# Used by constructor tests

@pytest.fixture
def model_type():
    model = File
    return model


# Used by assignment tests

@pytest.fixture
def model_data_required():
    parameters = {
        "@type":    "CVR.File",
        "Data":     "dGV4dA==",
    }
    return parameters


@pytest.fixture
def model_data_all(model_type):
    parameters = {
        "@type":    "CVR.File",
        "Data":     "dGV4dA==",
        "FileName": "filename.txt",
        "MimeType": "text/plain",
    }
    return parameters


# --- Test cases

@pytest.mark.parametrize("parameters,raises", FILE_CREATE_TESTS)
def test_file_create(parameters, raises, model_type):
    Model = model_type
    with raises as ex:
        model = Model(**parameters)
        # TODO: Test actual field values
        # For now that's happening in the assign test.
        # assert getattr(model, field) == parameters.get(alias)


@pytest.mark.parametrize("assigned,raises", FILE_ASSIGN_TESTS)
def test_file_assign_required(assigned, raises, model_type, model_data_required):
    Model = model_type
    parameters = model_data_required
    field, alias, value = assigned
    model = Model(**parameters)
    with raises as ex:
        setattr(model, field, value)
        assert getattr(model, field) == value


@pytest.mark.parametrize("assigned,raises", FILE_ASSIGN_TESTS)
def test_file_assign_all(assigned, raises, model_type, model_data_all):
    Model = model_type
    parameters = model_data_all
    field, alias, value = assigned
    model = Model(**parameters)
    with raises as ex:
        setattr(model, field, value)
        assert getattr(model, field) == value
