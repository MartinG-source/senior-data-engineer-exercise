"""
Test suite for data transformation functions.
"""
import pytest
import pandas as pd
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from transforms import normalize_email, normalize_phone, normalize_address, transform_contacts


def _eq(a, b):
    """Compare two values with None/NaN treated as equal; coerce numeric to string for phone comparison."""
    if pd.isna(a) and pd.isna(b):
        return True
    if pd.isna(a) or pd.isna(b):
        return False
    # Coerce so e.g. 5551234567.0 (from CSV) matches '5551234567'
    def _norm(x):
        if isinstance(x, (int, float)):
            return str(int(x))
        return str(x).strip() if x is not None else x
    return _norm(a) == _norm(b)


@pytest.fixture
def input_csv_path():
    """Path to input CSV with edge-case rows and expected output columns."""
    return Path(__file__).parent.parent / 'data' / 'input' / 'contacts.csv'


@pytest.fixture
def sample_contacts_df(input_csv_path):
    """Single fixture: load input contact data and expected outputs from CSV."""
    return pd.read_csv(input_csv_path)


def test_normalize_email_with_whitespace(sample_contacts_df):
    """Test email normalization removes whitespace and converts to lowercase."""
    row = sample_contacts_df.loc[0]
    assert normalize_email(row['email']) == row['expected_email']


def test_normalize_email_lowercase(sample_contacts_df):
    """Test email normalization converts to lowercase."""
    row = sample_contacts_df.loc[1]
    assert normalize_email(row['email']) == row['expected_email']


def test_normalize_email_none(sample_contacts_df):
    """Test email normalization handles None/empty values."""
    row = sample_contacts_df.loc[2]
    assert _eq(normalize_email(row['email']), row['expected_email'])


def test_normalize_email_invalid_no_at(sample_contacts_df):
    """Test email normalization returns None when email has no @."""
    row = sample_contacts_df.loc[3]
    assert _eq(normalize_email(row['email']), row['expected_email'])


def test_normalize_email_invalid_no_dot(sample_contacts_df):
    """Test email normalization returns None when email has no dot."""
    row = sample_contacts_df.loc[4]
    assert _eq(normalize_email(row['email']), row['expected_email'])


def test_normalize_phone_standard_format(sample_contacts_df):
    """Test phone normalization to single 10-digit string (removes parentheses, spaces, dashes)."""
    row = sample_contacts_df.loc[0]
    assert _eq(normalize_phone(row['phone_number']), row['expected_phone_number'])


def test_normalize_phone_with_dashes(sample_contacts_df):
    """Test phone normalization with dash separators -> single 10-digit string."""
    row = sample_contacts_df.loc[1]
    assert _eq(normalize_phone(row['phone_number']), row['expected_phone_number'])


def test_normalize_phone_with_country_code(sample_contacts_df):
    """Test phone normalization with country code -> single 10-digit string (drops leading 1)."""
    row = sample_contacts_df.loc[2]
    assert _eq(normalize_phone(row['phone_number']), row['expected_phone_number'])


def test_normalize_phone_strips_whitespace_and_nondigits(sample_contacts_df):
    """Test phone normalization removes whitespace and non-digit characters."""
    for i in [3, 4, 5]:
        row = sample_contacts_df.loc[i]
        assert _eq(normalize_phone(row['phone_number']), row['expected_phone_number'])


def test_normalize_phone_invalid_length_returns_none(sample_contacts_df):
    """Test phone normalization returns None for invalid digit count."""
    for i in [6, 7]:
        row = sample_contacts_df.loc[i]
        assert normalize_phone(row['phone_number']) is None


def test_normalize_address_standardization(sample_contacts_df):
    """Test address normalization standardizes abbreviations."""
    row = sample_contacts_df.loc[0]
    assert normalize_address(row['address']) == row['expected_address']


def test_normalize_address_ave_abbreviation(sample_contacts_df):
    """Test address normalization handles 'Ave' abbreviation."""
    row = sample_contacts_df.loc[1]
    assert normalize_address(row['address']) == row['expected_address']


def test_transform_contacts_integration(input_csv_path, tmp_path):
    """Test full transformation pipeline: run on input CSV and assert output matches expected columns from CSV."""
    output_file = tmp_path / 'output.csv'
    df = transform_contacts(str(input_csv_path), str(output_file))
    assert output_file.exists()
    for i in range(len(df)):
        assert _eq(df.loc[i, 'email'], df.loc[i, 'expected_email'])
        assert _eq(df.loc[i, 'phone_number'], df.loc[i, 'expected_phone_number'])
        assert _eq(df.loc[i, 'address'], df.loc[i, 'expected_address'])
    

