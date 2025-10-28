"""
Fetch Tier4 organization member list from GitHub.

This script queries GitHub's GraphQL API to retrieve the list of members
from the Tier4 organization team.
"""

from typing import List, Optional

from utils import (
    run_bash_script,
    write_text_file,
    ensure_directories_exist,
    TIER4_ENGINEERS_DIR,
    logger,
    SubprocessError,
    DataProcessingError,
)


def get_first_cursor(cursor_script: str) -> Optional[str]:
    """
    Get the first cursor for pagination from the Tier4 team API.

    Args:
        cursor_script: Bash script to get the first cursor

    Returns:
        First cursor string, or None if no data exists

    Raises:
        SubprocessError: If script execution fails
        DataProcessingError: If data extraction fails
    """
    try:
        loaded_json = run_bash_script(cursor_script)

        members = loaded_json.get("data", {}).get("organization", {}).get("team", {}).get("members", {})
        edges = members.get("edges", [])

        if not edges:
            logger.info("No Tier4 team members found")
            return None

        logger.info(f"Found initial members data: {len(edges)} members")
        return edges[0].get("cursor")

    except (SubprocessError, DataProcessingError) as e:
        logger.error(f"Failed to get first cursor for Tier4 engineers: {e}")
        raise


def fetch_all_members(query_script: str, first_cursor: str) -> List[str]:
    """
    Fetch all Tier4 team member logins.

    This function handles pagination by repeatedly calling the API until
    all members have been retrieved.

    Args:
        query_script: Bash script to query members with cursor
        first_cursor: Initial cursor for pagination

    Returns:
        List of all member login names

    Raises:
        SubprocessError: If script execution fails
        DataProcessingError: If data extraction fails
    """
    if first_cursor is None:
        return []

    all_members: List[str] = []
    cursor = first_cursor

    logger.info("Fetching Tier4 team members...")

    # Paginate through all results
    while True:
        try:
            loaded_json = run_bash_script(query_script, cursor)

            members_data = loaded_json.get("data", {}).get("organization", {}).get("team", {}).get("members", {})
            nodes = members_data.get("nodes", [])

            if not nodes:
                break

            # Extract login names from nodes
            for node in nodes:
                if "login" in node and node["login"]:
                    all_members.append(node["login"])

            logger.info(f"Fetched {len(nodes)} members (total: {len(all_members)})")

            # Get next cursor
            edges = members_data.get("edges", [])
            if not edges:
                break

            cursor = edges[-1].get("cursor")
            if not cursor:
                break

        except (SubprocessError, DataProcessingError) as e:
            logger.error(f"Error during pagination for Tier4 engineers: {e}")
            raise

    logger.info(f"Completed fetching {len(all_members)} total Tier4 team members")
    return all_members


def main() -> None:
    """Main execution function."""
    try:
        # Ensure output directory exists
        ensure_directories_exist()

        # Scripts for fetching Tier4 engineers
        cursor_script = "get_first_tier4_engineer.sh"
        query_script = "get_tier4_engineers.sh"

        # Get first cursor
        logger.info("Getting initial cursor...")
        cursor = get_first_cursor(cursor_script)

        if cursor is None:
            logger.warning("No Tier4 team members found, creating empty file")
            tier4_engineers = []
        else:
            # Fetch all members
            tier4_engineers = fetch_all_members(query_script, cursor)

        # Write results to file
        output_file = TIER4_ENGINEERS_DIR / "tier4_engineers.txt"
        write_text_file(tier4_engineers, output_file)

        logger.info(f"Successfully fetched {len(tier4_engineers)} Tier4 engineers")

    except Exception as e:
        logger.error(f"Fatal error in main execution: {e}")
        raise


if __name__ == "__main__":
    main()
