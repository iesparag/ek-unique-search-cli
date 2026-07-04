import os
import json
import tempfile
import shutil
import uuid
import pytest
from domain import Item
import storage

# For temp env var override
import importlib

def make_item(name="foo", tags=None):
    return Item(id=str(uuid.uuid4()), name=name, tags=tags or ["hello", "world"])

def read_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def test_save_and_load_items(tmp_path, monkeypatch):
    data_file = str(tmp_path / 'items.json')
    monkeypatch.setenv('DATA_FILE', data_file)
    importlib.reload(storage)
    items = [make_item("alpha"), make_item("beta", tags=["x","y"])]
    storage.save_items(items)
    loaded = storage.load_items()
    assert len(loaded) == 2
    assert {i.name for i in loaded} == {"alpha", "beta"}
    # Test actual JSON contents
    jarr = read_json_file(data_file)
    assert all(isinstance(x, dict) for x in jarr)

def test_missing_file(monkeypatch, tmp_path):
    data_file = str(tmp_path / 'missing.json')
    monkeypatch.setenv('DATA_FILE', data_file)
    importlib.reload(storage)
    # File does not exist:
    out = storage.load_items()
    assert out == []

def test_corrupt_json(monkeypatch, tmp_path):
    data_file = str(tmp_path / 'corrupt.json')
    # Write some garbage/corrupt JSON
    with open(data_file, 'w', encoding='utf-8') as f:
        f.write('{ this is not valid JSON [ ]!')
    monkeypatch.setenv('DATA_FILE', data_file)
    importlib.reload(storage)
    # Load should warn, backup, and return []
    out = storage.load_items()
    assert out == []
    backup_file = data_file + '.backup-corrupt'
    assert os.path.exists(backup_file)
    # The backup contents match the corrupt file:
    with open(data_file, 'r', encoding='utf-8') as src, open(backup_file, 'r', encoding='utf-8') as bkp:
        assert src.read() == bkp.read()

def test_atomic_write(tmp_path, monkeypatch):
    data_file = str(tmp_path / 'atomic.json')
    monkeypatch.setenv('DATA_FILE', data_file)
    importlib.reload(storage)
    items = [make_item("z")]
    storage.save_items(items)
    # Should have written file;
    assert os.path.exists(data_file)
    # Now forcibly create stale .tmp to ensure we're robust to re-use
    tmpfile = data_file + '.tmp'
    with open(tmpfile, 'w') as f:
        f.write('old')
    # Second save should overwrite atomically, remove temp
    items2 = [make_item("y")]
    storage.save_items(items2)
    assert not os.path.exists(tmpfile)
    # File contains only 'y'
    arr = read_json_file(data_file)
    assert len(arr) == 1 and arr[0]['name'] == 'y'
