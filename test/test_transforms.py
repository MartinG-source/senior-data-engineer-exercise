"""
Test suite for contact data transformations.

The two tests below are provided as examples of the pattern we expect.
For each new function you implement, follow the TDD cycle:
    1. Write a failing test
    2. Implement just enough code to make it pass
    3. Refactor if needed
"""
import pytest
import pandas as pd
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from transforms import (
    normalize_address,
    normalize_email,
    normalize_phone,
    normalize_state,
    normalize_zip,
    enrich_contacts,
)


# ---------------------------------------------------------------------------
# Fixtures — reusable test data
# ---------------------------------------------------------------------------

@pytest.fixture
def input_csv_path():
    """Path to raw contacts CSV."""
    return Path(__file__).parent.parent / 'data' / 'input' / 'contacts.csv'


@pytest.fixture
def contacts_df(input_csv_path):
    """DataFrame loaded from contacts.csv."""
    return pd.read_csv(input_csv_path)


@pytest.fixture
def preferences_df():
    """DataFrame loaded from contact_preferences.csv."""
    path = Path(__file__).parent.parent / 'data' / 'input' / 'contact_preferences.csv'
    return pd.read_csv(path)


@pytest.fixture
def events_df():
    """DataFrame loaded from engagement_events.csv."""
    path = Path(__file__).parent.parent / 'data' / 'input' / 'engagement_events.csv'
    return pd.read_csv(path)


# ===========================================================================
# EXAMPLE TESTS (provided) — normalize_address
# ===========================================================================

class TestNormalizeAddress:
    """Tests for address normalization — these pass out of the box."""

    def test_standardizes_st_abbreviation(self):
        assert normalize_address('123 Main St') == '123 Main Street'

    def test_standardizes_ave_abbreviation(self):
        assert normalize_address('456 Oak Ave') == '456 Oak Avenue'

    def test_returns_none_for_none(self):
        assert normalize_address(None) is None

    def test_returns_none_for_empty_string(self):
        assert normalize_address('') is None

    def test_title_cases_output(self):
        assert normalize_address('789 pine rd') == '789 Pine Road'


# ===========================================================================
# Step 2 — normalize_email
# ===========================================================================
# TODO: Write tests here, then implement normalize_email in src/transforms.py
#
# Things to test:
#   - Strips leading/trailing whitespace
#   - Converts to lowercase
#   - Returns None for None input
#   - Returns None for empty string


# ===========================================================================
# Step 3 — normalize_phone
# ===========================================================================
# TODO: Write tests here, then implement normalize_phone in src/transforms.py
#
# Things to test:
#   - Formats 10-digit number as (XXX) XXX-XXXX
#   - Formats 11-digit number starting with 1 as 1-(XXX) XXX-XXXX
#   - Strips parentheses, dashes, dots, spaces
#   - Returns None for too-short numbers
#   - Returns None for too-long numbers
#   - Returns None for None input


# ===========================================================================
# Step 4 — normalize_state / normalize_zip
# ===========================================================================
# TODO: Write tests here, then implement in src/transforms.py
#
# State things to test:
#   - Full name → 2-letter code (e.g. "Texas" → "TX")
#   - Already a code → uppercase (e.g. " il " → "IL")
#   - Returns None for unmappable values
#
# ZIP things to test:
#   - ZIP+4 → 5-digit (e.g. "90001-3344" → "90001")
#   - Float-like → 5-digit (e.g. "77001.0" → "77001")
#   - Returns None for non-numeric or wrong length


# ===========================================================================
# Step 5 — enrich_contacts (join + derive)
# ===========================================================================
# TODO: Write tests here, then implement enrich_contacts in src/transforms.py
#
# Approach: build small DataFrames in your tests rather than relying on
# the full CSV files. This makes tests fast, focused, and independent
# of the sample data.
#
# Things to test:
#   - contactable is True when email is valid
#   - contactable is True when phone is valid
#   - contactable is False when neither is valid
#   - preferred_reachable_channel uses preferred channel when valid
#   - preferred_reachable_channel falls back when preferred channel is invalid
#   - do_not_contact is True when both opt-ins are "no"
#   - do_not_contact is True when contact has an unsubscribe event
#   - contact_quality_tier logic (discuss approach before implementing)
