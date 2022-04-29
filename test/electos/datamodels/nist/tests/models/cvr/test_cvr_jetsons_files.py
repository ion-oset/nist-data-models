import pytest

import json

from electos.datamodels.nist.models.cvr import *

from pydantic import ValidationError

from tests.utility import load_test_data, raises, raises_none


# --- Test data

CVR_SAMPLE_FILES = [
    ( "jetsons", "jetsons_main_cvr.json" ),
]


# --- Test fixtures

@pytest.fixture(params = CVR_SAMPLE_FILES)
def test_data(request):
    """Pre-load test data and return the ."""
    package, file = request.param
    text = load_test_data(package, file)
    data = json.loads(text)
    return data


@pytest.fixture()
def cvr_report(test_data):
    return CastVoteRecordReport(**test_data)


@pytest.fixture()
def cvr_contests(cvr_report):
    return [
        contest
        for cvr in cvr_report.cvr
        for snapshot in cvr.cvr_snapshot
        for contest in snapshot.cvr_contest
    ]


@pytest.fixture()
def cvr_contest_selections(cvr_contests):
    return [
        contest_selection
        for contest in cvr_contests
        for contest_selection in contest.cvr_contest_selection
    ]


@pytest.fixture()
def cvr_selection_positions(cvr_contest_selections):
    return [
        selection_position
        for contest_selection in cvr_contest_selections
        for selection_position in contest_selection.selection_position
    ]


@pytest.fixture()
def elections(cvr_report):
    return cvr_report.election


@pytest.fixture()
def election_candidates(elections):
    return [
        candidate
        for election in elections
        for candidate in election.candidate
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
        for election_contest in election_contests
        for contest_selection in election_contest.contest_selection
    ]


@pytest.fixture()
def election_candidate_contest_selections(election_contests):
    return [
        contest_selection
        for election_contest in election_contests
        for contest_selection in election_contest.contest_selection
            if contest_selection.model__type == "CVR.CandidateSelection"
    ]


@pytest.fixture()
def election_ballot_measure_contest_selections(election_contests):
    return [
        contest_selection
        for election_contest in election_contests
        for contest_selection in election_contest.contest_selection
            if contest_selection.model__type == "CVR.BallotMeasureSelection"
    ]


@pytest.fixture()
def parties(cvr_report):
    return [
        party
        for party in cvr_report.party
    ]


@pytest.fixture()
def gp_units(cvr_report):
    return [
        gp_unit
        for gp_unit in cvr_report.gp_unit
    ]


# --- Test cases

CVR_BALLOT_STYLE_ID_TESTS = enumerate([
    "ballot-style/bedrock-precinct",
    "ballot-style/port-precinct",
    "ballot-style/downtown-precinct",
    "ballot-style/spacetown-precinct",
])


CVR_CURRENT_SNAPSHOT_ID_TESTS = enumerate([
    "snapshot-01",
    "snapshot-01",
    "snapshot-01",
    "snapshot-01",
])


CVR_ELECTION_ID_TESTS = enumerate([
    "gadget-county-2021-06",
    "gadget-county-2021-06",
    "gadget-county-2021-06",
    "gadget-county-2021-06",
])


CVR_CONTEST_ID_TESTS = enumerate([
    "contest-ballot-measure-gadget-county-1",
    "contest-control-board-spaceport",
    "contest-ballot-measure-gadget-county-1",
    "contest-mayor-orbit-city",
    "contest-ballot-measure-gadget-county-1",
    "contest-mayor-orbit-city",
    "contest-control-board-spaceport",
    "contest-ballot-measure-gadget-county-1",
])


CVR_CONTEST_SELECTION_ID_TESTS = enumerate([
    "contest-ballot-measure-1--selection-yes",
    "contest-control-board-spaceport--selection-rudi-indexer",
    "contest-control-board-spaceport--selection-write-in-1",
    "contest-ballot-measure-1--selection-yes",
    "contest-mayor--selection-spencer-cogswell",
    "contest-ballot-measure-1--selection-no",
    "contest-mayor--selection-cosmo-spacely",
    "contest-control-board-spaceport--selection-jane-jetson",
    "contest-control-board-spaceport--selection-harlan-ellis",
    "contest-ballot-measure-1--selection-yes",
])


CVR_CONTEST_SELECTION_TESTS = enumerate([
    { "OptionPosition": 1, "TotalNumberVotes": 1 },
    { "OptionPosition": 3, "TotalNumberVotes": 1 },
    { "OptionPosition": 4, "TotalNumberVotes": 1 },
    {                      "TotalNumberVotes": 1 },
    { "OptionPosition": 2, "TotalNumberVotes": 1 },
    {                      "TotalNumberVotes": 1 },
    { "OptionPosition": 1, "TotalNumberVotes": 1 },
    { "OptionPosition": 1, "TotalNumberVotes": 1 },
    { "OptionPosition": 2, "TotalNumberVotes": 1 },
    { "OptionPosition": 1, "TotalNumberVotes": 1 },
])


CVR_SELECTION_POSITION_TESTS = enumerate([
    { "HasIndication": "yes", "NumberVotes": 1 },
    { "HasIndication": "yes", "NumberVotes": 1 },
    { "HasIndication": "yes", "NumberVotes": 1 },
    { "HasIndication": "yes", "NumberVotes": 1 },
    { "HasIndication": "yes", "NumberVotes": 1 },
    { "HasIndication": "yes", "NumberVotes": 1 },
    { "HasIndication": "yes", "NumberVotes": 1 },
    { "HasIndication": "yes", "NumberVotes": 1 },
    { "HasIndication": "yes", "NumberVotes": 1 },
    { "HasIndication": "yes", "NumberVotes": 1 },
])


ELECTION_ID_TESTS = enumerate([
    "gadget-county-2021-06",
])


ELECTION_SCOPE_ID_TESTS = enumerate([
    "gadget-county",
])


ELECTION_CANDIDATE_ID_TESTS = enumerate([
    "candidate-cosmo-spacely",
    "candidate-spencer-cogswell",
    "candidate-jane-jetson",
    "candidate-harlan-ellis",
    "candidate-rudi-indexer",
])


ELECTION_CANDIDATE_TESTS = enumerate([
    { "Name": "Cosmo Spacely", "PartyId": "party-lepton" },
    { "Name": "Spencer Cogswell", "PartyId": "party-hadron" },
    { "Name": "Jane Jetson" },
    { "Name": "Harlan Ellis" },
    { "Name": "Rudi Indexer" },
])


ELECTION_CONTEST_ID_TESTS = enumerate([
    "contest-mayor-orbit-city",
    "contest-control-board-spaceport",
    "contest-ballot-measure-gadget-county-1",
])


ELECTION_CONTEST_TESTS = enumerate([
    {
        "Name": "Mayor of Orbit City",
        "VoteVariation": "plurality"
    },
    {
        "Name": "SpacePort Control Board",
        "VoteVariation": "n-of-m",
        "VotesAllowed": 2,
        "NumberElected": 2
    },
    {
        "Name": "Shall Gadget County increase its sales tax from 1% to 1.1% for "
                "the purpose of raising additional revenue to fund expanded air "
                "traffic control operations?",
        "VoteVariation": "plurality"
    },
])


ELECTION_CONTEST_SELECTION_ID_TESTS = enumerate([
    "contest-mayor--selection-cosmo-spacely",
    "contest-mayor--selection-spencer-cogswell",
    "contest-mayor--selection-write-in",
    "contest-control-board-spaceport--selection-jane-jetson",
    "contest-control-board-spaceport--selection-harlan-ellis",
    "contest-control-board-spaceport--selection-rudi-indexer",
    "contest-control-board-spaceport--selection-write-in-1",
    "contest-control-board-spaceport--selection-write-in-2",
    "contest-ballot-measure-1--selection-yes",
    "contest-ballot-measure-1--selection-no",
])


# Note: ContestSelections are split up by their '@type'.
# JSON Schema has ambiguity distinguishing between distinct subtypes.

ELECTION_CANDIDATE_CONTEST_SELECTION_TESTS = enumerate([
    {
      "@type": "CVR.CandidateSelection",
      "CandidateIds": [ "candidate-cosmo-spacely" ],
    },
    {
      "@type": "CVR.CandidateSelection",
      "CandidateIds": [ "candidate-spencer-cogswell" ],
    },
    {
      "@type": "CVR.CandidateSelection",
      "IsWriteIn": True,
    },
    {
      "@type": "CVR.CandidateSelection",
      "CandidateIds": [ "candidate-jane-jetson" ],
    },
    {
      "@type": "CVR.CandidateSelection",
      "CandidateIds": [ "candidate-harlan-ellis" ],
    },
    {
      "@type": "CVR.CandidateSelection",
      "CandidateIds": [ "candidate-rudi-indexer" ],
    },
    {
      "@type": "CVR.CandidateSelection",
      "IsWriteIn": True,
    },
    {
      "@type": "CVR.CandidateSelection",
      "IsWriteIn": True,
    },
])


ELECTION_BALLOT_MEASURE_CONTEST_SELECTION_TESTS = enumerate([
    {
      "@type": "CVR.BallotMeasureSelection",
      "Selection": "Yes",
    },
    {
      "@type": "CVR.BallotMeasureSelection",
      "Selection": "No",
    },
])


GP_UNIT_TESTS = enumerate([
    { "@id": "gadget-county", "Name": "Gadget County", "Type": "other",
      "OtherType": "county" },
    { "@id": "bedrock-precinct", "Name": "Bedrock Precinct", "Type": "precinct" },
    { "@id": "downtown-precinct", "Name": "Downtown Precinct", "Type": "precinct" },
    { "@id": "port-precinct", "Name": "Port Precinct", "Type": "precinct" },
    { "@id": "spacetown-precinct", "Name": "SpaceTown Precinct", "Type": "precinct" },
])


PARTY_TESTS = enumerate([
    { "@id": "party-hadron", "Name": "Hadron Party" },
    { "@id": "party-lepton", "Name": "Lepton Party" },
])


# --- Tests

@pytest.mark.parametrize("index,id", CVR_BALLOT_STYLE_ID_TESTS)
def test_cvr_ballot_style_ids(index, id, cvr_report):
    """'CVR.BallotStyleId'"""
    cvr = cvr_report.cvr[index]
    actual = cvr.ballot_style_id
    expected = id
    assert actual == expected


@pytest.mark.parametrize("index,id", CVR_CURRENT_SNAPSHOT_ID_TESTS)
def test_cvr_current_snapshot_ids(index, id, cvr_report):
    """'CVR.CurrentSnapshotId'"""
    cvr = cvr_report.cvr[index]
    actual = cvr.current_snapshot_id
    expected = id
    assert actual == expected


@pytest.mark.parametrize("index,id", CVR_ELECTION_ID_TESTS)
def test_cvr_election_ids(index, id, cvr_report):
    """'CVR.ElectionId'"""
    cvr = cvr_report.cvr[index]
    actual = cvr.election_id
    expected = id
    assert actual == expected


@pytest.mark.parametrize("index,id", CVR_CONTEST_ID_TESTS)
def test_cvr_contest_ids(index, id, cvr_contests):
    """'CVR.CVRSnapshot.CVRContest.ContestId'"""
    cvr_contest = cvr_contests[index]
    actual = cvr_contest.contest_id
    expected = id
    assert actual == expected


@pytest.mark.parametrize("index,id", CVR_CONTEST_SELECTION_ID_TESTS)
def test_cvr_contest_selection_ids(index, id, cvr_contest_selections):
    """'CVR.CVRSnapshot.CVRContest.CVRContestSelection.ContestSelectionId'"""
    cvr_contest_selection = cvr_contest_selections[index]
    actual = cvr_contest_selection.contest_selection_id
    expected = id
    assert actual == expected


@pytest.mark.parametrize("index,item", CVR_CONTEST_SELECTION_TESTS)
def test_cvr_contest_selections(index, item, cvr_contest_selections):
    """'CVR.CVRSnapshot.CVRContest.CVRContestSelection[]'
    All fields other than 'ContestSelectionId' and 'SelectionPosition'.
    """
    cvr_contest_selection = cvr_contest_selections[index]
    actual = {}
    option_position = getattr(cvr_contest_selection, "option_position", None)
    if option_position:
        actual["OptionPosition"] = option_position
    actual["TotalNumberVotes"] = cvr_contest_selection.total_number_votes
    expected = item
    assert actual == expected


@pytest.mark.parametrize("index,item", CVR_SELECTION_POSITION_TESTS)
def test_cvr_selection_positions(index, item, cvr_selection_positions):
    """'CVR.CVRSnapshot.CVRContest.CVRContestSelection.SelectionPosition[]'"""
    cvr_selection_position = cvr_selection_positions[index]
    actual = {
        "HasIndication": cvr_selection_position.has_indication.value,
        "NumberVotes": cvr_selection_position.number_votes
    }
    expected = item
    assert actual == expected


@pytest.mark.parametrize("index,id", ELECTION_ID_TESTS)
def test_election_ids(index, id, elections):
    """'Election["@id"]'"""
    election = elections[index]
    actual = election.model__id
    expected = id
    assert actual == expected


@pytest.mark.parametrize("index,id", ELECTION_SCOPE_ID_TESTS)
def test_election_scope_ids(index, id, elections):
    """'Election.ElectionScopeId'"""
    election = elections[index]
    actual = election.election_scope_id
    expected = id
    assert actual == expected


@pytest.mark.parametrize("index,id", ELECTION_CANDIDATE_ID_TESTS)
def test_election_candidate_ids(index, id, election_candidates):
    """'Election.Candidate[@id]'"""
    candidate = election_candidates[index]
    actual = candidate.model__id
    expected = id
    assert actual == expected


@pytest.mark.parametrize("index,item", ELECTION_CANDIDATE_TESTS)
def test_election_candidates(index, item, election_candidates):
    """'Election.Candidate'"""
    candidate = election_candidates[index]
    actual = {
        "Name": candidate.name,
    }
    party_id = getattr(candidate, "party_id", None)
    if party_id:
        actual["PartyId"] = party_id
    expected = item
    assert actual == expected


@pytest.mark.parametrize("index,id", ELECTION_CONTEST_ID_TESTS)
def test_election_contest_ids(index, id, election_contests):
    """'Election.Contest[@id]'"""
    contest = election_contests[index]
    actual = contest.model__id
    expected = id
    assert actual == expected


@pytest.mark.parametrize("index,item", ELECTION_CONTEST_TESTS)
def test_election_contests(index, item, election_contests):
    """'Election.Contest'
    All fields other than 'ContestSelection'.
    """
    contest = election_contests[index]
    actual = {
        "Name": contest.name,
        "VoteVariation": contest.vote_variation.value
    }
    votes_allowed = getattr(contest, "votes_allowed", None)
    if votes_allowed:
        actual["VotesAllowed"] = votes_allowed
    number_elected = getattr(contest, "number_elected", None)
    if number_elected:
        actual["NumberElected"] = number_elected
    expected = item
    assert actual == expected


@pytest.mark.parametrize("index,id", ELECTION_CONTEST_SELECTION_ID_TESTS)
def test_election_contest_selection_ids(index, id, election_contest_selections):
    """'Election.Contest.ContestSelection[@id]'."""
    contest_selection = election_contest_selections[index]
    actual = contest_selection.model__id
    expected = id
    assert actual == expected


# As noted above ContestSelections require checking the '@type'.

@pytest.mark.parametrize("index,item", ELECTION_CANDIDATE_CONTEST_SELECTION_TESTS)
def test_election_candidate_contest_selections(index, item, election_candidate_contest_selections):
    """'Election.Contest.ContestSelection["@type"] == 'CVR.CandidateSelection'."""
    contest_selection = election_candidate_contest_selections[index]
    assert contest_selection.model__type == "CVR.CandidateSelection"
    actual = {
        "@type": contest_selection.model__type,
    }
    candidate_ids = getattr(contest_selection, "candidate_ids", None)
    if candidate_ids:
        actual["CandidateIds"] = candidate_ids
    is_write_in = getattr(contest_selection, "is_write_in", None)
    if is_write_in:
        actual["IsWriteIn"] = is_write_in
    expected = item
    assert actual == expected


@pytest.mark.parametrize("index,item", ELECTION_BALLOT_MEASURE_CONTEST_SELECTION_TESTS)
def test_election_ballot_measure_contest_selections(index, item, election_ballot_measure_contest_selections):
    """'Election.Contest.ContestSelection["@type"] == 'CVR.BallotMeasureSelection'."""
    contest_selection = election_ballot_measure_contest_selections[index]
    assert contest_selection.model__type == "CVR.BallotMeasureSelection"
    actual = {
        "@type": contest_selection.model__type,
        "Selection": contest_selection.selection,
    }
    expected = item
    assert actual == expected


@pytest.mark.parametrize("index,item", GP_UNIT_TESTS)
def test_gp_units(index, item, gp_units):
    """'GpUnit'"""
    gp_unit = gp_units[index]
    actual = {
        "@id": gp_unit.model__id,
        "Name": gp_unit.name,
        "Type": gp_unit.type.value,
    }
    other_type = getattr(gp_unit, "other_type", None)
    if other_type:
        actual["OtherType"] = other_type
    expected = item
    assert actual == expected


@pytest.mark.parametrize("index,item", PARTY_TESTS)
def test_parties(index, item, parties):
    """'Party'"""
    party = parties[index]
    actual = {
        "@id": party.model__id,
        "Name": party.name,
    }
    expected = item
    assert actual == expected
