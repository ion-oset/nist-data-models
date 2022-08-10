import pytest

from electos.datamodels.nist.models.base import NistModel
from electos.datamodels.nist.models.cvr import CastVoteRecordReport
from electos.datamodels.nist.indexes import DocumentIndex, ElementIndex

from tests.utility import load_test_json, raises, raises_none


# --- Test data

CVR_NAMESPACE = "CVR"


CVR_SAMPLE_FILES = [
    ( "jetsons", "jetsons_main_cvr.json" ),
]


# --- Test fixtures

@pytest.fixture(params = CVR_SAMPLE_FILES)
def cast_vote_record_report(request):
    """Pre-load test data and return the cast vote record report."""
    package, file = request.param
    data = load_test_json(package, file)
    result = CastVoteRecordReport(**data)
    return result


@pytest.fixture()
def element_index(cast_vote_record_report):
    index = ElementIndex(cast_vote_record_report, CVR_NAMESPACE)
    return index


@pytest.fixture()
def document_index(cast_vote_record_report):
    index = DocumentIndex(cast_vote_record_report, CVR_NAMESPACE)
    return index


# --- Test cases
#
# Note: Each test case is derived from a 'BallotStyle' in the election report.

CVR_ID_NAMES = [
    [
        "ballot-marker-1",
        "bedrock-precinct",
        "candidate-cosmo-spacely",
        "candidate-harlan-ellis",
        "candidate-jane-jetson",
        "candidate-rudi-indexer",
        "candidate-spencer-cogswell",
        "contest-ballot-measure-1--selection-no",
        "contest-ballot-measure-1--selection-yes",
        "contest-ballot-measure-gadget-county-1",
        "contest-control-board-spaceport",
        "contest-control-board-spaceport--selection-harlan-ellis",
        "contest-control-board-spaceport--selection-jane-jetson",
        "contest-control-board-spaceport--selection-rudi-indexer",
        "contest-control-board-spaceport--selection-write-in-1",
        "contest-control-board-spaceport--selection-write-in-2",
        "contest-mayor--selection-cosmo-spacely",
        "contest-mayor--selection-spencer-cogswell",
        "contest-mayor--selection-write-in",
        "contest-mayor-orbit-city",
        "downtown-precinct",
        "gadget-county",
        "gadget-county-2021-06",
        "party-hadron",
        "party-lepton",
        "port-precinct",
        "snapshot-01",
        "spacetown-precinct",
    ],
]


CVR_ID_NAMES_STRICT = [
    # Exists
    (
        "downtown-precinct",
        "CVR.GpUnit",
        raises_none(),
    ),
    # Doesn't exist
    (
        "uptown-precinct",
        None,
        raises(KeyError),
    ),
]


CVR_ID_TYPES = [
    {
        "ballot-marker-1": "ReportingDevice",
        "bedrock-precinct": "GpUnit",
        "candidate-cosmo-spacely": "Candidate",
        "candidate-harlan-ellis": "Candidate",
        "candidate-jane-jetson": "Candidate",
        "candidate-rudi-indexer": "Candidate",
        "candidate-spencer-cogswell": "Candidate",
        "contest-ballot-measure-1--selection-no": "BallotMeasureSelection",
        "contest-ballot-measure-1--selection-yes": "BallotMeasureSelection",
        "contest-ballot-measure-gadget-county-1": "BallotMeasureContest",
        "contest-control-board-spaceport": "CandidateContest",
        "contest-control-board-spaceport--selection-harlan-ellis": "CandidateSelection",
        "contest-control-board-spaceport--selection-jane-jetson": "CandidateSelection",
        "contest-control-board-spaceport--selection-rudi-indexer": "CandidateSelection",
        "contest-control-board-spaceport--selection-write-in-1": "CandidateSelection",
        "contest-control-board-spaceport--selection-write-in-2": "CandidateSelection",
        "contest-mayor--selection-cosmo-spacely": "CandidateSelection",
        "contest-mayor--selection-spencer-cogswell": "CandidateSelection",
        "contest-mayor--selection-write-in": "CandidateSelection",
        "contest-mayor-orbit-city": "CandidateContest",
        "downtown-precinct": "GpUnit",
        "gadget-county": "GpUnit",
        "gadget-county-2021-06": "Election",
        "party-hadron": "Party",
        "party-lepton": "Party",
        "port-precinct": "GpUnit",
        "snapshot-01": "CVRSnapshot",
        "spacetown-precinct": "GpUnit",
    },
]


CVR_TYPE_NAMES = [
    [
        "CVR.BallotMeasureContest",
        "CVR.BallotMeasureSelection",
        "CVR.CVR",
        "CVR.CVRContest",
        "CVR.CVRContestSelection",
        "CVR.CVRSnapshot",
        "CVR.CVRWriteIn",
        "CVR.Candidate",
        "CVR.CandidateContest",
        "CVR.CandidateSelection",
        "CVR.Election",
        "CVR.GpUnit",
        "CVR.Party",
        "CVR.ReportingDevice",
        "CVR.SelectionPosition",
    ],
]


CVR_TYPE_NAMES_STRICT = [
    # Exists
    (
        "CVR.GpUnit",
        "CVR.GpUnit",
        raises_none(),
    ),
    # Doesn't exist
    (
        "NotARealType",
        [],
        raises(KeyError),
    ),
]


CVR_TYPE_COUNTS = [
    {
        "CVR.BallotMeasureContest": 1,
        "CVR.BallotMeasureSelection": 2,
        "CVR.CVR": 4,
        "CVR.CVRContest": 8,
        "CVR.CVRContestSelection": 10,
        "CVR.CVRSnapshot": 4,
        "CVR.CVRWriteIn": 1,
        "CVR.Candidate": 5,
        "CVR.CandidateContest": 2,
        "CVR.CandidateSelection": 8,
        "CVR.Election": 1,
        "CVR.GpUnit": 5,
        "CVR.Party": 2,
        "CVR.ReportingDevice": 1,
        "CVR.SelectionPosition": 10,
    },
]


# --- Tests

# Element Index

@pytest.mark.parametrize("id_names", CVR_ID_NAMES)
def test_element_id_names(id_names, element_index):
    expected = id_names
    actual = sorted(element_index.ids())
    assert actual == expected


@pytest.mark.parametrize("key, value, raises", CVR_ID_NAMES_STRICT)
def test_element_id_invalid_not_strict(key, value, raises, element_index):
    expected = value
    model = element_index.by_id(key)
    actual = model.model__type if isinstance(model, NistModel) else model
    assert actual == expected


@pytest.mark.parametrize("key, value, raises", CVR_ID_NAMES_STRICT)
def test_element_id_invalid_strict(key, value, raises, element_index):
    expected = value
    with raises:
        model = element_index.by_id(key, strict = True)
        actual = model.model__type if isinstance(model, NistModel) else model
        assert actual == expected


@pytest.mark.parametrize("id_types", CVR_ID_TYPES)
def test_element_id_types(id_types, element_index):
    expected = id_types
    actual = {}
    start = len(CVR_NAMESPACE) + 1
    for key in sorted(element_index.ids()):
        value = element_index.by_id(key)
        value = value.model__type[start:]
        actual[key] = value
    assert actual == expected


@pytest.mark.parametrize("key, value, raises", CVR_TYPE_NAMES_STRICT)
def test_element_type_invalid_not_strict(key, value, raises, element_index):
    expected = value
    models = list(element_index.by_type(key))
    actual = models[0].model__type \
        if models and isinstance(models[0], NistModel) else models
    assert actual == expected


@pytest.mark.parametrize("key, value, raises", CVR_TYPE_NAMES_STRICT)
def test_element_type_invalid_strict(key, value, raises, element_index):
    expected = value
    with raises:
        models = list(element_index.by_type(key, strict = True))
        actual = models[0].model__type \
            if models and isinstance(models[0], NistModel) else models
        assert actual == expected


@pytest.mark.parametrize("type_names", CVR_TYPE_NAMES)
def test_element_type_names(type_names, element_index):
    expected = type_names
    actual = sorted(element_index.types())
    assert actual == expected


@pytest.mark.parametrize("type_counts", CVR_TYPE_COUNTS)
def test_element_type_counts(type_counts, element_index):
    expected = type_counts
    actual = {}
    for key in element_index.types():
        items = list(element_index.by_type(key))
        value = len(items)
        actual[key] = value
    assert actual == expected


# Document Index

@pytest.mark.parametrize("id_names", CVR_ID_NAMES)
def test_document_id_names(id_names, document_index):
    expected = id_names
    actual = sorted(document_index.ids())
    assert actual == expected


@pytest.mark.parametrize("key, value, raises", CVR_ID_NAMES_STRICT)
def test_document_id_invalid_not_strict(key, value, raises, document_index):
    expected = value
    model = document_index.by_id(key)
    actual = model.value.model__type \
        if model and isinstance(model.value, NistModel) else model
    assert actual == expected


@pytest.mark.parametrize("key, value, raises", CVR_ID_NAMES_STRICT)
def test_document_id_invalid_strict(key, value, raises, document_index):
    expected = value
    with raises:
        model = document_index.by_id(key, strict = True)
        actual = model.value.model__type \
            if model and isinstance(model.value, NistModel) else model
        assert actual == expected


@pytest.mark.parametrize("id_types", CVR_ID_TYPES)
def test_document_id_types(id_types, document_index):
    expected = id_types
    actual = {}
    start = len(CVR_NAMESPACE) + 1
    for key in document_index.ids():
        value = document_index.by_id(key).value
        value = value.model__type[start:]
        actual[key] = value
    assert actual == expected


@pytest.mark.parametrize("key, value, raises", CVR_TYPE_NAMES_STRICT)
def test_document_type_invalid_not_strict(key, value, raises, document_index):
    expected = value
    models = list(document_index.by_type(key))
    actual = models[0].value.model__type \
        if models and isinstance(models[0].value, NistModel) else models
    assert actual == expected


@pytest.mark.parametrize("key, value, raises", CVR_TYPE_NAMES_STRICT)
def test_document_type_invalid_strict(key, value, raises, document_index):
    expected = value
    with raises:
        models = list(document_index.by_type(key, strict = True))
        actual = models[0].value.model__type \
            if models and isinstance(models[0].value, NistModel) else models
        assert actual == expected


@pytest.mark.parametrize("type_names", CVR_TYPE_NAMES)
def test_document_type_names(type_names, document_index):
    expected = type_names
    actual = sorted(document_index.types())
    assert actual == expected


@pytest.mark.parametrize("type_counts", CVR_TYPE_COUNTS)
def test_document_type_counts(type_counts, document_index):
    expected = type_counts
    actual = {}
    for key in document_index.types():
        items = list(document_index.by_type(key))
        value = len(items)
        actual[key] = value
    assert actual == expected
