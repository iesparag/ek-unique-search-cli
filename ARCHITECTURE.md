# Architecture

### Components:

- CLI entry point (`ek_unique_cli.py`): Parses commands and args, dispatches to domain logic.
- Domain (`domain.py`): Defines `Item` entity and business logic for creating and searching unique items.
- Storage (`storage.py`): Handles reading/writing items to a JSON file with atomic writes and corruption handling.
- CLI parsing (`cli.py`): Uses argparse to handle `create`, `search`, `list`, and `help` commands.
- Utils (`utils.py`): Provides helper functions like UUID generation, input validation, and safe file write.
- Tests (`tests/`): Unit and integration tests for domain logic and storage correctness.

### Folder/layout:

```
ek_unique_search_cli/
├── ek_unique_cli.py          # main CLI executable
├── cli.py                    # CLI command parsing
├── domain.py                 # Item entity and business logic
├── storage.py                # JSON persistence layer
├── utils.py                  # helpers
├── data/                     # storage files (items.json)
├── tests/                    # pytest tests
├── README.md
├── .gitignore
└── .env.example              # env vars like DATA_FILE
```

### Data Flow:

1. User runs `ek_unique_cli.py <command>`
2. `cli.py` parses commands and options.
3. Domain logic creates or searches items, interacting with storage.
4. Storage reads/writes JSON data, ensures atomicity and safety.
5. CLI prints results or errors neatly.

### Key decisions:
- JSON file used for simple persistent store, easy human inspection, no DB dependency.
- UUID + unique name ensures unique items.
- Tags are optional, comma-separated, sanitized.
- CLI uses standard python `argparse` for minimal dependencies.
- Clear validation and helpful CLI messages.
- Tests to verify correctness and resilience.

