# Autoware Contributors Analysis

This repository contains scripts to analyze contributor data from Autoware Foundation GitHub repositories.

## Overview

The analysis covers:
- **Contributors**: Unique users contributing through PRs, Issues, and Discussions
- **Stars**: Unique stargazers across all Autoware repositories
- **TIER IV Impact**: Breakdown of internal vs external contributions

## Prerequisites

- Python 3.9+
- GitHub CLI (`gh`) installed and authenticated
- For development: `pip install -r requirements.txt`

## Quick Start

Run the complete analysis pipeline:

```bash
# 1. Fetch raw data from GitHub GraphQL API
python3 generate_json.py

# 2. Process data and count contributors
python3 count_contributors.py

# 3. Generate contributor history (cumulative over time)
python3 get_contributor_history.py

# 4. Fetch TIER IV engineer list
python3 get_tier4_engineers.py

# 5. Count contributors excluding TIER IV engineers
python3 remove_tier4_engineers.py

# 6. Fetch stargazer data (all repositories, deduplicated)
#    WARNING: This takes a long time (~10-30 minutes)
python3 get_stars.py

# 7. Format stargazer data into CSV
python3 reformat_stargazers.py
```

## Check Results

```bash
# Count contributors
wc -l contributor_names/autoware_contributors.txt
wc -l contributor_names/autoware_code_contributors.txt
wc -l contributor_names/autoware_community_contributors.txt

# View star count
tail stars/counted_stars.csv
```

## Key Features

### Unique Star Counting (Multi-Repository Deduplication)

The star counting process (`get_stars.py`) has been enhanced to provide an accurate count of unique users who have starred any Autoware repository:

#### How it Works
1. **Fetch from ALL repositories**: Queries 6 repositories (autoware, autoware_universe, autoware_core, autoware_msgs, autoware_launch, autoware-documentation)
2. **Deduplicate by user**: Each user is counted only once across all repositories
3. **Use earliest star date**: When a user has starred multiple repos, their earliest star date is used
4. **Track individual repos**: Saves per-repository data in `stars/stargazers_<repo>.json` for analysis
5. **Generate aggregate data**: Final deduplicated data in `stars/stargazers.json`

#### Why This Matters
The current star count (10,499) represents **unique individuals** who have engaged with the Autoware ecosystem, not just stars on a single repository. This provides a more accurate measure of the project's reach and community size.

**Example**: If user `johndoe` starred `autoware` on 2022-01-15 and `autoware_universe` on 2022-03-20, they are counted once with the date 2022-01-15.

**Note**: Running `get_stars.py` takes 10-30 minutes as it must query the stargazers list from 6 separate repositories via GitHub GraphQL API.

### Output Files

```
generated_json/          # Raw GitHub GraphQL API responses
contributor_names/       # Lists of contributor usernames
contributor_history/     # Time-series contributor data
tier4_engineers/         # TIER IV organization members
stars/
  ├── stargazers_*.json  # Individual repo stargazer data
  ├── stargazers.json    # Deduplicated stargazers (all repos)
  └── counted_stars.csv  # Daily star counts with cumulative totals
```

## Analysis Report

View the comprehensive analysis report:
- `ANALYSIS_REPORT.md` - Full report with visualizations

## Documentation

- `CLAUDE.md` - Project guide and architecture
- `QUICK_START.md` - Quick reference for common operations
- `REFACTORING_NOTES.md` - Details on code improvements
- `tests/README.md` - Testing documentation

## Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=utils --cov-report=html
```

## Analyzed Repositories

**Current**:
- autoware
- autoware_universe
- autoware_core
- autoware_msgs
- autoware_launch
- autoware-documentation

**Legacy** (Autoware.AI):
- autoware_ai and related repositories

## Notes

- **Star data represents unique users**: The 10,499 star count represents deduplicated users across all 6 repositories, providing an accurate measure of unique community members who have starred any Autoware repository
- **Star data fetching takes time**: Fetching takes 10-30 minutes as it must query stargazers from 6 repositories and merge/deduplicate the results
- All data is fetched via GitHub GraphQL API using `gh` CLI
- Date filtering: Analysis starts from 2022-01-01 for current repos
- Owner is hardcoded to "autowarefoundation"

## Contributing

See `MIGRATION_CHECKLIST.md` for details on working with the refactored codebase.

## License

[License information to be added]
