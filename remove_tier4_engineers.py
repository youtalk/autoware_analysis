"""
Count contributors and identify Tier4 engineers.

This script reads contributor lists and identifies how many are Tier4 employees
by comparing against the Tier4 organization member list.
"""

from typing import List, Set
from pathlib import Path

from utils import (
    read_text_file,
    ensure_directories_exist,
    CONTRIBUTOR_NAMES_DIR,
    TIER4_ENGINEERS_DIR,
    logger,
    FileSystemError,
)


def count_tier4_contributors(contributor_file: str, tier4_engineers: Set[str]) -> tuple[int, int]:
    """
    Count total contributors and how many are Tier4 engineers.

    Args:
        contributor_file: Path to contributor file
        tier4_engineers: Set of Tier4 engineer login names

    Returns:
        Tuple of (total_contributors, tier4_contributors)

    Raises:
        FileSystemError: If file reading fails
    """
    try:
        contributors = read_text_file(CONTRIBUTOR_NAMES_DIR / contributor_file)
        tier4_count = sum(1 for contributor in contributors if contributor in tier4_engineers)

        return len(contributors), tier4_count

    except FileSystemError as e:
        logger.warning(f"Failed to read {contributor_file}: {e}")
        return 0, 0


def main() -> None:
    """Main execution function."""
    try:
        # Ensure directories exist
        ensure_directories_exist()

        # Load Tier4 engineers list
        tier4_file = TIER4_ENGINEERS_DIR / "tier4_engineers.txt"
        try:
            tier4_engineers_list = read_text_file(tier4_file)
            tier4_engineers = set(tier4_engineers_list)
            logger.info(f"Loaded {len(tier4_engineers)} Tier4 engineers")
        except FileSystemError as e:
            logger.error(f"Failed to load Tier4 engineers list: {e}")
            raise

        # List of contributor files to analyze
        contributor_files = [
            # Main aggregated files
            "autoware_code_contributors.txt",
            "autoware_community_contributors.txt",
            "autoware_contributors.txt",

            # Autoware main repository
            "autoware_discussions.txt",
            "autoware_issues.txt",
            "autoware_prs.txt",

            # Autoware universe
            "universe_issues.txt",
            "universe_prs.txt",

            # Autoware core
            "autoware_core_issues.txt",
            "autoware_core_prs.txt",

            # Autoware msgs
            "autoware_msgs_issues.txt",
            "autoware_msgs_prs.txt",

            # Autoware launch
            "autoware_launch_issues.txt",
            "autoware_launch_prs.txt",

            # Autoware documentation
            "autoware_documentation_issues.txt",
            "autoware_documentation_prs.txt",

            # Autoware AI repositories
            "autoware_ai_issues.txt",
            "autoware_ai_prs.txt",
            "autoware_ai_planning_issues.txt",
            "autoware_ai_planning_prs.txt",
            "autoware_ai_perception_issues.txt",
            "autoware_ai_perception_prs.txt",
            "autoware_ai_messages_issues.txt",
            "autoware_ai_messages_prs.txt",
            "autoware_ai_simulation_issues.txt",
            "autoware_ai_simulation_prs.txt",
            "autoware_ai_visualization_issues.txt",
            "autoware_ai_visualization_prs.txt",
            "autoware_ai_drivers_issues.txt",
            "autoware_ai_drivers_prs.txt",
            "autoware_ai_utilities_issues.txt",
            "autoware_ai_utilities_prs.txt",
            "autoware_ai_common_issues.txt",
            "autoware_ai_common_prs.txt",
        ]

        # Analyze each contributor file
        logger.info("Analyzing contributor files...")
        print("\nContributor Analysis Results:")
        print("=" * 80)
        print(f"{'File':<50} {'Total':<10} {'Tier4':<10} {'External':<10}")
        print("=" * 80)

        for contributor_file in contributor_files:
            total, tier4_count = count_tier4_contributors(contributor_file, tier4_engineers)

            if total > 0:
                external_count = total - tier4_count
                print(f"{contributor_file:<50} {total:<10} {tier4_count:<10} {external_count:<10}")

        print("=" * 80)
        logger.info("Successfully completed Tier4 engineer analysis")

    except Exception as e:
        logger.error(f"Fatal error in main execution: {e}")
        raise


if __name__ == "__main__":
    main()
