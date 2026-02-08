# Release Guide for PowerboatList

This document describes the release process for PowerboatList.

## Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for backwards-compatible functionality additions
- PATCH version for backwards-compatible bug fixes

## Pre-Release Checklist

Before creating a new release:

### 1. Code Quality
- [ ] All tests pass locally
- [ ] CI/CD pipeline is green
- [ ] Code coverage meets target (>80%)
- [ ] No linting errors
- [ ] Type checking passes

### 2. Documentation
- [ ] README.md is up to date
- [ ] CHANGELOG.md has entry for this version
- [ ] API keys setup guide is accurate
- [ ] Examples reflect current functionality
- [ ] All links are working

### 3. Version Updates
- [ ] Update version in `__version__.py`
- [ ] Update version in `setup.py` (should read from __version__.py)
- [ ] Update CHANGELOG.md with release date
- [ ] Update PROJECT_STATUS.md if needed

### 4. Testing
- [ ] Tested with fresh API keys
- [ ] Tested in Google Colab
- [ ] Tested local installation
- [ ] Tested on multiple platforms (if possible)
- [ ] Verified CSV output
- [ ] Verified Google Sheets output

## Release Process

### 1. Prepare the Release

```bash
# Ensure you're on main branch
git checkout main
git pull origin main

# Update version
vim __version__.py  # Update version number

# Update changelog
vim CHANGELOG.md    # Add release date, move items from Unreleased

# Commit version bump
git add __version__.py CHANGELOG.md
git commit -m "chore: bump version to X.Y.Z"
git push origin main
```

### 2. Create Git Tag

```bash
# Create annotated tag
git tag -a vX.Y.Z -m "Release version X.Y.Z"

# Push tag to remote
git push origin vX.Y.Z
```

### 3. Create GitHub Release

1. Go to GitHub repository
2. Click "Releases" → "Create a new release"
3. Select the tag you just created
4. Title: "PowerboatList vX.Y.Z"
5. Description: Copy from CHANGELOG.md
6. Attach any release artifacts (optional)
7. Check "Set as latest release" (for stable releases)
8. Click "Publish release"

### 4. PyPI Release (Optional)

If publishing to PyPI:

```bash
# Build distribution
python setup.py sdist bdist_wheel

# Upload to PyPI (requires PyPI account and twine)
python -m twine upload dist/*
```

### 5. Post-Release

- [ ] Verify release appears on GitHub
- [ ] Test installation from GitHub:
  ```bash
  pip install git+https://github.com/YOUR_USERNAME/PowerboatList.git@vX.Y.Z
  ```
- [ ] Announce release (if applicable)
- [ ] Update PROJECT_STATUS.md with new version
- [ ] Start new "Unreleased" section in CHANGELOG.md

## Release Types

### Major Release (X.0.0)
- Breaking changes to API or configuration
- Significant architectural changes
- Requires migration guide
- Extra testing required

### Minor Release (X.Y.0)
- New features added
- Backwards compatible
- May include deprecation warnings
- Standard testing required

### Patch Release (X.Y.Z)
- Bug fixes only
- No new features
- Backwards compatible
- Focused testing on fixed issues

## Hotfix Process

For critical bugs in production:

1. Create hotfix branch from main:
   ```bash
   git checkout -b hotfix/X.Y.Z main
   ```

2. Fix the bug and test thoroughly

3. Update version (patch bump)

4. Commit and merge to main:
   ```bash
   git checkout main
   git merge --no-ff hotfix/X.Y.Z
   ```

5. Tag and release as normal

6. Delete hotfix branch:
   ```bash
   git branch -d hotfix/X.Y.Z
   ```

## Release Schedule

PowerboatList follows a flexible release schedule:

- **Major versions**: As needed for breaking changes
- **Minor versions**: Monthly or when significant features accumulate
- **Patch versions**: As needed for bug fixes

## Communication

### Release Notes Template

```markdown
# PowerboatList vX.Y.Z

Released: YYYY-MM-DD

## What's New

- Feature 1
- Feature 2
- Bug fix 1

## Breaking Changes

- Change 1 (Major releases only)

## Upgrade Guide

Instructions for upgrading from previous version.

## Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete details.

## Installation

```bash
pip install git+https://github.com/YOUR_USERNAME/PowerboatList.git@vX.Y.Z
```

## Contributors

Thanks to everyone who contributed to this release!
```

## Rollback Procedure

If a release has critical issues:

1. Identify the problem
2. Document the issue
3. Create hotfix or revert
4. Release patch version
5. Update users via GitHub issues

## Version Support

- **Current version**: Full support
- **Previous minor**: Security fixes only
- **Older versions**: Not supported

## Questions?

Open an issue or contact the maintainers.

---

Last Updated: 2026-01-09
