# Build plan

### Issue 1: Setup project structure and dependencies
- Scaffold the repository structure and initial files
- Setup .gitignore, README.md, .env.example with DATA_FILE env var (default to './data/items.json')
- Create empty main CLI entry (`ek_unique_cli.py`) with `if __name__ == '__main__'` stub
- Add minimal requirements/setup instructions

### Issue 2: Domain model and utilities
- Implement `Item` class with uuid, name, tags, created_at
- `utils.py` with UUID generator, name/tag validators
- Input validation functions
- Unit tests for domain and utils

### Issue 3: Persistence layer with JSON
- Implement `storage.py` for reading & writing item list atomically to JSON file
- Handle file missing, corrupt, or unreadable gracefully with fallback
- Methods: load_items(), save_items(items)
- Tests for storage reading, writing, corrupt file handling

### Issue 4: CLI command parsing and dispatch
- Implement `cli.py` with argparse for commands: create, search, list, help
- Wire commands to call domain + storage logic
- Display help and usage messages
- Tests for CLI argument parsing correctness

### Issue 5: Implement 'create' command
- Create item with generated or user-provided unique name & tags
- Validate uniqueness of name, fail if duplicate
- Save new item to storage
- Print created item details
- Error messages on duplicates or validation
- Tests for create command end-to-end and error cases

### Issue 6: Implement 'search' command
- Search items by name substring (case-insensitive) and/or tag
- Combine filters if both provided
- Print list of matching items or no items found message
- Tests covering search cases, no results, multiple filters

### Issue 7: Implement 'list' command
- List all stored items
- If empty, print friendly message
- Support optional output formatting (plain text)
- Tests for empty and populated listings

### Issue 8: Final polishing, error handling, tests, docs
- Enhance error handling (file write failures, invalid inputs)
- Add atomic file save locking or safe write pattern
- Add full test coverage for all modules
- Update README with usage instructions, command examples
- Add usage examples for creating, searching, and listing

