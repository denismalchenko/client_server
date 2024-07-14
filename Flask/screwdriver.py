import argparse
import os
import requests

SERVER_URL = "http://localhost:8888"


def script_args():
    parser = argparse.ArgumentParser(
        description="Screwdriver - for upload audio files to the server."
    )
    parser.add_argument(
        "command",
        type=str,
        choices=["upload", "list"],
        help="The command to execute: upload or list.",
    )
    parser.add_argument(
        "file", type=str, nargs="?", help="A file to upload to the server."
    )
    args = parser.parse_args()
    return args.command, args.file


def upload_file(filename: str) -> None:
    if not os.path.exists(filename):
        print("File does not exist")
        return
    try:
        with open(filename, "rb") as file:
            response = requests.post(
                SERVER_URL, files={"file": file}, headers={"Accept": "application/json"}
            )
            response.raise_for_status()
            print(response.json().get("message", ""))
    except Exception as err:
        print_exception(err)


def list_files() -> None:
    try:
        response = requests.get(SERVER_URL, headers={"Accept": "application/json"})
        response.raise_for_status()
        files = response.json().get("files", [])
        if len(files) == 0:
            print("No files found")
        else:
            for file in files:
                print(file)
    except Exception as err:
        print_exception(err)


def print_exception(err):
    if isinstance(err, requests.exceptions.HTTPError):
        print("A server error occured. HTTP:", err)
    elif isinstance(err, requests.exceptions.ConnectionError):
        print("A connection error occured:", err)
    elif isinstance(err, FileNotFoundError):
        print("File not found:", err)
    elif isinstance(err, PermissionError):
        print("No access to the file:", err)
    elif isinstance(err, IOError):
        print("An Input/Output error occured:", err)
    elif isinstance(err, OSError):
        print("An operating system error occured:", err)
    else:
        print("An error occured:", err)


if __name__ == "__main__":
    command, file = script_args()
    if command == "upload":
        if file is None:
            print("Please specify a file to upload")
        else:
            upload_file(file)
    elif command == "list":
        list_files()
