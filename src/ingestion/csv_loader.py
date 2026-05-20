import csv
import io
from fastapi import UploadFile, HTTPException


async def load_csv_to_rows(file: UploadFile, expected_fields: list[str]) -> list[dict]:
    content = await file.read()
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = content.decode("latin-1")

    reader = csv.DictReader(io.StringIO(text))
    rows = list(reader)
    if not rows:
        raise HTTPException(400, "CSV file is empty")

    missing = [f for f in expected_fields if f not in rows[0]]
    if missing:
        raise HTTPException(400, f"CSV missing required columns: {missing}")

    return rows
