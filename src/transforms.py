"""
Data transformation module for cleaning and normalizing contact data.
"""
import pandas as pd
from typing import Optional
import re


def normalize_email(email: Optional[str]) -> Optional[str]:
    """
    Normalize email addresses by:
    1 Removing leading/trailing whitespace
    2. Converting to lowercase
    3. Valid email must contain @ and a .
    4. Returning None for empty strings or invalid format
    
    Args:
        email: Email string to normalize
        
    Returns:
        Normalized email or None if empty or invalid
    """
    if pd.isna(email) or email is None:
        return None
    
    email_str = str(email).strip()
    if not email_str:
        return None
    
    if '@' not in email_str or '.' not in email_str:
        return None
    
    return email_str.lower()


def normalize_phone(phone: Optional[str]) -> Optional[str]:
    """
    Normalize phone numbers to a single 10-digit string by:
    1. Removing whitespace and all non-digit characters
    2. Accepting 10 digits or 11 digits with leading US country code (1)
    3. Returning None for invalid lengths
    
    Args:
        phone: Phone string to normalize (any format; digits are extracted)
        
    Returns:
        Normalized phone as 10-digit string (e.g. '5551234567') or None if invalid
    """
    if pd.isna(phone) or phone is None:
        return None
    
    phone_str = str(phone).strip()
    if not phone_str:
        return None
    
    # Remove all non-digit characters (whitespace, punctuation, etc.)
    digits = re.sub(r'\D', '', phone_str)
    
    # Standard 10-digit US number
    if len(digits) == 10:
        return digits
    # 11 digits with leading US country code: use last 10 digits
    if len(digits) == 11 and digits.startswith('1'):
        return digits[1:]
    # Invalid length
    return None


def normalize_address(address: Optional[str]) -> Optional[str]:
    """
    Normalize address by:
    1. Removing leading/trailing whitespace
    2. Standardizing common abbreviations
    3. Capitalizing first letter of each word
    
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


def transform_contacts(input_file: str, output_file: str):
    """
    Transform contact data by normalizing emails, phones, and addresses.
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output file
    """
    # Read input CSV
    df = pd.read_csv(input_file)
    
    # Apply transformations
    df['email'] = df['email'].apply(normalize_email)
    df['phone_number'] = df['phone_number'].apply(normalize_phone)
    df['address'] = df['address'].apply(normalize_address)

    # Write output to CSV file
    df.to_csv(output_file, index=False)
    
    return df


if __name__ == '__main__':
    import sys
    
    input_path = 'data/input/contacts.csv'
    output_path = 'data/output/contacts_cleaned.csv'
    
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    
    transform_contacts(input_path, output_path)
    print(f"Transformation complete. Output written to {output_path}")