"""
Fetch stargazer data from GitHub repositories.

This script queries GitHub's GraphQL API to retrieve stargazer information
including when each star was added. It fetches stars from all Autoware
repositories and deduplicates by user to count unique stargazers.
"""

from typing import List, Optional, Tuple, Dict
from datetime import datetime

from utils import (
    run_bash_script,
    write_json_file,
    ensure_directories_exist,
    parse_datetime,
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


def deduplicate_stargazers(all_stargazers: Dict[str, List[dict]]) -> List[dict]:
    """
    Deduplicate stargazers across repositories by user.

    For each unique user, keeps only their earliest star timestamp
    across all repositories.

    Args:
        all_stargazers: Dictionary mapping repository names to lists of stargazer edges

    Returns:
        List of unique stargazer edges with earliest timestamp per user

    Raises:
        DataProcessingError: If data processing fails
    """
    try:
        # Dictionary to track earliest star per user
        # Key: user login, Value: (starredAt datetime, edge dict)
        unique_users: Dict[str, Tuple[datetime, dict]] = {}

        for repo_name, edges in all_stargazers.items():
            logger.info(f"Processing {len(edges)} stargazers from {repo_name}")

            for edge in edges:
                node = edge.get("node", {})
                login = node.get("login")
                starred_at_str = edge.get("starredAt")

                if not login or not starred_at_str:
                    logger.warning(f"Stargazer edge missing login or starredAt in {repo_name}")
                    continue

                try:
                    starred_at = parse_datetime(starred_at_str)

                    # If user not seen before, or this star is earlier, update
                    if login not in unique_users or starred_at < unique_users[login][0]:
                        unique_users[login] = (starred_at, edge)

                except DataProcessingError:
                    logger.warning(f"Failed to parse starredAt for user {login}: {starred_at_str}")
                    continue

        # Extract just the edges (without datetime)
        unique_edges = [edge for _, edge in unique_users.values()]

        logger.info(f"Found {len(unique_edges)} unique stargazers across all repositories")
        return unique_edges

    except Exception as e:
        raise DataProcessingError(f"Failed to deduplicate stargazers: {e}")


def main() -> None:
    """Main execution function."""
    try:
        # Ensure output directory exists
        ensure_directories_exist()

        # Configuration
        cursor_script = "get_first_star.sh"
        query_script = "query_stars.sh"

        # List of repositories to fetch stars from
        repositories = [
            "autoware",
            "autoware_universe",
            "autoware_core",
            "autoware_msgs",
            "autoware_launch",
            "autoware-documentation",
        ]

        # Fetch stargazers from all repositories
        all_stargazers: Dict[str, List[dict]] = {}

        for repository in repositories:
            logger.info(f"\n{'='*60}")
            logger.info(f"Fetching stargazers for {repository}")
            logger.info(f"{'='*60}")

            try:
                stargazers = fetch_all_stargazers(query_script, cursor_script, repository)
                all_stargazers[repository] = stargazers

                # Write individual repository results
                output_file = STARS_DIR / f"stargazers_{repository}.json"
                write_json_file(stargazers, output_file)
                logger.info(f"Saved {len(stargazers)} stargazers for {repository}")

            except Exception as e:
                logger.error(f"Failed to fetch stargazers for {repository}: {e}")
                # Continue with other repositories
                all_stargazers[repository] = []

        # Deduplicate stargazers across all repositories
        logger.info(f"\n{'='*60}")
        logger.info("Deduplicating stargazers across all repositories")
        logger.info(f"{'='*60}")

        unique_stargazers = deduplicate_stargazers(all_stargazers)

        # Write deduplicated results
        output_file = STARS_DIR / "stargazers.json"
        write_json_file(unique_stargazers, output_file)

        # Summary
        total_stars = sum(len(edges) for edges in all_stargazers.values())
        logger.info(f"\n{'='*60}")
        logger.info(f"Summary:")
        logger.info(f"  Total stars across all repos: {total_stars}")
        logger.info(f"  Unique stargazers (users): {len(unique_stargazers)}")
        logger.info(f"  Deduplication rate: {(1 - len(unique_stargazers)/total_stars)*100:.1f}%")
        logger.info(f"{'='*60}")

    except Exception as e:
        logger.error(f"Fatal error in main execution: {e}")
        raise


if __name__ == "__main__":
    main()
