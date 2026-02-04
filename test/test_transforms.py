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


@pytest.fixture
def sample_contacts_df():
    """Fixture providing sample contact data."""
    return pd.DataFrame({
        'contact_id': [1, 2, 3],
        'first_name': ['John', 'Jane', 'Bob'],
        'last_name': ['Smith', 'Doe', 'Johnson'],
        'email': ['  JOHN@EXAMPLE.COM  ', 'jane.doe@example.com', None],
        'phone_number': ['(555) 123-4567', '555-123-4568', '1-555-123-4569'],
        'address': ['123 Main St', '456 Oak Ave', '789 Pine Rd'],
        'city': ['Austin', 'New York', 'Los Angeles'],
        'state': ['TX', 'NY', 'CA'],
        'zip': ['78701', '10001', '90001']
    })


@pytest.fixture
def input_csv_path():
    """Fixture providing path to input CSV file."""
    return Path(__file__).parent.parent / 'data' / 'input' / 'contacts.csv'


def test_normalize_email_with_whitespace(sample_contacts_df):
    """Test email normalization removes whitespace and converts to lowercase."""
    email = sample_contacts_df.loc[0, 'email']
    normalized = normalize_email(email)
    assert normalized == 'john@example.com'


def test_normalize_email_lowercase(sample_contacts_df):
    """Test email normalization converts to lowercase."""
    email = sample_contacts_df.loc[1, 'email']
    normalized = normalize_email(email)
    assert normalized == 'jane.doe@example.com'


def test_normalize_email_none():
    """Test email normalization handles None values."""
    normalized = normalize_email(None)
    assert normalized is None


def test_normalize_phone_standard_format(sample_contacts_df):
    """Test phone normalization for standard US format."""
    phone = sample_contacts_df.loc[0, 'phone_number']
    normalized = normalize_phone(phone)
    assert normalized == '(555) 123-4567'


def test_normalize_phone_with_dashes(sample_contacts_df):
    """Test phone normalization with dash separators."""
    phone = sample_contacts_df.loc[1, 'phone_number']
    normalized = normalize_phone(phone)
    assert normalized == '(555) 123-4568'


def test_normalize_phone_with_country_code(sample_contacts_df):
    """Test phone normalization with country code."""
    phone = sample_contacts_df.loc[2, 'phone_number']
    normalized = normalize_phone(phone)
    assert normalized == '1-555-123-4569'


def test_normalize_address_standardization(sample_contacts_df):
    """Test address normalization standardizes abbreviations."""
    address = sample_contacts_df.loc[0, 'address']
    normalized = normalize_address(address)
    assert normalized == '123 Main Street'


def test_normalize_address_ave_abbreviation(sample_contacts_df):
    """Test address normalization handles 'Ave' abbreviation."""
    address = sample_contacts_df.loc[1, 'address']
    normalized = normalize_address(address)
    assert normalized == '456 Oak Avenue'


def test_transform_contacts_integration(input_csv_path, tmp_path):
    """Test full transformation pipeline with real CSV file."""
    output_file = tmp_path / 'output.xlsx'
    df = transform_contacts(str(input_csv_path), str(output_file), output_format='excel')
    
    # Verify output file exists
    assert output_file.exists()
    
    # Verify transformations were applied
    assert df['email'].iloc[0] == 'john.smith@example.com'
    assert df['phone_number'].iloc[0] == '(555) 123-4567'
    
    # This test is intentionally incorrect - wrong assertion
    # The actual normalized email should be lowercase, but we're asserting it's uppercase
    assert df['email'].iloc[0] == 'JOHN.SMITH@EXAMPLE.COM'  # This will fail!
