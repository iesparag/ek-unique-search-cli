import os
import json
import shutil
import errno
from typing import List
from dotenv import load_dotenv
from domain import Item
import threading

load_dotenv()

DATA_FILE = os.environ.get('DATA_FILE', './data/items.json')
_BACKUP_SUFFIX = '.backup-corrupt'

_lock = threading.Lock()

def _ensure_data_dir(filename: str):
    dirname = os.path.dirname(os.path.abspath(filename))
    if not os.path.isdir(dirname):
        try:
            os.makedirs(dirname, exist_ok=True)
        except Exception as e:
            raise RuntimeError(f'Could not create data directory {dirname}: {e}')

def load_items() -> List[Item]:
    """
    Reads items from DATA_FILE. If file does not exist, returns [].
    If corrupted JSON, prints warning, backs up corrupt file, returns [].
    Always returns List[Item].
    """
    filename = DATA_FILE
    _ensure_data_dir(filename)
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError('Data file does not contain a list.')
        items = [Item.from_dict(x) for x in data]
        return items
    except Exception as ex:
        print(f'Warning: Could not load items from {filename}: {ex}')
        # Attempt backup of corrupt file
        try:
            corrupt_path = filename + _BACKUP_SUFFIX
            shutil.copy(filename, corrupt_path)
            print(f'Corrupted data file backed up to {corrupt_path}')
        except Exception as backup_ex:
            print(f'Error: Could not backup corrupt file: {backup_ex}')
        return []

def save_items(items: List[Item]) -> None:
    """
    Write list of Item to file atomically (using temp + rename).
    Uses file lock to prevent corruption from concurrent writes.
    Raises on failure.
    """
    filename = DATA_FILE
    _ensure_data_dir(filename)
    tmp_path = filename + '.tmp'
    # Serialize items
    arr = [item.to_dict() for item in items]
    # Write atomically
    with _lock:
        try:
            with open(tmp_path, 'w', encoding='utf-8') as f:
                json.dump(arr, f, ensure_ascii=False, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, filename)  # atomic rename
        except Exception as e:
            # Remove possible temp file if failed
            try:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except Exception:
                pass
            raise RuntimeError(f'Could not save items to {filename}: {e}')
