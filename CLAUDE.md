# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This repository analyzes contributor data from Autoware Foundation GitHub repositories. It fetches data via GitHub GraphQL API and processes it to count contributors across various Autoware repositories (autoware, autoware.universe, autoware.core, autoware_common, autoware_msgs, autoware_launch, autoware-documentation, and legacy autoware_ai_* repositories).

## Prerequisites

- Python 3.9+ (required for type hints and modern features)
- GitHub CLI (`gh`) installed and authenticated
- Write access to create directories: `generated_json/`, `contributor_names/`, `contributor_history/`, `tier4_engineers/`, and `stars/`

### Development Prerequisites (Optional)

For development and testing:
```bash
pip install -r requirements.txt
```

This installs pytest, code quality tools, and other development utilities.

## Running the Analysis Pipeline

Execute these scripts in sequence to perform a complete analysis:

```bash
# 1. Fetch raw data from GitHub GraphQL API
python3 generate_json.py

# 2. Process data and count contributors
python3 count_contributors.py

# 3. Generate contributor history (cumulative over time)
python3 get_contributor_history.py

# 4. Fetch Tier4 engineer list from GitHub organization
python3 get_tier4_engineers.py

# 5. Count contributors excluding Tier4 engineers
python3 remove_tier4_engineers.py

# 6. Fetch stargazer data
python3 get_stars.py

# 7. Format stargazer data into CSV
python3 reformat_stargazers.py
```

To count the final results:
```bash
wc -l contributor_names/autoware_contributors.txt
wc -l contributor_names/autoware_code_contributors.txt
wc -l contributor_names/autoware_community_contributors.txt
```

## Architecture

### Data Flow

The system follows a multi-stage pipeline:

1. **Data Fetching** (`generate_json.py`): Uses bash scripts to query GitHub GraphQL API
   - Shell scripts (`query_*.sh`) handle pagination with cursors
   - `get_first_*.sh` scripts get initial cursor positions
   - Results stored in `generated_json/` directory as JSON files

2. **Contributor Extraction** (`count_contributors.py`): Parses JSON files
   - Extracts author logins from issues, PRs, discussions, and their comments
   - Applies date filtering (2022-01-01 cutoff for AI repositories)
   - Categorizes into code contributors (PRs) vs community contributors (issues/discussions)
   - Outputs to `contributor_names/` directory as text files

3. **Historical Analysis** (`get_contributor_history.py`): Tracks growth over time
   - Creates daily contributor counts since 2022-01-01
   - Tracks first contribution date per user
   - Generates cumulative CSV data in `contributor_history/`

4. **Tier4 Filtering** (`get_tier4_engineers.py`, `remove_tier4_engineers.py`):
   - Fetches Tier4 organization member list via GraphQL
   - Counts how many contributors are Tier4 employees vs external

5. **Stargazer Analysis** (`get_stars.py`, `reformat_stargazers.py`):
   - Fetches repository star data with timestamps
   - Converts to daily star count CSV

### Repository Coverage

The scripts analyze these Autoware Foundation repositories:
- **Current**: autoware, autoware.universe, autoware.core, autoware_common, autoware_msgs, autoware_launch, autoware-documentation
- **Legacy**: autoware_ai, autoware_ai_perception, autoware_ai_planning, autoware_ai_messages, autoware_ai_simulation, autoware_ai_visualization, autoware_ai_drivers, autoware_ai_utilities, autoware_ai_common

### Key Data Structures

- **Contributor Types**: Discussions, Issues, Pull Requests
- **Contributor Categories**:
  - `code_contributors`: Users who submitted PRs
  - `community_contributors`: Users who created/commented on issues or discussions
  - `autoware_contributors`: Union of both categories

### Output Files

- `generated_json/*.json`: Raw GraphQL response data
- `contributor_names/*.txt`: Sorted unique contributor usernames
- `contributor_history/*.txt` and `*.csv`: Daily contributor counts with cumulative totals
- `tier4_engineers/tier4_engineers.txt`: List of Tier4 organization members
- `stars/stargazers.json`: Raw stargazer data
- `stars/counted_stars.csv`: Daily star counts
- `tmp.txt`: Temporary file for GraphQL responses (not committed)

## GitHub GraphQL API Usage

All shell scripts use `gh api graphql` with pagination:
- Query 100 items per page using cursor-based pagination
- Extract cursors from responses to fetch next page
- Continue until no more results
- Owner is hardcoded to "autowarefoundation"

## Code Structure (Refactored)

The codebase has been refactored for improved maintainability, testability, and performance:

### Core Modules

- **`utils.py`**: Shared utilities module containing:
  - File I/O operations (JSON, text)
  - Subprocess execution with error handling
  - Date/time utilities
  - Contributor extraction and aggregation functions
  - Custom exception classes

### Best Practices Implemented

- **Type hints**: All functions have comprehensive type annotations
- **Error handling**: Proper exception handling with custom exception classes
- **Logging**: Structured logging instead of print statements
- **Documentation**: Comprehensive docstrings following Google style
- **Testing**: Unit tests with >90% coverage in `tests/` directory
- **PEP 8**: Follows Python style guidelines
- **Configuration-driven**: Uses dataclasses and configuration objects

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=utils --cov-report=html

# Run specific test file
python -m pytest tests/test_utils.py -v
```

See `tests/README.md` for detailed testing documentation.

## Modifying the Analysis

### Adding a New Repository

1. Edit `generate_json.py` and add to `REPOSITORIES` list:
```python
REPOSITORIES = [
    # ... existing repositories
    RepositoryConfig("new_repo_name", fetch_discussions=False, fetch_issues=True, fetch_prs=True),
]
```

2. Edit `count_contributors.py` and add to `sources` list:
```python
sources = [
    # ... existing sources
    ContributorSource("new_repo_name_issues.json", "new_repo_name_issues.txt"),
    ContributorSource("new_repo_name_prs.json", "new_repo_name_prs.txt"),
]
```

3. Edit `get_contributor_history.py` and add to relevant source lists:
```python
community_sources = [
    # ... existing sources
    "new_repo_name_issues.json",
]

code_sources = [
    # ... existing sources
    "new_repo_name_prs.json",
]
```

### Changing Date Filters

Modify `START_DATE` in `utils.py`:
```python
START_DATE = datetime(2022, 1, 1)  # Change this date
```

This affects all scripts that use date filtering.

### Customizing Output

Output directories are defined in `utils.py`:
```python
GENERATED_JSON_DIR = Path("generated_json")
CONTRIBUTOR_NAMES_DIR = Path("contributor_names")
CONTRIBUTOR_HISTORY_DIR = Path("contributor_history")
TIER4_ENGINEERS_DIR = Path("tier4_engineers")
STARS_DIR = Path("stars")
```

## Refactoring Details

For comprehensive information about the refactoring changes, see `REFACTORING_NOTES.md`:
- Code quality improvements
- Performance optimizations
- Architecture changes
- Migration guide
- Future enhancement ideas
