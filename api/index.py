import os
from pathlib import Path

# Base directory containing the web assets
BASE_DIR = Path(__file__).resolve().parent.parent

def app(environ, start_response):
    """
    Standard WSGI entrypoint for Vercel Serverless Function.
    Serves the Nalanda University Faculty Directory web dashboard,
    the Excel spreadsheet, and the JSON dataset.
    """
    raw_path = environ.get("PATH_INFO", "/").strip("/")
    
    if not raw_path or raw_path == "" or raw_path == "index.html":
        target_file = BASE_DIR / "index.html"
        content_type = "text/html; charset=utf-8"
    elif raw_path.endswith(".xlsx"):
        target_file = BASE_DIR / "faculty_directory.xlsx"
        content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif raw_path.endswith(".json"):
        target_file = BASE_DIR / "faculty_data.json"
        content_type = "application/json; charset=utf-8"
    else:
        # Check if file exists directly in root or public
        candidate = BASE_DIR / raw_path
        if candidate.exists() and candidate.is_file():
            target_file = candidate
            content_type = "application/octet-stream"
        else:
            target_file = BASE_DIR / "index.html"
            content_type = "text/html; charset=utf-8"

    if target_file.exists() and target_file.is_file():
        data = target_file.read_bytes()
        status = "200 OK"
        headers = [
            ("Content-Type", content_type),
            ("Content-Length", str(len(data))),
            ("Cache-Control", "public, max-age=3600")
        ]
        start_response(status, headers)
        return [data]

    status = "404 Not Found"
    headers = [("Content-Type", "text/plain; charset=utf-8")]
    start_response(status, headers)
    return [b"Resource not found"]

# Aliases supported by Vercel
handler = app
