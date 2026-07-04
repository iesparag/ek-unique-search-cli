import uuid
import re
from typing import List

MAX_NAME_LENGTH = 120  # Reasonable max length for item name
PROHIBITED_CHARS_RE = r'[\x00-\x1F\x7F]'  # Control characters (ASCII 0-31, 127)

class NameValidationError(ValueError):
    pass

def generate_uuid() -> str:
    """Return a uuid4 string."""
    return str(uuid.uuid4())

def sanitize_and_validate_name(name: str) -> str:
    if not isinstance(name, str):
        raise NameValidationError("Item name must be a string.")
    name = name.strip()
    if len(name) == 0:
        raise NameValidationError("Item name cannot be empty.")
    if len(name) > MAX_NAME_LENGTH:
        raise NameValidationError(
            f"Item name too long (>{MAX_NAME_LENGTH} chars)."
        )
    if re.search(PROHIBITED_CHARS_RE, name):
        raise NameValidationError(
            "Item name contains control or disallowed characters."
        )
    return name

def parse_tags(tags_str: str) -> List[str]:
    """
    Parse comma-separated tags string into a list of sanitized/non-empty tags.
    Tags may not contain commas or control chars; whitespace is stripped.
    Duplicate tags collapsed.
    """
    if not tags_str:
        return []
    tags = [t.strip() for t in tags_str.split(',')]
    out = set()
    for tag in tags:
        if not tag:
            continue
        # No control chars in tags
        if re.search(PROHIBITED_CHARS_RE, tag):
            raise ValueError(f"Tag '{tag}' contains control characters.")
        # No embedded commas
        if ',' in tag:
            raise ValueError(f"Comma not allowed inside single tag: '{tag}'")
        out.add(tag)
    return sorted(out)
