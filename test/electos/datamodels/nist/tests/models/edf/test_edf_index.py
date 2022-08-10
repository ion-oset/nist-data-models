import pytest

from electos.datamodels.nist.models.base import NistModel
from electos.datamodels.nist.models.edf import ElectionReport
from electos.datamodels.nist.indexes import DocumentIndex, ElementIndex
from electos.datamodels.nist.indexes.document_index import IndexNode

from tests.utility import load_test_json, raises, raises_none


# --- Test data

EDF_NAMESPACE = "ElectionResults"


EDF_SAMPLE_FILES = [
    ( "jetsons", "jetsons_main_edf.json" ),
]


# --- Test fixtures

@pytest.fixture(params = EDF_SAMPLE_FILES)
def election_report(request):
    """Pre-load test data and return the election report."""
    package, file = request.param
    data = load_test_json(package, file)
    result = ElectionReport(**data)
    return result


@pytest.fixture()
def element_index(election_report):
    index = ElementIndex(election_report, EDF_NAMESPACE)
    return index


@pytest.fixture()
def document_index(election_report):
    index = DocumentIndex(election_report, EDF_NAMESPACE)
    return index



# --- Test cases
#
# Note: Each test case is derived from a 'BallotStyle' in the election report.

EDF_ID_NAMES = [
    [
        "ballot-marker-1",
        "bedrock-precinct",
        "candidate-cosmo-spacely",
        "candidate-harlan-ellis",
        "candidate-jane-jetson",
        "candidate-rudi-indexer",
        "candidate-spencer-cogswell",
        "contest-ballot-measure-gadget-county-1",
        "contest-ballot-measure-gadget-county-1--selection-no",
        "contest-ballot-measure-gadget-county-1--selection-yes",
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
        "header-ballot-measures",
        "header-control-board-spaceport",
        "header-mayor-orbit-city",
        "party-hadron",
        "party-lepton",
        "person-harlan-ellis",
        "person-jane-jetson",
        "person-rudy-indexer",
        "port-precinct",
        "spacetown-precinct",
    ],
]


EDF_ID_NAMES_STRICT = [
    # Exists
    (
        "downtown-precinct",
        "ElectionResults.ReportingUnit",
        raises_none(),
    ),
    # Doesn't exist
    (
        "uptown-precinct",
        None,
        raises(KeyError),
    ),
]


EDF_ID_TYPES = [
    {
        "ballot-marker-1": "ElectionResults.ReportingDevice",
        "bedrock-precinct": "ElectionResults.ReportingUnit",
        "candidate-cosmo-spacely": "ElectionResults.Candidate",
        "candidate-harlan-ellis": "ElectionResults.Candidate",
        "candidate-jane-jetson": "ElectionResults.Candidate",
        "candidate-rudi-indexer": "ElectionResults.Candidate",
        "candidate-spencer-cogswell": "ElectionResults.Candidate",
        "contest-ballot-measure-gadget-county-1": "ElectionResults.BallotMeasureContest",
        "contest-ballot-measure-gadget-county-1--selection-no": "ElectionResults.BallotMeasureSelection",
        "contest-ballot-measure-gadget-county-1--selection-yes": "ElectionResults.BallotMeasureSelection",
        "contest-control-board-spaceport": "ElectionResults.CandidateContest",
        "contest-control-board-spaceport--selection-harlan-ellis": "ElectionResults.CandidateSelection",
        "contest-control-board-spaceport--selection-jane-jetson": "ElectionResults.CandidateSelection",
        "contest-control-board-spaceport--selection-rudi-indexer": "ElectionResults.CandidateSelection",
        "contest-control-board-spaceport--selection-write-in-1": "ElectionResults.CandidateSelection",
        "contest-control-board-spaceport--selection-write-in-2": "ElectionResults.CandidateSelection",
        "contest-mayor--selection-cosmo-spacely": "ElectionResults.CandidateSelection",
        "contest-mayor--selection-spencer-cogswell": "ElectionResults.CandidateSelection",
        "contest-mayor--selection-write-in": "ElectionResults.CandidateSelection",
        "contest-mayor-orbit-city": "ElectionResults.CandidateContest",
        "downtown-precinct": "ElectionResults.ReportingUnit",
        "gadget-county": "ElectionResults.ReportingUnit",
        "header-ballot-measures": "ElectionResults.Header",
        "header-control-board-spaceport": "ElectionResults.Header",
        "header-mayor-orbit-city": "ElectionResults.Header",
        "party-hadron": "ElectionResults.Party",
        "party-lepton": "ElectionResults.Party",
        "person-harlan-ellis": "ElectionResults.Person",
        "person-jane-jetson": "ElectionResults.Person",
        "person-rudy-indexer": "ElectionResults.Person",
        "port-precinct": "ElectionResults.ReportingUnit",
        "spacetown-precinct": "ElectionResults.ReportingUnit",
    },
]


EDF_TYPE_NAMES = [
    [
        "ElectionResults.BallotMeasureContest",
        "ElectionResults.BallotMeasureSelection",
        "ElectionResults.BallotStyle",
        "ElectionResults.Candidate",
        "ElectionResults.CandidateContest",
        "ElectionResults.CandidateSelection",
        "ElectionResults.DeviceClass",
        "ElectionResults.Election",
        "ElectionResults.ExternalIdentifier",
        "ElectionResults.Header",
        "ElectionResults.InternationalizedText",
        "ElectionResults.LanguageString",
        "ElectionResults.OrderedContest",
        "ElectionResults.OrderedHeader",
        "ElectionResults.Party",
        "ElectionResults.Person",
        "ElectionResults.ReportingDevice",
        "ElectionResults.ReportingUnit",
    ],
]


EDF_TYPE_NAMES_STRICT = [
    # Exists
    (
        "ElectionResults.ReportingUnit",
        "ElectionResults.ReportingUnit",
        raises_none(),
    ),
    # Doesn't exist
    (
        "NotARealType",
        [],
        raises(KeyError),
    ),
]


EDF_TYPE_COUNTS = [
    {
        "ElectionResults.BallotMeasureContest": 1,
        "ElectionResults.BallotMeasureSelection": 2,
        "ElectionResults.BallotStyle": 4,
        "ElectionResults.Candidate": 5,
        "ElectionResults.CandidateContest": 2,
        "ElectionResults.CandidateSelection": 8,
        "ElectionResults.DeviceClass": 1,
        "ElectionResults.Election": 1,
        "ElectionResults.ExternalIdentifier": 10,
        "ElectionResults.Header": 3,
        "ElectionResults.InternationalizedText": 24,
        "ElectionResults.LanguageString": 24,
        "ElectionResults.OrderedContest": 8,
        "ElectionResults.OrderedHeader": 8,
        "ElectionResults.Party": 2,
        "ElectionResults.Person": 3,
        "ElectionResults.ReportingDevice": 1,
        "ElectionResults.ReportingUnit": 5,
    },
]


# --- Tests

# Element Index

@pytest.mark.parametrize("id_names", EDF_ID_NAMES)
def test_element_id_names(id_names, element_index):
    expected = id_names
    actual = sorted(element_index.ids())
    assert actual == expected


@pytest.mark.parametrize("key, value, raises", EDF_ID_NAMES_STRICT)
def test_element_id_invalid_not_strict(key, value, raises, element_index):
    expected = value
    model = element_index.by_id(key)
    actual = model.model__type if isinstance(model, NistModel) else model
    assert actual == expected


@pytest.mark.parametrize("key, value, raises", EDF_ID_NAMES_STRICT)
def test_element_id_invalid_strict(key, value, raises, element_index):
    expected = value
    with raises:
        model = element_index.by_id(key, strict = True)
        actual = model.model__type if isinstance(model, NistModel) else model
        assert actual == expected


@pytest.mark.parametrize("id_types", EDF_ID_TYPES)
def test_element_id_types(id_types, element_index):
    expected = id_types
    actual = {}
    for key in sorted(element_index.ids()):
        model = element_index.by_id(key)
        actual[key] = model.model__type
    assert actual == expected


@pytest.mark.parametrize("key, value, raises", EDF_TYPE_NAMES_STRICT)
def test_element_type_invalid_not_strict(key, value, raises, element_index):
    expected = value
    models = list(element_index.by_type(key))
    actual = models[0].model__type \
        if models and isinstance(models[0], NistModel) else models
    assert actual == expected


@pytest.mark.parametrize("key, value, raises", EDF_TYPE_NAMES_STRICT)
def test_element_type_invalid_strict(key, value, raises, element_index):
    expected = value
    with raises:
        models = list(element_index.by_type(key, strict = True))
        actual = models[0].model__type \
            if models and isinstance(models[0], NistModel) else models
        assert actual == expected


@pytest.mark.parametrize("type_names", EDF_TYPE_NAMES)
def test_element_type_names(type_names, element_index):
    expected = type_names
    actual = sorted(element_index.types())
    assert actual == expected


@pytest.mark.parametrize("type_counts", EDF_TYPE_COUNTS)
def test_element_type_counts(type_counts, element_index):
    expected = type_counts
    actual = {}
    for key in element_index.types():
        items = list(element_index.by_type(key))
        count = len(items)
        actual[key] = count
    assert actual == expected


# Document Index

@pytest.mark.parametrize("id_names", EDF_ID_NAMES)
def test_document_id_names(id_names, document_index):
    expected = id_names
    actual = sorted(document_index.ids())
    assert actual == expected


@pytest.mark.parametrize("key, value, raises", EDF_ID_NAMES_STRICT)
def test_document_id_invalid_not_strict(key, value, raises, document_index):
    expected = value
    model = document_index.by_id(key)
    actual = model.value.model__type \
        if model and isinstance(model.value, NistModel) else model
    assert actual == expected


@pytest.mark.parametrize("key, value, raises", EDF_ID_NAMES_STRICT)
def test_document_id_invalid_strict(key, value, raises, document_index):
    expected = value
    with raises:
        model = document_index.by_id(key, strict = True)
        actual = model.value.model__type \
            if model and isinstance(model.value, NistModel) else model
        assert actual == expected


@pytest.mark.parametrize("id_types", EDF_ID_TYPES)
def test_document_id_types(id_types, document_index):
    expected = id_types
    actual = {}
    for key in document_index.ids():
        model = document_index.by_id(key).value
        actual[key] = model.model__type
    assert actual == expected


@pytest.mark.parametrize("key, value, raises", EDF_TYPE_NAMES_STRICT)
def test_document_type_invalid_not_strict(key, value, raises, document_index):
    expected = value
    models = list(document_index.by_type(key))
    actual = models[0].value.model__type \
        if models and isinstance(models[0].value, NistModel) else models
    assert actual == expected


@pytest.mark.parametrize("key, value, raises", EDF_TYPE_NAMES_STRICT)
def test_document_type_invalid_strict(key, value, raises, document_index):
    expected = value
    with raises:
        models = list(document_index.by_type(key, strict = True))
        actual = models[0].value.model__type \
            if models and isinstance(models[0].value, NistModel) else models
        assert actual == expected


@pytest.mark.parametrize("type_names", EDF_TYPE_NAMES)
def test_document_type_names(type_names, document_index):
    expected = type_names
    actual = sorted(document_index.types())
    assert actual == expected


@pytest.mark.parametrize("type_counts", EDF_TYPE_COUNTS)
def test_document_type_counts(type_counts, document_index):
    expected = type_counts
    actual = {}
    for key in document_index.types():
        items = list(document_index.by_type(key))
        count = len(items)
        actual[key] = count
    assert actual == expected
