import pytest

from electos.datamodels.nist.models.edf import *

from pydantic import ValidationError

from tests.utility import load_test_json, raises, raises_none


# --- Test data

EDF_SAMPLE_FILES = [
    ( "jetsons", "jetsons_main_edf.json" ),
]


# --- Test fixtures

@pytest.fixture(params = EDF_SAMPLE_FILES)
def test_data(request):
    """Pre-load test data and return the ."""
    package, file = request.param
    data = load_test_json(package, file)
    return data


@pytest.fixture()
def election_report(test_data):
    return ElectionReport(**test_data)


@pytest.fixture()
def elections(election_report):
    return [
        election
        for election in election_report.election
    ]


@pytest.fixture()
def election_ballot_styles(elections):
    return [
        ballot_style
        for election in elections
        for ballot_style in election.ballot_style
    ]


@pytest.fixture()
def election_ballot_style_external_ids(election_ballot_styles):
    return [
        external_identifier
        for ballot_style in election_ballot_styles
        for external_identifier in ballot_style.external_identifier
    ]


@pytest.fixture()
def election_ballot_style_gp_unit_ids(election_ballot_styles):
    return [
        gp_unit_id
        for ballot_style in election_ballot_styles
        for gp_unit_id in ballot_style.gp_unit_ids
    ]


@pytest.fixture()
def election_ballot_style_header_ids(election_ballot_styles):
    return [
        container.header_id
        for ballot_style in election_ballot_styles
        for container in ballot_style.ordered_content
    ]


@pytest.fixture()
def election_ballot_style_contest_ids(election_ballot_styles):
    return [
        content.contest_id
        for ballot_style in election_ballot_styles
        for container in ballot_style.ordered_content
        for content in container.ordered_content
    ]


@pytest.fixture()
def election_candidates(elections):
    return [
        candidate
        for election in elections
        for candidate in election.candidate
    ]


@pytest.fixture()
def election_candidate_ballot_names(election_candidates):
    return [
        candidate.ballot_name
        for candidate in election_candidates
    ]


@pytest.fixture()
def election_contests(elections):
    return [
        contest
        for election in elections
        for contest in election.contest
    ]


@pytest.fixture()
def election_contest_selections(election_contests):
    return [
        contest_selection
        for contest in election_contests
        for contest_selection in contest.contest_selection
    ]


@pytest.fixture()
def election_contest_candidates(election_contests):
    return [
        contest
        for contest in election_contests
            if contest.model__type == "ElectionResults.CandidateContest"
    ]


@pytest.fixture()
def election_contest_candidate_selections(election_contest_selections):
    return [
        contest_selection
        for contest_selection in election_contest_selections
            if contest_selection.model__type == "ElectionResults.CandidateSelection"
    ]


@pytest.fixture()
def election_contest_ballot_measures(election_contests):
    return [
        contest
        for contest in election_contests
            if contest.model__type == "ElectionResults.BallotMeasureContest"
    ]


@pytest.fixture()
def election_contest_ballot_measure_selections(election_contest_selections):
    return [
        contest_selection
        for contest_selection in election_contest_selections
            if contest_selection.model__type == "ElectionResults.BallotMeasureSelection"
    ]


@pytest.fixture()
def headers(election_report):
    return [
        header
        for header in election_report.header
    ]


@pytest.fixture()
def parties(election_report):
    return [
        party
        for party in election_report.party
    ]


@pytest.fixture()
def persons(election_report):
    return [
        person
        for person in election_report.person
    ]


@pytest.fixture()
def reporting_units(election_report):
    return [
        unit
        for unit in election_report.gp_unit
            if unit.model__type == "ElectionResults.ReportingUnit"
    ]


@pytest.fixture()
def reporting_devices(election_report):
    return [
        unit
        for unit in election_report.gp_unit
            if unit.model__type == "ElectionResults.ReportingDevice"
    ]


# --- Test cases

ELECTION_TESTS = enumerate([
    {
        "ElectionScopeId": "gadget-county",
        "EndDate": "2021-06-15",
        "Name": {
            "Text": [
                {
                    "Content": "Gadget County Elections",
                    "Language": "en",
                }
            ]
        },
        "StartDate": "2021-06-01",
        "Type": "general",
    },
])


# Ballot styles


ELECTION_BALLOT_STYLE_EXTERNAL_ID_TESTS = enumerate([
    { "Type": "local-level", "Value": "ballot-style-bedrock-precinct" },
    { "Type": "local-level", "Value": "ballot-style-downtown-precinct" },
    { "Type": "local-level", "Value": "ballot-style-port-precinct" },
    { "Type": "local-level", "Value": "ballot-style-spacetown-precinct" },
])


ELECTION_BALLOT_STYLE_GP_UNIT_ID_TESTS = enumerate([
    "bedrock-precinct",
    "downtown-precinct",
    "port-precinct",
    "spacetown-precinct",
])


ELECTION_BALLOT_STYLE_HEADER_ID_TESTS = enumerate([
    "header-ballot-measures",
    "header-mayor-orbit-city",
    "header-ballot-measures",
    "header-control-board-spaceport",
    "header-ballot-measures",
    "header-mayor-orbit-city",
    "header-control-board-spaceport",
    "header-ballot-measures",
])


ELECTION_BALLOT_STYLE_CONTEST_ID_TESTS = enumerate([
    "contest-ballot-measure-gadget-county-1",
    "contest-mayor-orbit-city",
    "contest-ballot-measure-gadget-county-1",
    "contest-control-board-spaceport",
    "contest-ballot-measure-gadget-county-1",
    "contest-mayor-orbit-city",
    "contest-control-board-spaceport",
    "contest-ballot-measure-gadget-county-1",
])


# Candidates


ELECTION_CANDIDATE_ID_TESTS = enumerate([
    "candidate-cosmo-spacely",
    "candidate-spencer-cogswell",
    "candidate-jane-jetson",
    "candidate-harlan-ellis",
    "candidate-rudi-indexer",
])


ELECTION_CANDIDATE_BALLOT_NAME_TESTS = enumerate([
    [ { "Content": "Cosmo Spacely", "Language": "en" } ],
    [ { "Content": "Spencer Cogswell", "Language": "en" } ],
    [ { "Content": "Jane Jetson", "Language": "en" } ],
    [ { "Content": "Harlan Ellis", "Language": "en" } ],
    [ { "Content": "Rudi Indexer", "Language": "en" } ],
])


ELECTION_CANDIDATE_EXTERNAL_ID_TESTS = enumerate([
    [ { "Type": "local-level", "Value": "candidate-cosmo-spacely" } ],
    [ { "Type": "local-level", "Value": "candidate-spencer-cogswell" } ],
    [ { "Type": "local-level", "Value": "candidate-jane-jetson" } ],
    [ { "Type": "local-level", "Value": "candidate-harlan-ellis" } ],
    [ { "Type": "local-level", "Value": "candidate-rudi-indexer" } ],
])


# Candidate Contests


ELECTION_CONTEST_CANDIDATE_TESTS = enumerate([
    {
      "Name": "Mayor of Orbit City",
      "ElectionDistrictId": "gadget-county",
      "VoteVariation": "plurality",
      "VotesAllowed": 1
    },
    {
      "Name": "SpacePort Control Board",
      "ElectionDistrictId": "gadget-county",
      "VoteVariation": "n-of-m",
      "VotesAllowed": 2
    },
])


ELECTION_CONTEST_CANDIDATE_ID_TESTS = enumerate([
    "contest-mayor-orbit-city",
    "contest-control-board-spaceport",
])


ELECTION_CONTEST_CANDIDATE_SELECTION_TESTS = enumerate([
    {
        "@type": "ElectionResults.CandidateSelection",
        "SequenceOrder": 1,
        "CandidateIds": [
            "candidate-cosmo-spacely"
        ],
        "EndorsementPartyIds": [
            "party-lepton"
        ]
    },
    {
        "@type": "ElectionResults.CandidateSelection",
        "SequenceOrder": 2,
        "CandidateIds": [
            "candidate-spencer-cogswell"
        ],
        "EndorsementPartyIds": [
            "party-hadron"
        ]
    },
    {
        "@type": "ElectionResults.CandidateSelection",
        "SequenceOrder": 3,
        "IsWriteIn": True
    }
])


ELECTION_CONTEST_CANDIDATE_SELECTION_ID_TESTS = enumerate([
    "contest-mayor--selection-cosmo-spacely",
    "contest-mayor--selection-spencer-cogswell",
    "contest-mayor--selection-write-in",
    "contest-control-board-spaceport--selection-jane-jetson",
    "contest-control-board-spaceport--selection-harlan-ellis",
    "contest-control-board-spaceport--selection-rudi-indexer",
    "contest-control-board-spaceport--selection-write-in-1",
    "contest-control-board-spaceport--selection-write-in-2",
])


# Ballot Measure Contests


ELECTION_CONTEST_BALLOT_MEASURE_TESTS = enumerate([
    {
      "Name": "Shall Gadget County increase its sales tax from 1% to 1.1% for the "
              "purpose of raising additional revenue to fund expanded air traffic "
              "control operations?",
      "ElectionDistrictId": "gadget-county",
      "VoteVariation": "plurality"
    },
])


ELECTION_CONTEST_BALLOT_MEASURE_ID_TESTS = enumerate([
    "contest-ballot-measure-gadget-county-1",
])


ELECTION_CONTEST_BALLOT_MEASURE_SELECTION_TESTS = enumerate([
    {
        "@type": "ElectionResults.BallotMeasureSelection",
        "SequenceOrder": 1,
        "Selection": [
            { "Content": "Yes", "Language": "en" }
        ]
    },
    {
        "@type": "ElectionResults.BallotMeasureSelection",
        "SequenceOrder": 2,
        "Selection": [
            { "Content": "No", "Language": "en" }
        ]
    }
])


ELECTION_CONTEST_BALLOT_MEASURE_SELECTION_ID_TESTS = enumerate([
    "contest-ballot-measure-gadget-county-1--selection-yes",
    "contest-ballot-measure-gadget-county-1--selection-no",
])


# Election Reports

ELECTION_REPORT_TESTS = enumerate([
    {
        "Format": "summary-contest",
        "GeneratedDate": "2021-06-01T12:00:00-08:00",
        "Issuer": "State",
        "IssuerAbbreviation": "US",
        "SequenceEnd": 1,
        "SequenceStart": 1,
        "Status": "pre-election",
        "VendorApplicationId": "TTV"
    }
])


HEADER_TESTS = enumerate([
    {
        "@id": "header-ballot-measures",
        "Name": [
            { "Content": "Ballot Measures", "Language": "en" }
        ]
    },
    {
        "@id": "header-control-board-spaceport",
        "Name": [
            { "Content": "SpacePort Control Board", "Language": "en" }
        ]
    },
    {
        "@id": "header-mayor-orbit-city",
        "Name": [
            { "Content": "Mayor of Orbit City", "Language": "en" }
        ]
    }
])


PARTY_TESTS = enumerate([
    {
        "@id": "party-hadron",
        "Name": [
            { "Content": "Hadron Party", "Language": "en" }
        ]
    },
    {
        "@id": "party-lepton",
        "Name": [
            { "Content": "Lepton Party", "Language": "en" }
        ]
    },
])


PERSON_TESTS = enumerate([
    {
        "@id": "person-jane-jetson",
        "FullName": [{ "Content": "Jane Jetson", "Language": "en" }],
        "Profession": [{ "Content": "Independent Consultant", "Language": "en" }]
    },
    {
        "@id": "person-harlan-ellis",
        "FullName": [{ "Content": "Harlan Ellis", "Language": "en" }],
        "Profession": [{ "Content": "Author", "Language": "en" }]
    },
    {
        "@id": "person-rudy-indexer",
        "FullName": [{ "Content": "Rudi Indexer", "Language": "en" }],
        "Profession": [{ "Content": "Sentient Search Engine", "Language": "en" }]
    }
])


REPORTING_UNIT_TESTS = enumerate([
    {
        "@id": "gadget-county",
        "Name": [
            { "Content": "Gadget County", "Language": "en" }
        ],
        "Type": "county"
    },
    {
        "@id": "bedrock-precinct",
        "Name": [
            { "Content": "Bedrock Precinct", "Language": "en" }
        ],
        "Type": "precinct"
    },
    {
        "@id": "downtown-precinct",
        "Name": [
            { "Content": "Downtown Precinct", "Language": "en" }
        ],
        "Type": "precinct"
    },
    {
        "@id": "port-precinct",
        "Name": [
            { "Content": "Port Precinct", "Language": "en" }
        ],
        "Type": "precinct"
    },
    {
        "@id": "spacetown-precinct",
        "Name": [
            { "Content": "SpaceTown Precinct", "Language": "en" }
        ],
        "Type": "precinct"
    },
])


REPORTING_DEVICE_TESTS = enumerate([
    {
        "@id": "ballot-marker-1",
        "Manufacturer": "Trust the Vote",
        "Model": "git-c3cd6f4f-20210601",
        "SerialNumber": "AB:CD:EF:12:34:56",
        "Type": "bmd"
    }
])


# --- Tests

@pytest.mark.parametrize("index,item", ELECTION_REPORT_TESTS)
def test_election_report(index, item, election_report):
    """ElectionReport"""
    actual = {
        "Format": election_report.format.value,
        "GeneratedDate": election_report.generated_date.__root__.isoformat(),
        # "GeneratedDate": election_report.generated_date.__root__.strftime(
        #     "%Y-%m-%dT%H:%M:%S%z"
        # ),
        "Issuer": election_report.issuer,
        "IssuerAbbreviation": election_report.issuer_abbreviation,
        "SequenceEnd": election_report.sequence_end,
        "SequenceStart": election_report.sequence_start,
        "Status": election_report.status.value,
        "VendorApplicationId": election_report.vendor_application_id,
    }
    expected = item
    assert actual == expected


@pytest.mark.parametrize("index,item", ELECTION_TESTS)
def test_election(index, item, elections):
    """ElectionReport.Election"""
    election = elections[index]
    actual = {
        "ElectionScopeId": election.election_scope_id,
        "EndDate": election.end_date.strftime("%Y-%m-%d"),
        "Name": {
            "Text": [
                {
                    "Content": _.content,
                    "Language": _.language,
                } for _ in election.name.text
            ]
        },
        "StartDate": election.start_date.strftime("%Y-%m-%d"),
        "Type": election.type.value,
    }
    expected = item
    assert actual == expected


@pytest.mark.parametrize("index,item", ELECTION_BALLOT_STYLE_EXTERNAL_ID_TESTS)
def test_ballot_style_external_ids(index, item, election_ballot_style_external_ids):
    """ElectionReport.Election.BallotStyle.ExternalId"""
    external_identifier = election_ballot_style_external_ids[index]
    actual = {
        "Type": external_identifier.type.value,
        "Value": external_identifier.value,
    }
    expected = item
    assert actual == expected


@pytest.mark.parametrize("index,id", ELECTION_BALLOT_STYLE_GP_UNIT_ID_TESTS)
def test_ballot_style_gp_unit_ids(index, id, election_ballot_style_gp_unit_ids):
    """ElectionReport.Election.BallotStyle.GpUnitIds"""
    gp_unit_id = election_ballot_style_gp_unit_ids[index]
    actual = gp_unit_id
    expected = id
    assert actual == expected


@pytest.mark.parametrize("index,id", ELECTION_BALLOT_STYLE_HEADER_ID_TESTS)
def test_ballot_style_header_ids(index, id, election_ballot_style_header_ids):
    """ElectionReport.Election.BallotStyle.HeaderId"""
    header_id = election_ballot_style_header_ids[index]
    actual = header_id
    expected = id
    assert actual == expected


@pytest.mark.parametrize("index,id", ELECTION_BALLOT_STYLE_CONTEST_ID_TESTS)
def test_ballot_style_contest_ids(index, id, election_ballot_style_contest_ids):
    """ElectionReport.Election.BallotStyle.OrderedContent.OrderedContent.ContestId"""
    contest_id = election_ballot_style_contest_ids[index]
    actual = contest_id
    expected = id
    assert actual == expected


@pytest.mark.parametrize("index,id", ELECTION_CANDIDATE_ID_TESTS)
def test_candidate_ids(index, id, election_candidates):
    """ElectionReport.Election.Candidate["@id"]"""
    candidate = election_candidates[index]
    actual = candidate.model__id
    expected = id
    assert actual == expected


@pytest.mark.parametrize("index,item", ELECTION_CANDIDATE_BALLOT_NAME_TESTS)
def test_candidate_ballot_names(index, item, election_candidate_ballot_names):
    """ElectionReport.Election.Candidate.BallotName"""
    ballot_name = election_candidate_ballot_names[index]
    actual = [
        {
            "Content": _.content,
            "Language": _.language,
        } for _ in ballot_name.text
    ]
    expected = item
    assert actual == expected


@pytest.mark.parametrize("index,item", ELECTION_CANDIDATE_EXTERNAL_ID_TESTS)
def test_candidate_external_ids(index, item, election_candidates):
    """ElectionReport.Election.Candidate.ExternalId"""
    candidate = election_candidates[index]
    external_identifier = candidate.external_identifier
    actual = [
        {
            "Type": _.type.value,
            "Value": _.value,
        } for _ in external_identifier
    ]
    expected = item
    assert actual == expected


@pytest.mark.parametrize("index,item", ELECTION_CONTEST_CANDIDATE_TESTS)
def test_contest_candidates(index, item, election_contest_candidates):
    """ElectionReport.Election.Contest["@type"] == 'ElectionResults.CandidateContest'"""
    candidate_contest = election_contest_candidates[index]
    actual = {
        "Name": candidate_contest.name,
        "ElectionDistrictId": candidate_contest.election_district_id,
        "VoteVariation": candidate_contest.vote_variation.value,
        "VotesAllowed": candidate_contest.votes_allowed,
    }
    expected = item
    assert actual == expected


@pytest.mark.parametrize("index,id", ELECTION_CONTEST_CANDIDATE_ID_TESTS)
def test_contest_candidate_ids(index, id, election_contest_candidates):
    """ElectionReport.Election.Contest["@id"]"""
    candidate_contest = election_contest_candidates[index]
    actual = candidate_contest.model__id
    expected = id
    assert actual == expected


@pytest.mark.parametrize("index,item", ELECTION_CONTEST_CANDIDATE_SELECTION_TESTS)
def test_contest_candidate_selections(index, item, election_contest_candidate_selections):
    """ElectionReport.Election.Contest.ContestSelection["@id"]"""
    candidate_contest_selection = election_contest_candidate_selections[index]
    actual = {
        "@type": candidate_contest_selection.model__type,
        "SequenceOrder": candidate_contest_selection.sequence_order,
    }
    candidate_ids = getattr(candidate_contest_selection, "candidate_ids", None)
    if candidate_ids:
        actual["CandidateIds"] = candidate_ids
    endorsement_party_ids = getattr(candidate_contest_selection, "endorsement_party_ids", None)
    if endorsement_party_ids:
        actual["EndorsementPartyIds"] = endorsement_party_ids
    is_write_in = getattr(candidate_contest_selection, "is_write_in", None)
    if is_write_in:
        actual["IsWriteIn"] = is_write_in
    expected = item
    assert actual == expected


@pytest.mark.parametrize("index,id", ELECTION_CONTEST_CANDIDATE_SELECTION_ID_TESTS)
def test_contest_candidate_selection_ids(index, id, election_contest_candidate_selections):
    """ElectionReport.Election.Contest.ContestSelection["@id"]"""
    candidate_contest_selection = election_contest_candidate_selections[index]
    actual = candidate_contest_selection.model__id
    expected = id
    assert actual == expected


@pytest.mark.parametrize("index,item", ELECTION_CONTEST_BALLOT_MEASURE_TESTS)
def test_contest_ballot_measures(index, item, election_contest_ballot_measures):
    """ElectionReport.Election.Contest["@type"] == 'ElectionResults.BallotMeasureContest'"""
    ballot_measure_contest = election_contest_ballot_measures[index]
    actual = {
        "Name": ballot_measure_contest.name,
        "ElectionDistrictId": ballot_measure_contest.election_district_id,
        "VoteVariation": ballot_measure_contest.vote_variation.value,
    }
    expected = item
    assert actual == expected


@pytest.mark.parametrize("index,id", ELECTION_CONTEST_BALLOT_MEASURE_ID_TESTS)
def test_contest_ballot_measure_ids(index, id, election_contest_ballot_measures):
    """ElectionReport.Election.Contest.ContestSelection["@id"]"""
    ballot_measure_contest = election_contest_ballot_measures[index]
    actual = ballot_measure_contest.model__id
    expected = id
    assert actual == expected


@pytest.mark.parametrize("index,item", ELECTION_CONTEST_BALLOT_MEASURE_SELECTION_TESTS)
def test_contest_ballot_measure_selections(index, item, election_contest_ballot_measure_selections):
    """ElectionReport.Election.Contest.ContestSelection["@id"]"""
    ballot_measure_contest_selection = election_contest_ballot_measure_selections[index]
    actual = {
        "@type": ballot_measure_contest_selection.model__type,
        "SequenceOrder": ballot_measure_contest_selection.sequence_order,
        "Selection": [
            {
                "Content": _.content,
                "Language": _.language,
            } for _ in ballot_measure_contest_selection.selection.text
        ]
    }
    expected = item
    assert actual == expected


@pytest.mark.parametrize("index,id", ELECTION_CONTEST_BALLOT_MEASURE_SELECTION_ID_TESTS)
def test_contest_ballot_measure_selection_ids(index, id, election_contest_ballot_measure_selections):
    """ElectionReport.Election.Contest.ContestSelection["@id"]"""
    ballot_measure_contest_selection = election_contest_ballot_measure_selections[index]
    actual = ballot_measure_contest_selection.model__id
    expected = id
    assert actual == expected



@pytest.mark.parametrize("index,item", HEADER_TESTS)
def test_headers(index, item, headers):
    """'Header'"""
    header = headers[index]
    actual = {
        "@id": header.model__id,
        "Name": [
            {
                "Content": _.content,
                "Language": _.language,
            } for _ in header.name.text
        ]
    }
    expected = item
    assert actual == expected


@pytest.mark.parametrize("index,item", PARTY_TESTS)
def test_parties(index, item, parties):
    """'Party'"""
    party = parties[index]
    actual = {
        "@id": party.model__id,
        "Name": [
            {
                "Content": _.content,
                "Language": _.language,
            } for _ in party.name.text
        ]
    }
    expected = item
    assert actual == expected


@pytest.mark.parametrize("index,item", PERSON_TESTS)
def test_persons(index, item, persons):
    """'Person'"""
    person = persons[index]
    actual = {
        "@id": person.model__id,
        "FullName": [
            {
                "Content": _.content,
                "Language": _.language,
            } for _ in person.full_name.text
        ],
        "Profession": [
            {
                "Content": _.content,
                "Language": _.language,
            } for _ in person.profession.text
        ],
    }
    expected = item
    assert actual == expected


@pytest.mark.parametrize("index,item", REPORTING_UNIT_TESTS)
def test_reporting_units(index, item, reporting_units):
    """GpUnit['@type'] == 'ElectionResults.ReportingUnit'"""
    reporting_unit = reporting_units[index]
    actual = {
        "@id": reporting_unit.model__id,
        "Name": [
            {
                "Content": _.content,
                "Language": _.language,
            } for _ in reporting_unit.name.text
        ],
        "Type": reporting_unit.type.value,
    }
    expected = item
    assert actual == expected


@pytest.mark.parametrize("index,item", REPORTING_DEVICE_TESTS)
def test_reporting_devices(index, item, reporting_devices):
    """GpUnit['@type'] == 'ElectionResults.ReportingDevice'"""
    reporting_device = reporting_devices[index]
    actual = {
        "@id": reporting_device.model__id,
        "Manufacturer": reporting_device.device_class.manufacturer,
        "Model": reporting_device.device_class.model,
        "Type": reporting_device.device_class.type.value,
        "SerialNumber": reporting_device.serial_number,
    }
    expected = item
    assert actual == expected
