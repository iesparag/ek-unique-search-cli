#!/usr/bin/env python3
"""ek_unique_cli.py: Command-line entry point for ek-unique-search-cli."""
import sys
import cli

def main():
    # All logic in cli.py
    cli.dispatch(sys.argv[1:])

if __name__ == "__main__":
    main()
