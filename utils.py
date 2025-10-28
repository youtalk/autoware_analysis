"""
Shared utilities for Autoware contributor analysis.

This module provides common functionality used across all analysis scripts,
including file I/O operations, subprocess handling, and data processing utilities.
"""

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from datetime import datetime, date, timedelta
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FileSystemError(Exception):
    """Custom exception for file system operations."""
    pass


class SubprocessError(Exception):
    """Custom exception for subprocess operations."""
    pass


class DataProcessingError(Exception):
    """Custom exception for data processing operations."""
    pass


# Constants
TEMP_FILE = "tmp.txt"
DEFAULT_DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
OUTPUT_DATE_FORMAT = '%Y/%m/%d'
START_DATE = datetime(2022, 1, 1)

# Directory paths
GENERATED_JSON_DIR = Path("generated_json")
CONTRIBUTOR_NAMES_DIR = Path("contributor_names")
CONTRIBUTOR_HISTORY_DIR = Path("contributor_history")
TIER4_ENGINEERS_DIR = Path("tier4_engineers")
STARS_DIR = Path("stars")


def ensure_directories_exist() -> None:
    """Create necessary directories if they don't exist."""
    directories = [
        GENERATED_JSON_DIR,
        CONTRIBUTOR_NAMES_DIR,
        CONTRIBUTOR_HISTORY_DIR,
        TIER4_ENGINEERS_DIR,
        STARS_DIR,
    ]

    for directory in directories:
        try:
            directory.mkdir(exist_ok=True)
            logger.debug(f"Ensured directory exists: {directory}")
        except Exception as e:
            raise FileSystemError(f"Failed to create directory {directory}: {e}")


def run_bash_script(script: str, *args: str) -> Dict[str, Any]:
    """
    Execute a bash script and return the JSON result from tmp.txt.

    Args:
        script: Name of the bash script to execute
        *args: Arguments to pass to the script

    Returns:
        Parsed JSON data from the script output

    Raises:
        SubprocessError: If script execution fails
        DataProcessingError: If JSON parsing fails
    """
    try:
        result = subprocess.run(
            ["bash", script, *args],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            logger.error(f"Script {script} failed with return code {result.returncode}")
            logger.error(f"stderr: {result.stderr}")
            raise SubprocessError(f"Script {script} failed: {result.stderr}")

    except subprocess.TimeoutExpired:
        raise SubprocessError(f"Script {script} timed out after 60 seconds")
    except Exception as e:
        raise SubprocessError(f"Failed to execute script {script}: {e}")

    # Read the temporary file
    try:
        return read_json_file(TEMP_FILE)
    except FileNotFoundError:
        raise DataProcessingError(f"Temporary file {TEMP_FILE} not found after script execution")


def read_json_file(file_path: str | Path) -> Dict[str, Any]:
    """
    Read and parse a JSON file.

    Args:
        file_path: Path to the JSON file

    Returns:
        Parsed JSON data

    Raises:
        DataProcessingError: If file reading or JSON parsing fails
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise DataProcessingError(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        raise DataProcessingError(f"Invalid JSON in {file_path}: {e}")
    except Exception as e:
        raise DataProcessingError(f"Failed to read {file_path}: {e}")


def write_json_file(data: Any, file_path: str | Path, indent: int = 2) -> None:
    """
    Write data to a JSON file.

    Args:
        data: Data to write
        file_path: Path to the output file
        indent: JSON indentation level

    Raises:
        FileSystemError: If file writing fails
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent)
        logger.info(f"Successfully wrote JSON to {file_path}")
    except Exception as e:
        raise FileSystemError(f"Failed to write JSON to {file_path}: {e}")


def read_text_file(file_path: str | Path) -> List[str]:
    """
    Read a text file and return lines as a list.

    Args:
        file_path: Path to the text file

    Returns:
        List of lines (stripped of whitespace)

    Raises:
        FileSystemError: If file reading fails
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        raise FileSystemError(f"File not found: {file_path}")
    except Exception as e:
        raise FileSystemError(f"Failed to read {file_path}: {e}")


def write_text_file(lines: List[str], file_path: str | Path) -> None:
    """
    Write lines to a text file.

    Args:
        lines: List of lines to write
        file_path: Path to the output file

    Raises:
        FileSystemError: If file writing fails
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(f"{line}\n")
        logger.info(f"Successfully wrote {len(lines)} lines to {file_path}")
    except Exception as e:
        raise FileSystemError(f"Failed to write to {file_path}: {e}")


def write_sorted_names_to_file(names: Set[str], file_path: str | Path) -> None:
    """
    Write a sorted set of names to a file.

    Args:
        names: Set of names to write
        file_path: Path to the output file

    Raises:
        FileSystemError: If file writing fails
    """
    sorted_names = sorted(names)
    write_text_file(sorted_names, file_path)


def parse_datetime(date_string: str, date_format: str = DEFAULT_DATE_FORMAT) -> datetime:
    """
    Parse a datetime string into a datetime object.

    Args:
        date_string: String representation of a datetime
        date_format: Format string for parsing

    Returns:
        Parsed datetime object

    Raises:
        DataProcessingError: If parsing fails
    """
    try:
        return datetime.strptime(date_string, date_format)
    except ValueError as e:
        raise DataProcessingError(f"Failed to parse datetime '{date_string}': {e}")


def date_range(start: datetime, end: datetime, step: timedelta = timedelta(days=1)):
    """
    Generate a range of dates from start to end.

    Args:
        start: Start date
        end: End date
        step: Step size between dates

    Yields:
        datetime objects in the range
    """
    current = start
    while current < end:
        yield current
        current += step


def extract_author_login(node: Dict[str, Any]) -> Optional[str]:
    """
    Safely extract author login from a node.

    Args:
        node: Node dictionary that may contain author information

    Returns:
        Author login string, or None if not present
    """
    if node and "author" in node and node["author"]:
        return node["author"].get("login")
    return None


def extract_contributors_from_edges(
    edges: List[Dict[str, Any]],
    date_filter: Optional[datetime] = None,
    filter_after: bool = True
) -> Set[str]:
    """
    Extract unique contributor logins from GraphQL edges.

    Args:
        edges: List of GraphQL edge objects
        date_filter: Optional date to filter by
        filter_after: If True, include only contributions after date_filter;
                     if False, include only contributions before date_filter

    Returns:
        Set of unique contributor login names

    Raises:
        DataProcessingError: If data extraction fails
    """
    contributors: Set[str] = set()

    for edge in edges:
        try:
            node = edge.get("node", {})

            # Check date filter if provided
            if date_filter and "createdAt" in node:
                created_at = parse_datetime(node["createdAt"])
                if filter_after and created_at < date_filter:
                    continue
                if not filter_after and created_at >= date_filter:
                    continue

            # Extract author
            author = extract_author_login(node)
            if author:
                contributors.add(author)

            # Extract comment authors
            comments = node.get("comments", {}).get("edges", [])
            for comment_edge in comments:
                comment_node = comment_edge.get("node", {})
                comment_author = extract_author_login(comment_node)
                if comment_author:
                    contributors.add(comment_author)

        except Exception as e:
            logger.warning(f"Failed to process edge: {e}")
            continue

    return contributors


def merge_contributor_dicts(
    dict1: Dict[str, datetime],
    dict2: Dict[str, datetime]
) -> Dict[str, datetime]:
    """
    Merge two contributor dictionaries, keeping the earliest date for each contributor.

    Args:
        dict1: First dictionary (contributor -> first contribution date)
        dict2: Second dictionary (contributor -> first contribution date)

    Returns:
        Merged dictionary with earliest dates
    """
    result = dict1.copy()

    for contributor, date2 in dict2.items():
        if contributor not in result:
            result[contributor] = date2
        elif result[contributor] > date2:
            result[contributor] = date2

    return result


def count_contributors_by_day(
    contributors: Dict[str, datetime]
) -> Dict[date, int]:
    """
    Count how many contributors joined on each day.

    Args:
        contributors: Dictionary mapping contributor name to first contribution date

    Returns:
        Dictionary mapping date to count of new contributors that day
    """
    contributors_per_day: Dict[date, int] = {}

    for contributor_date in contributors.values():
        day = date(contributor_date.year, contributor_date.month, contributor_date.day)
        contributors_per_day[day] = contributors_per_day.get(day, 0) + 1

    return contributors_per_day


def format_csv_line(data: List[Any]) -> str:
    """
    Format a list of data into a CSV line.

    Args:
        data: List of values to format

    Returns:
        Comma-separated string
    """
    return ",".join(str(item) for item in data)
