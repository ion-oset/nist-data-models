import pytest

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


EDF_ID_TYPES = [
    {
        "ballot-marker-1": "ReportingDevice",
        "bedrock-precinct": "ReportingUnit",
        "candidate-cosmo-spacely": "Candidate",
        "candidate-harlan-ellis": "Candidate",
        "candidate-jane-jetson": "Candidate",
        "candidate-rudi-indexer": "Candidate",
        "candidate-spencer-cogswell": "Candidate",
        "contest-ballot-measure-gadget-county-1": "BallotMeasureContest",
        "contest-ballot-measure-gadget-county-1--selection-no": "BallotMeasureSelection",
        "contest-ballot-measure-gadget-county-1--selection-yes": "BallotMeasureSelection",
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
        "downtown-precinct": "ReportingUnit",
        "gadget-county": "ReportingUnit",
        "header-ballot-measures": "Header",
        "header-control-board-spaceport": "Header",
        "header-mayor-orbit-city": "Header",
        "party-hadron": "Party",
        "party-lepton": "Party",
        "person-harlan-ellis": "Person",
        "person-jane-jetson": "Person",
        "person-rudy-indexer": "Person",
        "port-precinct": "ReportingUnit",
        "spacetown-precinct": "ReportingUnit",
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


@pytest.mark.parametrize("id_types", EDF_ID_TYPES)
def test_element_id_types(id_types, element_index):
    expected = id_types
    actual = {}
    start = len(EDF_NAMESPACE) + 1
    for key in id_types.keys():
        value = element_index.by_id(key)
        value = value.model__type[start:]
        actual[key] = value
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
    for key in type_counts.keys():
        items = list(element_index.by_type(key))
        value = len(items)
        actual[key] = value
    assert actual == expected

# Document Index

@pytest.mark.parametrize("id_names", EDF_ID_NAMES)
def test_document_id_names(id_names, document_index):
    expected = id_names
    actual = sorted(document_index.ids())
    assert actual == expected


@pytest.mark.parametrize("id_types", EDF_ID_TYPES)
def test_document_id_types(id_types, document_index):
    expected = id_types
    actual = {}
    start = len(EDF_NAMESPACE) + 1
    for key in id_types.keys():
        value = document_index.by_id(key).value
        value = value.model__type[start:]
        actual[key] = value
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
    for key in type_counts.keys():
        items = list(document_index.by_type(key))
        value = len(items)
        actual[key] = value
    assert actual == expected
