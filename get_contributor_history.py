"""
Generate contributor history tracking cumulative growth over time.

This script analyzes contributor data from JSON files and tracks when each
contributor first appeared, generating daily counts and cumulative totals.
"""

from typing import Dict, List
from datetime import datetime, date

from utils import (
    read_json_file,
    ensure_directories_exist,
    parse_datetime,
    extract_author_login,
    date_range,
    count_contributors_by_day,
    merge_contributor_dicts,
    format_csv_line,
    GENERATED_JSON_DIR,
    CONTRIBUTOR_HISTORY_DIR,
    START_DATE,
    OUTPUT_DATE_FORMAT,
    logger,
    DataProcessingError,
)


def extract_contributors_with_dates(json_file: str) -> Dict[str, datetime]:
    """
    Extract contributors and their first contribution date from a JSON file.

    Args:
        json_file: Path to JSON file containing edges

    Returns:
        Dictionary mapping contributor login to their first contribution date

    Raises:
        DataProcessingError: If data extraction fails
    """
    try:
        edges = read_json_file(GENERATED_JSON_DIR / json_file)
        contributors: Dict[str, datetime] = {}

        logger.info(f"Processing {len(edges)} edges from {json_file}")

        for edge in edges:
            node = edge.get("node", {})

            # Check if contribution is after start date
            if "createdAt" not in node:
                continue

            try:
                created_at = parse_datetime(node["createdAt"])
            except DataProcessingError:
                logger.warning(f"Failed to parse date in {json_file}")
                continue

            if created_at < START_DATE:
                continue

            # Extract author and track earliest contribution
            author = extract_author_login(node)
            if author:
                if author not in contributors:
                    contributors[author] = created_at
                elif contributors[author] > created_at:
                    contributors[author] = created_at

            # Extract comment authors and their dates
            comments = node.get("comments", {}).get("edges", [])
            for comment_edge in comments:
                comment_node = comment_edge.get("node", {})

                if "createdAt" not in comment_node:
                    continue

                try:
                    comment_date = parse_datetime(comment_node["createdAt"])
                except DataProcessingError:
                    continue

                comment_author = extract_author_login(comment_node)
                if comment_author:
                    if comment_author not in contributors:
                        contributors[comment_author] = comment_date
                    elif contributors[comment_author] > comment_date:
                        contributors[comment_author] = comment_date

        logger.info(f"Extracted {len(contributors)} unique contributors with dates from {json_file}")
        return contributors

    except Exception as e:
        raise DataProcessingError(f"Failed to extract contributors from {json_file}: {e}")


def write_history_to_file(
    contributors_per_day: Dict[date, int],
    file_path: str
) -> None:
    """
    Write contributor history to a text file with cumulative counts.

    Args:
        contributors_per_day: Dictionary mapping date to count of new contributors
        file_path: Output file path

    Raises:
        Exception: If file writing fails
    """
    try:
        with open(CONTRIBUTOR_HISTORY_DIR / file_path, 'w', encoding='utf-8') as f:
            cumulative_count = 0

            for day, count in sorted(contributors_per_day.items()):
                cumulative_count += count
                line = f"{day.strftime(OUTPUT_DATE_FORMAT)},{count},{cumulative_count}"
                f.write(f"{line}\n")

        logger.info(f"Successfully wrote history to {file_path}")

    except Exception as e:
        raise Exception(f"Failed to write history to {file_path}: {e}")


def write_combined_csv(
    autoware_per_day: Dict[date, int],
    code_per_day: Dict[date, int],
    community_per_day: Dict[date, int],
    file_path: str
) -> None:
    """
    Write combined contributor history to CSV file.

    Args:
        autoware_per_day: All autoware contributors by day
        code_per_day: Code contributors by day
        community_per_day: Community contributors by day
        file_path: Output file path

    Raises:
        Exception: If file writing fails
    """
    try:
        end_date = datetime.today()

        with open(CONTRIBUTOR_HISTORY_DIR / file_path, 'w', encoding='utf-8') as f:
            # Write header
            f.write("date,autoware_contributors,code_contributors,community_contributors\n")

            # Initialize cumulative counts
            autoware_cumulative = 0
            code_cumulative = 0
            community_cumulative = 0

            # Write data for each day
            for day in date_range(START_DATE, end_date):
                day_date = date(day.year, day.month, day.day)

                updated = False

                # Update counts if there were contributions on this day
                if day_date in autoware_per_day:
                    autoware_cumulative += autoware_per_day[day_date]
                    updated = True

                if day_date in code_per_day:
                    code_cumulative += code_per_day[day_date]
                    updated = True

                if day_date in community_per_day:
                    community_cumulative += community_per_day[day_date]
                    updated = True

                # Only write lines where there was an update
                if updated:
                    line = format_csv_line([
                        day.strftime(OUTPUT_DATE_FORMAT),
                        autoware_cumulative,
                        code_cumulative,
                        community_cumulative
                    ])
                    f.write(f"{line}\n")

        logger.info(f"Successfully wrote combined CSV to {file_path}")

    except Exception as e:
        raise Exception(f"Failed to write combined CSV to {file_path}: {e}")


def main() -> None:
    """Main execution function."""
    try:
        # Ensure output directories exist
        ensure_directories_exist()

        # Initialize contributor dictionaries
        code_contributors: Dict[str, datetime] = {}
        community_contributors: Dict[str, datetime] = {}

        # Extract community contributors (discussions and issues)
        community_sources = [
            "autoware_discussions.json",
            "autoware_issues.json",
            "universe_issues.json",
            "autoware_core_issues.json",
            "autoware_msgs_issues.json",
            "autoware_launch_issues.json",
            "autoware_documentation_issues.json",
        ]

        logger.info("Extracting community contributors...")
        for source in community_sources:
            try:
                contributors = extract_contributors_with_dates(source)
                community_contributors = merge_contributor_dicts(community_contributors, contributors)
            except DataProcessingError as e:
                logger.warning(f"Skipping {source}: {e}")
                continue

        # Extract code contributors (pull requests)
        code_sources = [
            "autoware_prs.json",
            "universe_prs.json",
            "autoware_core_prs.json",
            "autoware_msgs_prs.json",
            "autoware_launch_prs.json",
            "autoware_documentation_prs.json",
        ]

        logger.info("Extracting code contributors...")
        for source in code_sources:
            try:
                contributors = extract_contributors_with_dates(source)
                code_contributors = merge_contributor_dicts(code_contributors, contributors)
            except DataProcessingError as e:
                logger.warning(f"Skipping {source}: {e}")
                continue

        # Merge all autoware contributors
        autoware_contributors = merge_contributor_dicts(community_contributors, code_contributors)

        # Count contributors by day
        logger.info("Counting contributors by day...")
        code_per_day = count_contributors_by_day(code_contributors)
        community_per_day = count_contributors_by_day(community_contributors)
        autoware_per_day = count_contributors_by_day(autoware_contributors)

        # Write individual history files
        logger.info("Writing history files...")
        write_history_to_file(code_per_day, "code_contributors_per_day.txt")
        write_history_to_file(community_per_day, "community_contributors_per_day.txt")
        write_history_to_file(autoware_per_day, "autoware_contributors_per_day.txt")

        # Write combined CSV
        write_combined_csv(
            autoware_per_day,
            code_per_day,
            community_per_day,
            "contributors_count.csv"
        )

        # Log summary
        logger.info(f"Total code contributors: {len(code_contributors)}")
        logger.info(f"Total community contributors: {len(community_contributors)}")
        logger.info(f"Total autoware contributors: {len(autoware_contributors)}")

        logger.info("Successfully completed contributor history generation")

    except Exception as e:
        logger.error(f"Fatal error in main execution: {e}")
        raise


if __name__ == "__main__":
    main()
