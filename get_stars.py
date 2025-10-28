"""
Fetch stargazer data from GitHub repositories.

This script queries GitHub's GraphQL API to retrieve stargazer information
including when each star was added.
"""

from typing import List, Optional, Tuple

from utils import (
    run_bash_script,
    write_json_file,
    ensure_directories_exist,
    STARS_DIR,
    logger,
    SubprocessError,
    DataProcessingError,
)


def get_first_cursor_and_edges(
    cursor_script: str,
    repository: str
) -> Tuple[Optional[str], List[dict]]:
    """
    Get the first cursor and initial edges for stargazers.

    Args:
        cursor_script: Bash script to get the first cursor
        repository: Repository name

    Returns:
        Tuple of (first_cursor, initial_edges)

    Raises:
        SubprocessError: If script execution fails
        DataProcessingError: If data extraction fails
    """
    try:
        loaded_json = run_bash_script(cursor_script, repository)

        stargazers = loaded_json.get("data", {}).get("repository", {}).get("stargazers", {})
        edges = stargazers.get("edges", [])

        if not edges:
            logger.info(f"No stargazers found for repository {repository}")
            return None, []

        cursor = edges[0].get("cursor")
        logger.info(f"Found {len(edges)} initial stargazers for {repository}")

        return cursor, edges

    except (SubprocessError, DataProcessingError) as e:
        logger.error(f"Failed to get first cursor for stargazers in {repository}: {e}")
        raise


def fetch_all_stargazers(
    query_script: str,
    cursor_script: str,
    repository: str
) -> List[dict]:
    """
    Fetch all stargazers for a repository.

    This function handles pagination by repeatedly calling the API until
    all stargazers have been retrieved.

    Args:
        query_script: Bash script to query stargazers with cursor
        cursor_script: Bash script to get initial cursor
        repository: Repository name

    Returns:
        List of all stargazer edges

    Raises:
        SubprocessError: If script execution fails
        DataProcessingError: If data extraction fails
    """
    logger.info(f"Fetching stargazers for {repository}")

    # Get first cursor and initial edges
    cursor, all_edges = get_first_cursor_and_edges(cursor_script, repository)

    if cursor is None:
        return []

    # Paginate through remaining results
    while True:
        try:
            loaded_json = run_bash_script(query_script, cursor, repository)

            stargazers = loaded_json.get("data", {}).get("repository", {}).get("stargazers", {})
            edges = stargazers.get("edges", [])

            if not edges:
                break

            all_edges.extend(edges)
            logger.info(f"Fetched {len(edges)} stargazers (total: {len(all_edges)})")

            # Get next cursor
            cursor = edges[-1].get("cursor")
            if not cursor:
                break

        except (SubprocessError, DataProcessingError) as e:
            logger.error(f"Error during pagination for {repository} stargazers: {e}")
            raise

    logger.info(f"Completed fetching {len(all_edges)} total stargazers for {repository}")
    return all_edges


def main() -> None:
    """Main execution function."""
    try:
        # Ensure output directory exists
        ensure_directories_exist()

        # Configuration
        cursor_script = "get_first_star.sh"
        query_script = "query_stars.sh"
        repository = "autoware"

        # Fetch stargazers
        stargazers = fetch_all_stargazers(query_script, cursor_script, repository)

        # Write results to file
        output_file = STARS_DIR / "stargazers.json"
        write_json_file(stargazers, output_file)

        logger.info(f"Successfully fetched {len(stargazers)} stargazers for {repository}")

    except Exception as e:
        logger.error(f"Fatal error in main execution: {e}")
        raise


if __name__ == "__main__":
    main()
