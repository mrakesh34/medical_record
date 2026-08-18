
import re
import csv
from pathlib import Path
from datetime import datetime

print (dir(csv))
import re
print(re.__file__)


NOTES_DIR = Path("sample_notes")
OUTPUT_CSV = Path("extracted.csv")


def normalize_date(date_string):
    formats = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%Y/%m/%d",
        "%d %b %Y",
        "%B %d, %Y",
    ]

    for fmt in formats:
        try:
            date = datetime.strptime(date_string, fmt)
            return date.strftime("%m/%d/%Y")
        except ValueError:
            continue

    return None


def extract_fields(text: str) -> dict:

    def find_label(patterns):
        for pattern in patterns:
            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE | re.MULTILINE
            )
            if match:
                return match.group(1).strip()
        return None

    mrn = find_label([
        r"^\s*(?:MRN|MRN\s*#)\s*[:#]?\s*(\d+)\s*$",
        r"^\s*Medical\s+Record\s+Number\s*[:#]?\s*(\d+)\s*$",
    ])

    dob = find_label([
        r"^\s*DOB\s*[:#]?\s*(.+?)\s*$",
        r"^\s*Date\s+of\s+Birth\s*[:#]?\s*(.+?)\s*$",
    ])

    date_of_service = find_label([
        r"^\s*Date\s+of\s+Service\s*[:#]?\s*(.+?)\s*$",
        r"^\s*DOS\s*[:#]?\s*(.+?)\s*$",
    ])

    def normalize_or_missing(value):
        if not value:
            return "MISSING"

        normalized = normalize_date(value)
        return normalized if normalized else "MISSING"

    return {
        "mrn": mrn if mrn else "MISSING",
        "dob": normalize_or_missing(dob),
        "date_of_service": normalize_or_missing(date_of_service),
    }

def process_all_notes(notes_dir: Path) -> list:
    rows = []

    for filepath in sorted(notes_dir.glob("*.txt")):
        text = filepath.read_text()
        fields = extract_fields(text)
        fields["filename"] = filepath.name
        rows.append(fields)

    return rows


def write_csv(rows: list, output_path: Path) -> None:
    fieldnames = ["filename", "mrn", "dob", "date_of_service"]
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


if __name__ == "__main__":
    rows = process_all_notes(NOTES_DIR)
    write_csv(rows, OUTPUT_CSV)
    print(f"Wrote {len(rows)} rows to {OUTPUT_CSV}")
    for row in rows:
        print(row)