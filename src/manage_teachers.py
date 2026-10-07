import getpass
import hashlib
import json
import os
import secrets
import sys
from pathlib import Path


CREDENTIALS_FILE = Path(__file__).with_name("teachers.json")
PASSWORD_ITERATIONS = 600_000


def add_teacher(username, password, credentials_file=CREDENTIALS_FILE):
    if not username or username.strip() != username or ":" in username:
        raise ValueError("Enter a username without leading/trailing spaces or colons.")
    if len(password) < 12:
        raise ValueError("Teacher passwords must be at least 12 characters.")

    data = {"teachers": {}}
    if credentials_file.exists():
        try:
            data = json.loads(credentials_file.read_text())
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError("The teacher credentials file is invalid.") from error
        if not isinstance(data, dict) or not isinstance(data.get("teachers"), dict):
            raise ValueError("The teacher credentials file has an invalid format.")

    salt = secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PASSWORD_ITERATIONS
    )
    data["teachers"][username] = {
        "salt": salt.hex(),
        "password_hash": password_hash.hex(),
        "iterations": PASSWORD_ITERATIONS,
    }

    credentials_file.parent.mkdir(parents=True, exist_ok=True)
    temporary_file = credentials_file.with_suffix(".json.tmp")
    temporary_file.write_text(json.dumps(data, indent=2) + "\n")
    os.chmod(temporary_file, 0o600)
    temporary_file.replace(credentials_file)


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python src/manage_teachers.py <username>")

    username = sys.argv[1]
    password = getpass.getpass("Teacher password (minimum 12 characters): ")
    confirmation = getpass.getpass("Confirm password: ")
    if password != confirmation:
        raise SystemExit("Passwords do not match.")

    try:
        add_teacher(username, password)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    print("Teacher credentials saved locally.")


if __name__ == "__main__":
    main()