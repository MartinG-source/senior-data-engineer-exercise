# Senior Data Engineer Exercise

> **Branch notice:** This branch contains the **solution for version 1** of the exercise.  
> **Interviewers and candidates** should use the **`main`** branch for the exercise (blank template, no solution).

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

## Running the Transformation

After setup, you can run the transformation script:

```bash
# Using default paths
python src/transforms.py

# Or specify custom input and output paths
python src/transforms.py data/input/contacts.csv data/output/contacts_cleaned.csv
```

The script will:
1. Read the input CSV file
2. Normalize email addresses (lowercase, trim whitespace)
3. Normalize phone numbers to a single 10-digit string (strip whitespace and non-digits)
4. Normalize addresses (standardize abbreviations, capitalize)
5. Write the output to a CSV file

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

## Data Transformation Details

### Email Normalization
- Removes leading/trailing whitespace
- Converts to lowercase
- Handles missing/empty values

### Phone Number Normalization
- **Input**: Any string (e.g. with spaces, parentheses, dashes, dots); treated as a standard 10-digit number once cleaned.
- **Processing**: Removes all whitespace and non-digit characters; accepts 10 digits or 11 digits with leading US country code `1`.
- **Output**: A single 10-digit string (e.g. `5551234567`). Returns `None` for invalid lengths.

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
- `phone_number`: Phone number (various input formats; normalized to a single 10-digit string with whitespace and non-digits removed)
- `address`: Street address
- `city`: City name
- `state`: State abbreviation
- `zip`: ZIP code

The dataset includes intentionally dirty data:
- Emails with extra spaces and mixed case
- Phone numbers with various punctuation formats (parentheses, dashes, dots, spaces); all normalized to a single 10-digit string
- One phone number with country code (1-XXX-XXX-XXXX), normalized to 10 digits
- One missing email
- One invalid phone number length (output as None)

## Dependencies

- **pytest**: Testing framework
- **pandas**: Data manipulation and analysis
- **pydantic**: Data validation (available for use)

## License

This is an exercise repository for educational purposes.
