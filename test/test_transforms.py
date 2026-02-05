"""
Test suite for data transformation functions.
"""
import pytest
import pandas as pd
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from transforms import normalize_address

@pytest.fixture
def input_csv_path():
    """Fixture providing path to input CSV file."""
    return Path(__file__).parent.parent / 'data' / 'input' / 'contacts.csv'


@pytest.fixture
def input_df(input_csv_path):
    """Fixture providing dataframe loaded from input CSV."""
    return pd.read_csv(input_csv_path)


def test_normalize_address_standardization(input_df):
    """Test address normalization standardizes abbreviations."""
    address = input_df.loc[0, 'address']
    normalized = normalize_address(address)
    assert normalized == '123 Main Street'


def test_normalize_address_ave_abbreviation(input_df):
    """Test address normalization handles 'Ave' abbreviation."""
    address = input_df.loc[1, 'address']
    normalized = normalize_address(address)
    assert normalized == '456 Oak Avenue '


