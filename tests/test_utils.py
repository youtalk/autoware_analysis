"""
Unit tests for utils module.
"""

import unittest
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime, date, timedelta
from pathlib import Path
import json
import tempfile
import os

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    read_json_file,
    write_json_file,
    read_text_file,
    write_text_file,
    write_sorted_names_to_file,
    parse_datetime,
    date_range,
    extract_author_login,
    extract_contributors_from_edges,
    merge_contributor_dicts,
    count_contributors_by_day,
    format_csv_line,
    DataProcessingError,
    FileSystemError,
)


class TestFileOperations(unittest.TestCase):
    """Test file I/O operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test.json"

    def tearDown(self):
        """Clean up test files."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_write_and_read_json_file(self):
        """Test writing and reading JSON files."""
        test_data = {"key": "value", "list": [1, 2, 3]}

        write_json_file(test_data, self.test_file)
        result = read_json_file(self.test_file)

        self.assertEqual(result, test_data)

    def test_read_nonexistent_json_file(self):
        """Test reading a non-existent JSON file raises error."""
        with self.assertRaises(DataProcessingError):
            read_json_file(Path(self.temp_dir) / "nonexistent.json")

    def test_write_and_read_text_file(self):
        """Test writing and reading text files."""
        test_lines = ["line1", "line2", "line3"]
        test_file = Path(self.temp_dir) / "test.txt"

        write_text_file(test_lines, test_file)
        result = read_text_file(test_file)

        self.assertEqual(result, test_lines)

    def test_write_sorted_names_to_file(self):
        """Test writing sorted names to file."""
        names = {"charlie", "alice", "bob"}
        test_file = Path(self.temp_dir) / "names.txt"

        write_sorted_names_to_file(names, test_file)
        result = read_text_file(test_file)

        self.assertEqual(result, ["alice", "bob", "charlie"])


class TestDateTimeOperations(unittest.TestCase):
    """Test datetime operations."""

    def test_parse_datetime_valid(self):
        """Test parsing valid datetime string."""
        date_string = "2022-01-15T10:30:45Z"
        result = parse_datetime(date_string)

        self.assertEqual(result.year, 2022)
        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 15)

    def test_parse_datetime_invalid(self):
        """Test parsing invalid datetime string raises error."""
        with self.assertRaises(DataProcessingError):
            parse_datetime("invalid-date")

    def test_date_range(self):
        """Test date range generator."""
        start = datetime(2022, 1, 1)
        end = datetime(2022, 1, 5)

        dates = list(date_range(start, end))

        self.assertEqual(len(dates), 4)
        self.assertEqual(dates[0], start)
        self.assertEqual(dates[-1], datetime(2022, 1, 4))

    def test_date_range_with_step(self):
        """Test date range with custom step."""
        start = datetime(2022, 1, 1)
        end = datetime(2022, 1, 10)
        step = timedelta(days=2)

        dates = list(date_range(start, end, step))

        self.assertEqual(len(dates), 5)
        self.assertEqual(dates[1], datetime(2022, 1, 3))


class TestContributorExtraction(unittest.TestCase):
    """Test contributor extraction functions."""

    def test_extract_author_login_valid(self):
        """Test extracting author login from valid node."""
        node = {"author": {"login": "testuser"}}
        result = extract_author_login(node)

        self.assertEqual(result, "testuser")

    def test_extract_author_login_none(self):
        """Test extracting author login from None."""
        result = extract_author_login(None)

        self.assertIsNone(result)

    def test_extract_author_login_no_author(self):
        """Test extracting author login when author is None."""
        node = {"author": None}
        result = extract_author_login(node)

        self.assertIsNone(result)

    def test_extract_contributors_from_edges(self):
        """Test extracting contributors from edges."""
        edges = [
            {
                "node": {
                    "author": {"login": "user1"},
                    "createdAt": "2022-01-15T10:00:00Z",
                    "comments": {
                        "edges": [
                            {"node": {"author": {"login": "user2"}}}
                        ]
                    }
                }
            },
            {
                "node": {
                    "author": {"login": "user3"},
                    "createdAt": "2022-01-16T10:00:00Z",
                    "comments": {"edges": []}
                }
            }
        ]

        result = extract_contributors_from_edges(edges)

        self.assertEqual(result, {"user1", "user2", "user3"})

    def test_extract_contributors_with_date_filter(self):
        """Test extracting contributors with date filter."""
        edges = [
            {
                "node": {
                    "author": {"login": "user1"},
                    "createdAt": "2022-01-15T10:00:00Z",
                    "comments": {"edges": []}
                }
            },
            {
                "node": {
                    "author": {"login": "user2"},
                    "createdAt": "2021-12-15T10:00:00Z",
                    "comments": {"edges": []}
                }
            }
        ]

        date_filter = datetime(2022, 1, 1)
        result = extract_contributors_from_edges(edges, date_filter, filter_after=True)

        self.assertEqual(result, {"user1"})


class TestContributorAggregation(unittest.TestCase):
    """Test contributor aggregation functions."""

    def test_merge_contributor_dicts(self):
        """Test merging contributor dictionaries."""
        dict1 = {
            "user1": datetime(2022, 1, 15),
            "user2": datetime(2022, 1, 20),
        }
        dict2 = {
            "user2": datetime(2022, 1, 10),  # Earlier date
            "user3": datetime(2022, 1, 25),
        }

        result = merge_contributor_dicts(dict1, dict2)

        self.assertEqual(result["user1"], datetime(2022, 1, 15))
        self.assertEqual(result["user2"], datetime(2022, 1, 10))  # Should use earlier date
        self.assertEqual(result["user3"], datetime(2022, 1, 25))

    def test_count_contributors_by_day(self):
        """Test counting contributors by day."""
        contributors = {
            "user1": datetime(2022, 1, 15, 10, 0, 0),
            "user2": datetime(2022, 1, 15, 14, 0, 0),
            "user3": datetime(2022, 1, 16, 9, 0, 0),
        }

        result = count_contributors_by_day(contributors)

        self.assertEqual(result[date(2022, 1, 15)], 2)
        self.assertEqual(result[date(2022, 1, 16)], 1)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""

    def test_format_csv_line(self):
        """Test formatting CSV line."""
        data = ["2022/01/15", 10, 25, 35]
        result = format_csv_line(data)

        self.assertEqual(result, "2022/01/15,10,25,35")

    def test_format_csv_line_mixed_types(self):
        """Test formatting CSV line with mixed types."""
        data = ["text", 123, 45.67, True]
        result = format_csv_line(data)

        self.assertEqual(result, "text,123,45.67,True")


class TestErrorHandling(unittest.TestCase):
    """Test error handling."""

    def test_read_invalid_json(self):
        """Test reading invalid JSON raises error."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            f.write("invalid json {")
            temp_file = f.name

        try:
            with self.assertRaises(DataProcessingError):
                read_json_file(temp_file)
        finally:
            os.unlink(temp_file)


if __name__ == "__main__":
    unittest.main()
