# Test Suite for Autoware Analysis

This directory contains unit tests for the Autoware contributor analysis project.

## Running Tests

### Prerequisites

Install testing dependencies:
```bash
pip install pytest pytest-cov
```

### Run All Tests

```bash
# From the project root directory
python -m pytest tests/ -v

# Or using unittest
python -m unittest discover tests/
```

### Run Specific Test File

```bash
python -m pytest tests/test_utils.py -v
```

### Run with Coverage Report

```bash
# Generate coverage report
python -m pytest tests/ --cov=utils --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Run Specific Test Class or Method

```bash
# Run specific test class
python -m pytest tests/test_utils.py::TestFileOperations -v

# Run specific test method
python -m pytest tests/test_utils.py::TestFileOperations::test_write_and_read_json_file -v
```

## Test Structure

### test_utils.py

Tests for the shared utilities module:

- **TestFileOperations**: JSON and text file I/O
- **TestDateTimeOperations**: Date parsing and range generation
- **TestContributorExtraction**: Extracting contributors from GraphQL edges
- **TestContributorAggregation**: Merging and counting contributors
- **TestUtilityFunctions**: CSV formatting and other utilities
- **TestErrorHandling**: Exception handling

## Test Coverage Goals

- **Target**: >90% code coverage
- **Current**: ~95% for utils module
- **Focus areas**:
  - All public functions
  - Error handling paths
  - Edge cases and boundary conditions

## Writing New Tests

Follow these guidelines when adding new tests:

### Test Naming Convention

```python
class TestFeatureName(unittest.TestCase):
    """Test FeatureName functionality."""

    def test_specific_behavior(self):
        """Test that specific behavior works correctly."""
        # Arrange
        input_data = "test"

        # Act
        result = function_under_test(input_data)

        # Assert
        self.assertEqual(result, expected_value)
```

### AAA Pattern

Use the Arrange-Act-Assert pattern:
1. **Arrange**: Set up test data and preconditions
2. **Act**: Call the function being tested
3. **Assert**: Verify the result

### Testing Best Practices

1. **One assertion per test**: Keep tests focused
2. **Test edge cases**: Empty inputs, None values, boundary conditions
3. **Use descriptive names**: Test names should describe what is being tested
4. **Mock external dependencies**: Use unittest.mock for subprocess calls, file I/O
5. **Clean up**: Use setUp/tearDown for test fixtures
6. **Independent tests**: Tests should not depend on each other

### Example Test

```python
def test_extract_author_login_valid(self):
    """Test extracting author login from valid node."""
    # Arrange
    node = {"author": {"login": "testuser"}}

    # Act
    result = extract_author_login(node)

    # Assert
    self.assertEqual(result, "testuser")
```

## Mocking External Dependencies

Use mocking for operations that interact with external systems:

```python
from unittest.mock import patch, MagicMock

@patch('subprocess.run')
def test_subprocess_call(self, mock_run):
    """Test subprocess execution."""
    # Arrange
    mock_run.return_value = MagicMock(returncode=0)

    # Act
    result = run_bash_script("test.sh")

    # Assert
    mock_run.assert_called_once()
```

## Testing Philosophy

### What to Test

- **Public interfaces**: All public functions and methods
- **Error conditions**: Invalid inputs, missing files, network errors
- **Edge cases**: Empty data, boundary values, special characters
- **Business logic**: Core algorithms and data transformations
- **Integration points**: How modules interact

### What Not to Test

- **Private functions**: Only test through public interfaces
- **Third-party libraries**: Assume they work correctly
- **Trivial code**: Simple getters/setters, pass-through functions
- **Implementation details**: Test behavior, not implementation

## Continuous Testing

For development, use pytest watch mode:

```bash
pip install pytest-watch
ptw tests/ -- -v
```

This will automatically re-run tests when files change.

## Test Data

Test data should be:
- **Minimal**: Use smallest data that demonstrates the behavior
- **Realistic**: Representative of actual data
- **Self-contained**: Tests should not depend on external files

## Troubleshooting

### Tests Fail with Import Errors

Make sure you're running tests from the project root:
```bash
cd /path/to/autoware_analysis
python -m pytest tests/
```

### Tests Fail with File Not Found

Check that temporary directories are being cleaned up properly in tearDown methods.

### Slow Tests

If tests are slow:
1. Use mocks for I/O operations
2. Reduce test data size
3. Parallelize tests: `pytest -n auto`

## Future Test Coverage

Areas to add tests for:

1. **Integration tests**: Test full pipeline from JSON to output
2. **Performance tests**: Benchmark critical operations
3. **Edge case tests**: Unicode characters, very large datasets
4. **Script tests**: Test main() functions with mocked dependencies
5. **Error recovery**: Test graceful degradation

## Contributing

When contributing code:
1. Write tests for new features
2. Update existing tests if behavior changes
3. Maintain >90% coverage
4. Run full test suite before submitting PR
5. Document complex test scenarios

## Test Metrics

Current test metrics:
- **Total tests**: 15+
- **Coverage**: ~95% (utils module)
- **Execution time**: <2 seconds
- **Pass rate**: 100%

Target metrics:
- **Total tests**: 50+
- **Coverage**: >90% (all modules)
- **Execution time**: <5 seconds
- **Pass rate**: 100%
