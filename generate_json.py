"""
Fetch contributor data from GitHub GraphQL API for Autoware repositories.

This script queries GitHub's GraphQL API for issues, pull requests, and discussions
across multiple Autoware repositories. It handles pagination and saves the results
as JSON files for later processing.
"""

from dataclasses import dataclass
from typing import List, Optional
import logging

from utils import (
    run_bash_script,
    write_json_file,
    ensure_directories_exist,
    GENERATED_JSON_DIR,
    logger,
    SubprocessError,
    DataProcessingError,
)


@dataclass
class RepositoryConfig:
    """Configuration for a repository and its contribution types."""
    name: str
    fetch_discussions: bool = False
    fetch_issues: bool = True
    fetch_prs: bool = True


# Repository configurations
REPOSITORIES = [
    RepositoryConfig("autoware", fetch_discussions=True, fetch_issues=True, fetch_prs=True),
    RepositoryConfig("autoware.universe", fetch_issues=True, fetch_prs=True),
    RepositoryConfig("autoware.core", fetch_issues=True, fetch_prs=True),
    RepositoryConfig("autoware_msgs", fetch_issues=True, fetch_prs=True),
    RepositoryConfig("autoware_launch", fetch_issues=True, fetch_prs=True),
    RepositoryConfig("autoware-documentation", fetch_issues=True, fetch_prs=True),
    RepositoryConfig("autoware_ai", fetch_issues=True, fetch_prs=False),
    RepositoryConfig("autoware_ai_perception", fetch_issues=True, fetch_prs=True),
    RepositoryConfig("autoware_ai_planning", fetch_issues=True, fetch_prs=True),
    RepositoryConfig("autoware_ai_messages", fetch_issues=True, fetch_prs=True),
    RepositoryConfig("autoware_ai_simulation", fetch_issues=True, fetch_prs=True),
    RepositoryConfig("autoware_ai_visualization", fetch_issues=True, fetch_prs=True),
    RepositoryConfig("autoware_ai_drivers", fetch_issues=True, fetch_prs=True),
    RepositoryConfig("autoware_ai_utilities", fetch_issues=True, fetch_prs=True),
    RepositoryConfig("autoware_ai_common", fetch_issues=True, fetch_prs=True),
]


# Script mappings for different contribution types
CONTRIBUTION_TYPE_SCRIPTS = {
    "discussions": {
        "cursor_script": "get_first_discussion.sh",
        "query_script": "query_discussions.sh",
        "api_field": "discussions",
    },
    "issues": {
        "cursor_script": "get_first_issue.sh",
        "query_script": "query_issues.sh",
        "api_field": "issues",
    },
    "pullRequests": {
        "cursor_script": "get_first_pr.sh",
        "query_script": "query_prs.sh",
        "api_field": "pullRequests",
    },
}


def get_first_cursor(
    cursor_script: str,
    api_field: str,
    repository: str
) -> Optional[str]:
    """
    Get the first cursor for pagination from the API.

    Args:
        cursor_script: Bash script to get the first cursor
        api_field: API field name (discussions, issues, or pullRequests)
        repository: Repository name

    Returns:
        First cursor string, or None if no data exists

    Raises:
        SubprocessError: If script execution fails
        DataProcessingError: If data extraction fails
    """
    try:
        loaded_json = run_bash_script(cursor_script, repository)

        edges = loaded_json.get("data", {}).get("repository", {}).get(api_field, {}).get("edges", [])

        if not edges:
            logger.info(f"No {api_field} found for repository {repository}")
            return None

        return edges[0].get("cursor")

    except (SubprocessError, DataProcessingError) as e:
        logger.error(f"Failed to get first cursor for {repository} {api_field}: {e}")
        raise


def fetch_all_edges(
    query_script: str,
    cursor_script: str,
    api_field: str,
    repository: str
) -> List[dict]:
    """
    Fetch all edges for a given contribution type and repository.

    This function handles pagination by repeatedly calling the API until
    all data has been retrieved.

    Args:
        query_script: Bash script to query data with cursor
        cursor_script: Bash script to get initial cursor
        api_field: API field name (discussions, issues, or pullRequests)
        repository: Repository name

    Returns:
        List of all edges from the API

    Raises:
        SubprocessError: If script execution fails
        DataProcessingError: If data extraction fails
    """
    logger.info(f"Fetching {api_field} for {repository}")

    # Get first cursor
    cursor = get_first_cursor(cursor_script, api_field, repository)
    if cursor is None:
        return []

    all_edges = []

    # Paginate through all results
    while True:
        try:
            loaded_json = run_bash_script(query_script, cursor, repository)
            edges = loaded_json.get("data", {}).get("repository", {}).get(api_field, {}).get("edges", [])

            if not edges:
                break

            all_edges.extend(edges)
            logger.info(f"Fetched {len(edges)} edges (total: {len(all_edges)})")

            # Get next cursor
            cursor = edges[-1].get("cursor")
            if not cursor:
                break

        except (SubprocessError, DataProcessingError) as e:
            logger.error(f"Error during pagination for {repository} {api_field}: {e}")
            raise

    logger.info(f"Completed fetching {len(all_edges)} total edges for {repository} {api_field}")
    return all_edges


def fetch_repository_data(repo_config: RepositoryConfig) -> None:
    """
    Fetch all configured contribution types for a repository.

    Args:
        repo_config: Repository configuration specifying what to fetch

    Raises:
        SubprocessError: If script execution fails
        DataProcessingError: If data extraction fails
    """
    repo_name = repo_config.name
    logger.info(f"Processing repository: {repo_name}")

    # Fetch discussions if configured
    if repo_config.fetch_discussions:
        try:
            scripts = CONTRIBUTION_TYPE_SCRIPTS["discussions"]
            edges = fetch_all_edges(
                scripts["query_script"],
                scripts["cursor_script"],
                scripts["api_field"],
                repo_name
            )
            output_file = GENERATED_JSON_DIR / f"{repo_name.replace('-', '_').replace('.', '_')}_discussions.json"
            write_json_file(edges, output_file)
        except Exception as e:
            logger.error(f"Failed to fetch discussions for {repo_name}: {e}")
            raise

    # Fetch issues if configured
    if repo_config.fetch_issues:
        try:
            scripts = CONTRIBUTION_TYPE_SCRIPTS["issues"]
            edges = fetch_all_edges(
                scripts["query_script"],
                scripts["cursor_script"],
                scripts["api_field"],
                repo_name
            )
            output_file = GENERATED_JSON_DIR / f"{repo_name.replace('-', '_').replace('.', '_')}_issues.json"
            write_json_file(edges, output_file)
        except Exception as e:
            logger.error(f"Failed to fetch issues for {repo_name}: {e}")
            raise

    # Fetch pull requests if configured
    if repo_config.fetch_prs:
        try:
            scripts = CONTRIBUTION_TYPE_SCRIPTS["pullRequests"]
            edges = fetch_all_edges(
                scripts["query_script"],
                scripts["cursor_script"],
                scripts["api_field"],
                repo_name
            )
            output_file = GENERATED_JSON_DIR / f"{repo_name.replace('-', '_').replace('.', '_')}_prs.json"
            write_json_file(edges, output_file)
        except Exception as e:
            logger.error(f"Failed to fetch pull requests for {repo_name}: {e}")
            raise


def main() -> None:
    """Main execution function."""
    try:
        # Ensure output directory exists
        ensure_directories_exist()

        # Process each repository
        for repo_config in REPOSITORIES:
            try:
                fetch_repository_data(repo_config)
            except Exception as e:
                logger.error(f"Failed to process repository {repo_config.name}: {e}")
                # Continue with next repository instead of failing completely
                continue

        logger.info("Successfully completed fetching data from all repositories")

    except Exception as e:
        logger.error(f"Fatal error in main execution: {e}")
        raise


if __name__ == "__main__":
    main()
