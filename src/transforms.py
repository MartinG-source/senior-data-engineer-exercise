"""
Data transformation module for cleaning and normalizing contact data.
"""
import pandas as pd
from typing import Optional
import re


def normalize_email(email: Optional[str]) -> Optional[str]:
    """
    Normalize email addresses by:
    - Removing leading/trailing whitespace
    - Converting to lowercase
    - Returning None for empty strings
    
    Args:
        email: Email string to normalize
        
    Returns:
        Normalized email or None if empty
    """
    if pd.isna(email) or email is None:
        return None
    
    email_str = str(email).strip()
    if not email_str:
        return None
    
    return email_str.lower()


def normalize_phone(phone: Optional[str]) -> Optional[str]:
    """
    Normalize phone numbers by:
    - Removing all non-digit characters except leading '1' country code
    - Formatting as (XXX) XXX-XXXX or 1-XXX-XXX-XXXX if country code present
    - Returning None for invalid lengths
    
    Args:
        phone: Phone string to normalize
        
    Returns:
        Normalized phone in format (XXX) XXX-XXXX or None if invalid
    """
    if pd.isna(phone) or phone is None:
        return None
    
    phone_str = str(phone).strip()
    if not phone_str:
        return None
    
    # Extract digits
    digits = re.sub(r'\D', '', phone_str)
    
    # Check for country code
    if digits.startswith('1') and len(digits) == 11:
        # US number with country code: format as 1-XXX-XXX-XXXX
        return f"1-{digits[1:4]}-{digits[4:7]}-{digits[7:]}"
    elif len(digits) == 10:
        # Standard US number: format as (XXX) XXX-XXXX
        return f"({digits[0:3]}) {digits[3:6]}-{digits[6:]}"
    else:
        # Invalid length
        return None


def normalize_address(address: Optional[str]) -> Optional[str]:
    """
    Normalize address by:
    - Removing leading/trailing whitespace
    - Standardizing common abbreviations
    - Capitalizing first letter of each word
    
    Args:
        address: Address string to normalize
        
    Returns:
        Normalized address or None if empty
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
    address_str = re.sub(r'\bWay\b', 'Way', address_str, flags=re.IGNORECASE)
    
    # Capitalize first letter of each word
    return ' '.join(word.capitalize() for word in address_str.split())


def transform_contacts(input_file: str, output_file: str, output_format: str = 'excel'):
    """
    Transform contact data by normalizing emails, phones, and addresses.
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output file
        output_format: 'excel' or 'csv' (default: 'excel')
    """
    # Read input CSV
    df = pd.read_csv(input_file)
    
    # Apply transformations
    df['email'] = df['email'].apply(normalize_email)
    df['phone_number'] = df['phone_number'].apply(normalize_phone)
    df['address'] = df['address'].apply(normalize_address)
    
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
