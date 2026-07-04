#!/usr/bin/env python3
"""ek_unique_cli.py: Command-line entry point for ek-unique-search-cli.
Currently a stub.
"""
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description="ek-unique-search-cli (skeleton CLI)"
    )
    # No subcommands yet
    args = parser.parse_args()
    # Only shows help for now
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

if __name__ == "__main__":
    main()
