# Warmup Exercise: Extract Patient Metadata from Clinical Notes

## Setup

You have a folder `sample_notes/` containing 6 `.txt` files — each one a
plain-text clinical note from a different (fictional) clinic. Your job is
to read every file in the folder, pull out three fields from each note,
and write the results to a single CSV file.

## Fields to extract

| Field             | Description                                   |
| ----------------- | --------------------------------------------- |
| `mrn`             | Medical Record Number                         |
| `dob`             | Date of Birth, normalized to `MM/DD/YYYY`     |
| `date_of_service` | Date of the visit, normalized to `MM/DD/YYYY` |

## Task

1. Open `extract.py`. Implement `extract_fields(text)`.
2. Run `python extract.py`. It should create `extracted.csv` with one row
   per note, columns: `filename, mrn, dob, date_of_service`.
3. Look through `sample_notes/*.txt` **before** you start writing regex —
   the six files are not all formatted the same way on purpose.

## Things your solution needs to handle

Look closely at the sample notes and you'll find real variation in:

- **Label wording**: "MRN", "MRN #", "Medical Record Number" all mean the
  same field.
- **Case and spacing**: some notes use lowercase labels with extra
  whitespace (`mrn:    558102`).
- **Date formats**: `03/14/1967`, `March 2, 1981`, and `1990-11-23` should
  all normalize to `MM/DD/YYYY` in your output.
- **Decoy dates**: at least one note contains a date in the narrative
  paragraph (not labeled as DOB or DOS) that a naive "just grab any date
  in the file" approach would incorrectly extract. Your extraction needs
  to be anchored to the actual labels.
- **Missing fields**: at least one note is missing a field entirely. Your
  code should not crash — it should write `"MISSING"` for that cell and
  keep going.

## What "done" looks like

- `python extract.py` runs without errors on all 6 files.
- `extracted.csv` has 6 rows, correct filenames, and all dates normalized
  to `MM/DD/YYYY`.
- Exactly one row has `mrn = MISSING` (note_005), and no row has a
  hallucinated MRN or the wrong date pulled from narrative text.

## Note on using AI

You're welcome to use AI for this one — it's a warmup. But paste in a
generic regex from an AI tool and run it against all 6 files before you
trust it. If it gets note_004 or note_006 wrong, that's expected the
first time; fixing it is the actual exercise.
