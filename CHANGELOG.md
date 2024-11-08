# 1.0.3 ()

### Features and enhancements

### Bug fixes

- **Package Handler** Fix: Minor label got mistaken as major in a specific case

# 1.0.2 (2024-11-07)

### Features and enhancements

- **Changelog** The changelog now differentiates between Arch changes and origin package changes
- **Web Scraper** Reduce default timeout from 15s to 5s after multiple test runs
- **Package Handler** Differentiate the regex extraction regarding if the source url is a .git url or not
- **Package Handler** Differentiate between different KDE package groups to selext the correct source control URL
- **Package Handler** Refactor: Moved the code to handle intermediate tags into a separate function for better overview
- **Package Handler** Refactor: Simplified the changelog handling
- **Package Handler** Refactor: Many enhancements and fixes to the intermediate tags handling
- **Entire codebase** Refactor: Formatted the entire codebase with the Black formatter
- **Package Handler** Added: Further information in the changelog json files regarding major/minor release
- **README** Updated README
- **Package Handler** Added: More docstrings for functions and type annotations for function parameters

### Bug fixes

- **Package Handler** Fix: Prevent TypeError when appending None to package_changelog by checking return value before concatenation
- **Package Handler** Fix: Corrected access to intermediate_tags, which was mistakenly accessed through the package object
- **Package Handler** Fix: Corrected order of intermediate tags to be checked with current tag
- **Package Handler** Fix: Rare cases of no package changelog could lead to a TypeError
- **Package Handler** Fix: Change default package architecture search string to English
- **Package Handler** Fix: Missing import for type annotation types
- **Package Handler** Removed: Wrong type annotation for logger

# 1.0.1 (2024-10-06)

### Bug fixes

- **Logger:** Revert: Remove StreamHandler duplicate check as it caused issues

# 1.0.0 (2024-10-05)

### Features and enhancements

- First release