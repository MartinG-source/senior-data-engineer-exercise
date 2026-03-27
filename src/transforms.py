"""
Contact data transformation module.

Contains normalization functions for cleaning raw contact data
and an enrichment pipeline that joins contacts with preferences
and engagement events.
"""
import pandas as pd
from typing import Optional
import re


# ---------------------------------------------------------------------------
# Step 2 — Email normalization
# ---------------------------------------------------------------------------

def normalize_email(email: Optional[str]) -> Optional[str]:
    """
    Normalize an email address.

    Rules:
        - Remove leading/trailing whitespace
        - Convert to lowercase
        - Return None for empty or missing values

    Args:
        email: Raw email string.

    Returns:
        Normalized email or None.
    """
    # TODO: implement
    return None


# ---------------------------------------------------------------------------
# Step 3 — Phone normalization
# ---------------------------------------------------------------------------

def normalize_phone(phone: Optional[str]) -> Optional[str]:
    """
    Normalize a phone number.

    Rules:
        - Strip all non-digit characters
        - 10-digit numbers → (XXX) XXX-XXXX
        - 11-digit numbers starting with 1 → 1-(XXX) XXX-XXXX
        - Return None for anything else

    Args:
        phone: Raw phone string.

    Returns:
        Formatted phone number or None.
    """
    # TODO: implement
    return None


# ---------------------------------------------------------------------------
# Step 2 (provided example) — Address normalization
# ---------------------------------------------------------------------------

def normalize_address(address: Optional[str]) -> Optional[str]:
    """
    Normalize a street address.

    Rules:
        - Remove leading/trailing whitespace
        - Standardize abbreviations (St → Street, Ave → Avenue, etc.)
        - Title-case each word

    Args:
        address: Raw address string.

    Returns:
        Normalized address or None.
    """
    if pd.isna(address) or address is None:
        return None

    address_str = str(address).strip()
    if not address_str:
        return None

    # Standardize common abbreviations
    address_str = re.sub(r'\bSt\b', 'Street', address_str, flags=re.IGNORECASE)
    address_str = re.sub(r'\bAve\b', 'Avenue', address_str, flags=re.IGNORECASE)
    address_str = re.sub(r'\bRd\b', 'Road', address_str, flags=re.IGNORECASE)
    address_str = re.sub(r'\bDr\b', 'Drive', address_str, flags=re.IGNORECASE)
    address_str = re.sub(r'\bLn\b', 'Lane', address_str, flags=re.IGNORECASE)

    # Title-case each word
    return address_str.title()


# ---------------------------------------------------------------------------
# Step 4 — State normalization
# ---------------------------------------------------------------------------

def normalize_state(state: Optional[str]) -> Optional[str]:
    """
    Normalize a US state to its 2-letter code.

    Rules:
        - Remove leading/trailing whitespace
        - If already a 2-letter code, uppercase it
        - If a full state name, map to the 2-letter code
        - Return None if the value can't be mapped

    Args:
        state: Raw state string (e.g. "Texas", " il ", "NY").

    Returns:
        Uppercase 2-letter state code or None.
    """
    # TODO: implement
    return None


# ---------------------------------------------------------------------------
# Step 4 — ZIP normalization
# ---------------------------------------------------------------------------

def normalize_zip(zip_code: Optional[str]) -> Optional[str]:
    """
    Normalize a ZIP code to 5-digit format.

    Rules:
        - Remove leading/trailing whitespace
        - Handle ZIP+4 format (90001-3344 → 90001)
        - Handle float-like strings (77001.0 → 77001)
        - Return None if the result is not exactly 5 digits

    Args:
        zip_code: Raw ZIP string.

    Returns:
        5-digit ZIP string or None.
    """
    # TODO: implement
    return None


# ---------------------------------------------------------------------------
# Step 5 — Contact enrichment (join + derive)
# ---------------------------------------------------------------------------

def enrich_contacts(
    contacts_df: pd.DataFrame,
    preferences_df: pd.DataFrame,
    events_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Join contacts with preferences and engagement events, then derive
    enrichment fields.

    Derived fields:
        - contactable (bool): True if email or phone is valid after normalization
        - preferred_reachable_channel (str): preferred channel if valid,
          else fallback to any valid channel, else "none"
        - do_not_contact (bool): True if both opt-ins are "no" OR contact
          has an unsubscribe event
        - contact_quality_tier (str): "high" / "medium" / "low" / "unreachable"

    Args:
        contacts_df:    DataFrame from contacts.csv (already normalized).
        preferences_df: DataFrame from contact_preferences.csv.
        events_df:      DataFrame from engagement_events.csv.

    Returns:
        Enriched DataFrame with the derived columns added.
    """
    # TODO: implement
    # Hint: break this into smaller helper functions and test each one.
    return contacts_df


# ---------------------------------------------------------------------------
# Pipeline entry point
# ---------------------------------------------------------------------------

def transform_contacts(input_file: str, output_file: str, output_format: str = 'excel'):
    """
    End-to-end pipeline: read raw CSV, normalize, and write output.

    Args:
        input_file:    Path to contacts CSV.
        output_file:   Path to output file.
        output_format: 'excel' or 'csv'.
    """
    df = pd.read_csv(input_file)

    # Apply column-level normalizations
    df['email'] = df['email'].apply(normalize_email)
    df['phone_number'] = df['phone_number'].apply(normalize_phone)
    df['address'] = df['address'].apply(normalize_address)
    df['state'] = df['state'].apply(normalize_state)
    df['zip'] = df['zip'].apply(normalize_zip)

    # Write output
    if output_format.lower() == 'excel':
        df.to_excel(output_file, index=False, engine='openpyxl')
    else:
        df.to_csv(output_file, index=False)

    return df


if __name__ == '__main__':
    import sys

    input_path = 'data/input/contacts.csv'
    output_path = 'data/output/contacts_cleaned.xlsx'

    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_path = sys.argv[2]

    transform_contacts(input_path, output_path, output_format='excel')
    print(f"Transformation complete. Output written to {output_path}")
