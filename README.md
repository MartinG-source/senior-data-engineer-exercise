# Senior Data Engineer — Pairing Exercise

## Overview

You are a data engineer at a marketing platform company. The CRM team has asked you to build a **contact enrichment pipeline** that cleans raw contact data, joins it with preference and engagement data, and produces an enriched output used for campaign targeting.

This exercise is designed to be completed collaboratively during a live pairing session. We will work through it together using **test-driven development (TDD)**: write a failing test, implement the logic, then refactor.

## What We're Evaluating

- **TDD workflow** — Can you write a focused test before implementing logic?
- **Data transformation skills** — Comfort with Pandas (or PySpark) for cleaning, normalizing, and joining datasets.
- **Problem decomposition** — Can you break a complex, multi-dataset problem into small, testable steps?
- **Communication** — Talk through your thinking as you go.

## Repository Layout

```
senior-data-engineer-exercise/
├── data/
│   ├── input/
│   │   ├── contacts.csv                    # Raw contact records (messy)
│   │   ├── contacts_schema.csv             # Schema for contacts
│   │   ├── contact_preferences.csv         # Channel & consent preferences
│   │   ├── contact_preferences_schema.csv  # Schema for preferences
│   │   ├── engagement_events.csv           # Historical engagement events
│   │   ├── engagement_events_schema.csv    # Schema for events
│   │   ├── target_schema.csv               # Target output schema
│   │   └── transformation_constraints.csv  # Business rules / constraints
│   └── output/
├── src/
│   └── transforms.py          # Transformation functions (stubs provided)
├── test/
│   └── test_transforms.py     # Test suite (2 passing examples provided)
├── requirements.txt
└── README.md
```

## Setup

```bash
cd senior-data-engineer-exercise
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run Tests

```bash
pytest test/ -v
```

## The Data

You have three input datasets that share `contact_id` as a foreign key:


| Dataset                   | Description                                                                                    |
| ------------------------- | ---------------------------------------------------------------------------------------------- |
| `contacts.csv`            | 8 contact records with intentionally messy data (whitespace, mixed case, inconsistent formats) |
| `contact_preferences.csv` | Each contact's preferred channel and opt-in/opt-out status                                     |
| `engagement_events.csv`   | Historical interaction events (opens, clicks, bounces, unsubscribes)                           |


Review the schema files and `transformation_constraints.csv` to understand the business rules.

---

## Exercise Steps

Work through these in order. Each step follows the same TDD cycle:
**Red** (write a failing test) → **Green** (implement just enough to pass) → **Refactor**

### Step 1 — Verify Baseline

Run `pytest test/ -v` and confirm the existing tests pass. These test `normalize_address`, which is already implemented as an example.

### Step 2 — Normalize Email

Implement `normalize_email()` in `src/transforms.py`.

Rules (from `transformation_constraints.csv`):

- Remove leading/trailing whitespace
- Convert to lowercase
- Return `None` for empty or missing values

### Step 3 — Normalize Phone

Implement `normalize_phone()` in `src/transforms.py`.

Rules:

- Strip all non-digit characters
- Valid formats: 10-digit, or 11-digit starting with `1`
- Format as `(XXX) XXX-XXXX` or `1-(XXX) XXX-XXXX`
- Return `None` for invalid inputs

This is intentionally more complex — we'd like to see you break it into smaller pieces.

### Step 4 — Normalize State & ZIP

Implement `normalize_state()` and `normalize_zip()` in `src/transforms.py`.

Rules:

- **State**: Normalize to uppercase 2-letter code (e.g., `"Texas"` → `"TX"`, `" il "` → `"IL"`)
- **ZIP**: Normalize to 5-digit string (e.g., `"90001-3344"` → `"90001"`, `"77001.0"` → `"77001"`)
- Return `None` for values that can't be normalized

### Step 5 — Contact Enrichment (Join + Derive)

This is the core design challenge. Join all three datasets and derive new fields:


| Field                         | Type    | Logic                                                                                                                                         |
| ----------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `contactable`                 | boolean | `True` if the contact has a valid email OR valid phone after normalization                                                                    |
| `preferred_reachable_channel` | string  | The contact's preferred channel, but only if that channel is actually valid after normalization. Falls back to any valid channel, or `"none"` |
| `do_not_contact`              | boolean | `True` if both `marketing_opt_in` and `transactional_opt_in` are `"no"`, OR if the contact has an `unsubscribe` event                         |
| `contact_quality_tier`        | string  | `"high"` / `"medium"` / `"low"` / `"unreachable"` based on valid channels + engagement recency                                                |


**We don't expect you to finish this in the time allotted.** What we want to see is:

1. How you decompose it into smaller functions
2. What tests you'd write first
3. How you handle the joins and edge cases
4. How you reason about conflicting signals across datasets

---

## Notes

- The 2 existing tests for `normalize_address` show the test pattern we expect.
- Write tests that assert on specific inputs, not on row indices — the example tests use row indices for simplicity, but direct-input tests are better.
- You're free to use Pandas or PySpark. The stubs use Pandas but you can switch.
- Focus on clear, testable logic over clever one-liners.
- Ask questions — this is a conversation, not an exam.

