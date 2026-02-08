# Contributing to PowerboatList

Thank you for your interest in contributing to PowerboatList! This document provides guidelines for contributing to the project.

## Ways to Contribute

### 1. Report Missing Boats
Found a boat model that matches the criteria (13'6"-13'11", 40+ HP) but isn't in the results?

- Open an issue with the boat details
- Include: Make, Model, Length, Max HP, and a source URL
- We'll verify and add it to the manufacturer list

### 2. Add Manufacturers
Know of manufacturers we haven't included?

- Fork the repository
- Add manufacturer to `config_template.py` in the `MANUFACTURERS` list
- Submit a pull request
- Include information about the manufacturer

### 3. Improve Documentation
Help make the docs better:

- Fix typos or unclear instructions
- Add examples or use cases
- Improve setup guides
- Translate documentation

### 4. Code Improvements
Enhance the codebase:

- Bug fixes
- Performance optimizations
- New features
- Test coverage improvements

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repo on GitHub, then:
git clone https://github.com/YOUR_USERNAME/PowerboatList.git
cd PowerboatList
```

### 2. Create Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your API keys for testing
```

### 4. Run Tests

```bash
# Run all tests
python -m unittest discover

# Run specific test file
python -m unittest test_search_boats.py -v

# Check code coverage
pytest --cov=search_boats --cov-report=html
```

## Coding Standards

### Python Style

- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Maximum line length: 100 characters
- Use descriptive variable names

### Code Quality Tools

We use these tools to maintain code quality:

```bash
# Format code with black
black search_boats.py

# Sort imports with isort
isort search_boats.py

# Check types with mypy
mypy search_boats.py

# Lint with flake8
flake8 search_boats.py
```

### Documentation

- Add docstrings to all functions
- Include type hints
- Provide examples for complex functions
- Update README.md for new features

Example:
```python
def filter_boats(boats: List[Dict]) -> List[Dict]:
    """
    Filters boats based on length and HP criteria.

    Args:
        boats: List of boat dictionaries with specs

    Returns:
        List of boats matching criteria (13'6"-13'11", 40+ HP)

    Example:
        >>> boats = [{'make': 'Test', 'model': 'A', 'length_ft': 13.5, 'max_hp': 40}]
        >>> filtered = filter_boats(boats)
        >>> len(filtered)
        1
    """
```

## Testing Guidelines

### Writing Tests

- Write tests for all new functions
- Test happy paths and edge cases
- Use mocking for external API calls
- Aim for >80% code coverage

### Test Structure

```python
class TestFeature(unittest.TestCase):
    """Test the new feature"""

    def setUp(self):
        """Set up test fixtures"""
        pass

    def test_normal_case(self):
        """Test typical usage"""
        pass

    def test_edge_case(self):
        """Test boundary conditions"""
        pass

    def test_error_handling(self):
        """Test error scenarios"""
        pass
```

## Pull Request Process

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Your Changes

- Write clear, focused commits
- Follow the coding standards
- Add tests for new code
- Update documentation

### 3. Commit Messages

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:
```
feat(search): add retry logic for failed API calls

Implements exponential backoff for Brave Search and Claude API
failures. Retries up to 3 times before giving up.

Closes #42
```

```
fix(filter): handle missing HP field gracefully

Previously crashed when max_hp was None. Now treats missing
HP as 0 and filters out the boat.
```

### 4. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:

- Clear title and description
- Reference related issues
- Include test results
- Add screenshots if UI changes

### 5. Code Review

- Address reviewer feedback
- Keep discussions constructive
- Update PR based on suggestions
- Ensure CI passes

## Adding Manufacturers

To add a new manufacturer:

1. Research the manufacturer's boat lineup
2. Verify they make boats in the 13'6"-13'11" range
3. Add to `MANUFACTURERS` list in `config_template.py`:

```python
MANUFACTURERS = [
    # ... existing manufacturers ...
    "New Manufacturer Name",
]
```

4. Test that the search works:

```python
# In search_boats.py, temporarily change:
manufacturers = ["New Manufacturer Name"]
# Run the script and verify results
```

5. Submit PR with:
   - Manufacturer added to list
   - Test results showing successful search
   - Any boats found in the target range

## Reporting Issues

### Bug Reports

Include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs
- API versions used

### Feature Requests

Include:
- Clear description of the feature
- Use cases and benefits
- Potential implementation approach
- Willingness to contribute code

## Community Guidelines

- Be respectful and constructive
- Help others learn and grow
- Credit others' work
- Follow the Code of Conduct
- Ask questions when unclear

## Questions?

- Open an issue for general questions
- Tag issues with `question` label
- Check existing issues first
- Be specific about your question

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

Thank you for contributing to PowerboatList! 🚤
