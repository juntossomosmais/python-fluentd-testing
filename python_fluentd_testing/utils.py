import json
import os
import pathlib
import subprocess
from contextlib import contextmanager
from time import sleep
from typing import List
from typing import Optional


def execute_shell_command(commands_list: List[str]):
    built_command = " ".join(commands_list)
    output = subprocess.Popen(built_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    stdout, stderr = output.communicate()
    return stdout, stderr


@contextmanager
def execute_system_command_and_does_not_await_its_execution(commands_list: List[str]):
    built_command = " ".join(commands_list)
    try:
        process = subprocess.Popen(built_command, shell=True)
        sleep(7)
        yield
    finally:
        process.kill()


def create_file_with_full_permission(file_location):
    pathlib.Path(file_location).touch(mode=0o644, exist_ok=False)


def number_of_lines(file_name: str) -> int:
    with open(file_name, mode="r") as file:
        return sum(1 for row in file)


def create_all_folders_if_needed(path: str):
    if not os.path.exists(path):
        os.makedirs(path, mode=0o755, exist_ok=True)


def delete_all_log_files_contained_in_the_folder(folder_path: str):
    folder = pathlib.Path(folder_path)
    if folder.exists():
        for each_file_path in folder.glob("*.log"):
            print(f"Removing {each_file_path}...")
            each_file_path.unlink()


def last_line_from_some_file(file: str) -> Optional[str]:
    with open(file, "r") as f:
        lines = f.read().splitlines()
        return lines[-1] if lines else None


def erase_file_content(file_location: str):
    folder = pathlib.Path(file_location)
    if folder.exists():
        with open(file_location, "r+") as f:
            f.truncate(0)


def try_to_get_last_line_as_json(file_location: str, max_tries=3, await_in_seconds_between_tries=1) -> Optional[dict]:
    attempts = 0
    while True:
        line = last_line_from_some_file(file_location)
        line_as_json = json.loads(line) if line else None
        if line_as_json:
            return line_as_json
        if attempts >= max_tries:
            return None
        sleep(await_in_seconds_between_tries)
        attempts += 1
