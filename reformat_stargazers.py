"""
Reformat stargazer data into daily star counts.

This script processes the raw stargazer JSON data and converts it into
a CSV file with daily star counts and cumulative totals.
"""

from typing import Dict
from datetime import date

from utils import (
    read_json_file,
    ensure_directories_exist,
    parse_datetime,
    STARS_DIR,
    OUTPUT_DATE_FORMAT,
    logger,
    DataProcessingError,
)


def count_stars_per_day(stargazers_file: str) -> Dict[date, int]:
    """
    Count how many stars were added on each day.

    Args:
        stargazers_file: Path to stargazers JSON file

    Returns:
        Dictionary mapping date to count of stars added that day

    Raises:
        DataProcessingError: If data processing fails
    """
    try:
        edges = read_json_file(STARS_DIR / stargazers_file)
        stars_per_day: Dict[date, int] = {}

        logger.info(f"Processing {len(edges)} stargazers")

        for edge in edges:
            if "starredAt" not in edge:
                logger.warning("Stargazer edge missing 'starredAt' field")
                continue

            try:
                starred_at = parse_datetime(edge["starredAt"])
                day = date(starred_at.year, starred_at.month, starred_at.day)

                stars_per_day[day] = stars_per_day.get(day, 0) + 1

            except DataProcessingError:
                logger.warning(f"Failed to parse date: {edge.get('starredAt')}")
                continue

        logger.info(f"Counted stars across {len(stars_per_day)} days")
        return stars_per_day

    except Exception as e:
        raise DataProcessingError(f"Failed to count stars from {stargazers_file}: {e}")


def write_star_counts_to_csv(stars_per_day: Dict[date, int], output_file: str) -> None:
    """
    Write star counts to CSV file with cumulative totals.

    Args:
        stars_per_day: Dictionary mapping date to count of stars
        output_file: Output CSV file path

    Raises:
        Exception: If file writing fails
    """
    try:
        with open(STARS_DIR / output_file, 'w', encoding='utf-8') as f:
            cumulative_count = 0

            for day in sorted(stars_per_day.keys()):
                count = stars_per_day[day]
                cumulative_count += count

                line = f"{day.strftime(OUTPUT_DATE_FORMAT)},{count},{cumulative_count}"
                f.write(f"{line}\n")

        logger.info(f"Successfully wrote star counts to {output_file}")

    except Exception as e:
        raise Exception(f"Failed to write star counts to {output_file}: {e}")


def main() -> None:
    """Main execution function."""
    try:
        # Ensure output directory exists
        ensure_directories_exist()

        # Process stargazer data
        input_file = "stargazers.json"
        output_file = "counted_stars.csv"

        logger.info("Counting stars per day...")
        stars_per_day = count_stars_per_day(input_file)

        logger.info("Writing star counts to CSV...")
        write_star_counts_to_csv(stars_per_day, output_file)

        total_stars = sum(stars_per_day.values())
        logger.info(f"Successfully processed {total_stars} total stars")

    except Exception as e:
        logger.error(f"Fatal error in main execution: {e}")
        raise


if __name__ == "__main__":
    main()
