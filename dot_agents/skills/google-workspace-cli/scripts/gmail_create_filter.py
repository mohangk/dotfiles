#!/usr/bin/env python3
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


SCOPES = [
    "https://mail.google.com/",
    "https://www.googleapis.com/auth/gmail.settings.basic",
    "https://www.googleapis.com/auth/gmail.labels",
    "https://www.googleapis.com/auth/gmail.modify",
]


def load_auth() -> dict:
    with tempfile.NamedTemporaryFile("w+", delete=True) as tmp:
        with open(tmp.name, "w") as out:
            subprocess.run(
                ["npx", "-y", "@googleworkspace/cli@0.22.5", "auth", "export", "--unmasked"],
                check=True,
                stdout=out,
            )
        text = Path(tmp.name).read_text()
    return json.loads(text[text.find("{") :])


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a Gmail filter using gws OAuth credentials.")
    parser.add_argument("--body", required=True, help="Filter body JSON.")
    args = parser.parse_args()

    auth = load_auth()
    creds = Credentials(
        token=None,
        refresh_token=auth["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=auth["client_id"],
        client_secret=auth["client_secret"],
        scopes=SCOPES,
    )
    creds.refresh(Request())
    service = build("gmail", "v1", credentials=creds, cache_discovery=False)
    created = service.users().settings().filters().create(
        userId="me",
        body=json.loads(args.body),
    ).execute()
    print(json.dumps(created, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
