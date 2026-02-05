# Senior Data Engineer Exercise

This repository contains a data transformation exercise for cleaning and normalizing contact data.

## Repository Structure

```
senior-data-engineer-exercise/
├── data/
│   ├── input/
│   │   └── contacts.csv          # Input data with dirty records
│   └── output/                    # Output directory (created after transformation)
├── src/
│   └── transforms.py              # Data transformation functions
├── test/
│   └── test_transforms.py         # Test suite using pytest
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
├── .gitattributes                 # Cross-platform consistency
└── README.md                      # This file
```

## Prerequisites

- Python 3.10 or 3.11
- pip (Python package installer)

## Setup Instructions

### Windows PowerShell

```powershell
# Navigate to the repository directory
cd senior-data-engineer-exercise

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Mac OS / Linux

```bash
# Navigate to the repository directory
cd senior-data-engineer-exercise

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Git Bash (Windows)

```bash
# Navigate to the repository directory
cd senior-data-engineer-exercise

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt
```

## Interview / Task Instructions

Follow a **test-driven development (TDD)** workflow for each transformation:

1. **Write a failing test** for one transformation in `test/test_transforms.py`.
2. **Run the test** and confirm it fails: `pytest test/ -v`
3. **Implement the transformation** in `src/transforms.py` so the test passes.
4. **Repeat** for the next transformation until all are done.

### Transformations to Implement (TODOs)

Complete the following in order:

1. **Validate all tests pass** — Run `pytest test/ -v` and fix any failing tests so the suite is green before you start.
2. **Address** (`normalize_address`) — Write a failing test in `test/test_transforms.py`, then implement in `src/transforms.py`: remove leading/trailing whitespace; standardize abbreviations (St→Street, Ave→Avenue, etc.); capitalize first letter of each word.
3. **Email** (`normalize_email`) — Write a failing test, then implement: remove leading/trailing whitespace; convert to lowercase; return `None` for empty strings.
4. **Phone** (`normalize_phone`) — Write a failing test, then implement: strip non-digits (keep leading `1` for country code); format as `(XXX) XXX-XXXX` or `1-XXX-XXX-XXXX`; return `None` for invalid lengths.

## Running the Transformation

After setup, you can run the transformation script:

```bash
# Using default paths
python src/transforms.py

# Or specify custom input and output paths
python src/transforms.py data/input/contacts.csv data/output/contacts_cleaned.xlsx
```

The script will:
1. Read the input CSV file
2. Normalize email addresses (lowercase, trim whitespace)
3. Normalize phone numbers (standard format: (XXX) XXX-XXXX)
4. Normalize addresses (standardize abbreviations, capitalize)
5. Write the output to an Excel file (or CSV if specified)

## Running Tests

Run the test suite using pytest:

```bash
# Run all tests
pytest test/

# Run with verbose output
pytest test/ -v

# Run with coverage (if pytest-cov is installed)
pytest test/ --cov=src
```

**Note:** One test is intentionally incorrect and will fail initially. This is by design for the exercise.

## Data Transformation Details

### Email Normalization
- Removes leading/trailing whitespace
- Converts to lowercase
- Handles missing/empty values

### Phone Number Normalization
- Removes punctuation
- Formats as (XXX) XXX-XXXX for 10-digit numbers
- Formats as 1-XXX-XXX-XXXX for 11-digit numbers with country code
- Returns None for invalid lengths

### Address Normalization
- Removes leading/trailing whitespace
- Standardizes abbreviations (St → Street, Ave → Avenue, etc.)
- Capitalizes first letter of each word

## Dataset Description

The input CSV contains contact data with the following columns:
- `contact_id`: Unique identifier
- `first_name`: First name
- `last_name`: Last name
- `email`: Email address (may contain whitespace, mixed case)
- `phone_number`: Phone number (various formats)
- `address`: Street address
- `city`: City name
- `state`: State abbreviation
- `zip`: ZIP code

The dataset includes intentionally dirty data:
- Emails with extra spaces and mixed case
- Phone numbers with various punctuation formats
- One phone number with country code (1-XXX-XXX-XXXX)
- One missing email
- One invalid phone number length

## Dependencies

- **pytest**: Testing framework
- **pandas**: Data manipulation and analysis
- **openpyxl**: Excel file support
- **pydantic**: Data validation (available for use)

## License

This is an exercise repository for educational purposes.
