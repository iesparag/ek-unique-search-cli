# ek-unique-search-cli

A command-line tool for generating unique items, tagging them, and searching/persisting them locally. Useful for anyone needing easy unique item creation and fast local search.

## Project Structure

```
.
├── ek_unique_cli.py     # Main CLI entry point
├── data/                # Local persistent storage for items
├── tests/               # Pytest test directory
├── .env.example         # Example environment variables
├── .gitignore           # Ignore pycache/ and data/
└── README.md            # This file
```

## Requirements

- Python 3.8+
- (For later stages) `pytest` for tests

## Setup

1. **(Recommended)** Create a virtualenv:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. **Install dependencies** (not needed for initial stub, but later: `pip install -r requirements.txt`)

3. **Configure environment variables**

    - Copy `.env.example` to `.env` and adjust, or export directly:
      ```bash
      export DATA_FILE=./data/items.json
      ```
    - By default, data will be stored at `./data/items.json`.

4. **Create data and tests directory:**
   - The structure is set up; nothing to do unless running tests later.

## Usage

Run the CLI tool:

```bash
python ek_unique_cli.py --help
```

You should see:

```
usage: ek_unique_cli.py [-h]

ek-unique-search-cli (skeleton CLI)

options:
  -h, --help  show this help message and exit
```

(The actual commands (create/search/list) will be implemented in later steps.)

## Development
- All code lives at root for now. Test files will be inside `tests/`.
- The `data/` folder is where items will be persisted as JSON.
- Store environment variable as per `.env.example`.

## Testing

Tests will be in `tests/` and runnable via:
```
pytest
```

(Once implemented; there are no real tests yet.)

---

## License
[MIT](LICENSE)
