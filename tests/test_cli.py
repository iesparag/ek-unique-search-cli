import pytest
from cli import build_parser, dispatch
from utils import generate_uuid
import sys
import tempfile
import os
import shutil
import uuid
import json
import importlib
from storage import save_items
from domain import Item

# monkeypatch sys.argv and capture stdout
from io import StringIO


def run_cli_cmd(cmd_args, monkeypatch):
    """Helper to run CLI dispatch for testing, capturing stdout and exit codes."""
    std_out, std_err = StringIO(), StringIO()
    monkeypatch.setattr(sys, 'stdout', std_out)
    monkeypatch.setattr(sys, 'stderr', std_err)
    exit_status = None
    def my_exit(code=0):
        nonlocal exit_status
        raise SystemExit(code)
    monkeypatch.setattr(sys, 'exit', my_exit)
    try:
        dispatch(cmd_args)
    except SystemExit as e:
        exit_status = e.code
    finally:
        output = std_out.getvalue()
        std_out.close(), std_err.close()
    return exit_status, output

def make_item(name=None, tags=None):
    return Item(id=generate_uuid(), name=name or f"item-{uuid.uuid4().hex[:4]}", tags=tags or [])

def test_parser_rejects_invalid_command():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(['not-a-cmd'])

def test_parser_create_and_search_flags():
    parser = build_parser()
    ns = parser.parse_args(["create", "--name", "hello", "--tags", "foo,bar"])
    assert ns.command == 'create'
    assert ns.name == 'hello'
    assert ns.tags == 'foo,bar'
    ns2 = parser.parse_args(["search", "--name", "he", "--tag", "foo"])
    assert ns2.command == 'search'
    assert ns2.name == 'he'
    assert ns2.tag == 'foo'
    ns3 = parser.parse_args(["list"])
    assert ns3.command == 'list'

def test_cli_create_and_duplicate(monkeypatch, tmp_path):
    data_file = str(tmp_path / 'items.json')
    monkeypatch.setenv('DATA_FILE', data_file)
    import storage; importlib.reload(storage)
    # First create
    code, out = run_cli_cmd(['create', '--name', 'MyTest', '--tags', 'a,b'], monkeypatch)
    assert code == 0
    assert 'Item created' in out
    assert 'MyTest' in out
    # Try duplicate name
    code2, out2 = run_cli_cmd(['create', '--name', 'MyTest'], monkeypatch)
    assert code2 == 1
    assert 'already exists' in out2

def test_cli_create_default_name(monkeypatch, tmp_path):
    data_file = str(tmp_path / 'items.json')
    monkeypatch.setenv('DATA_FILE', data_file)
    import storage; importlib.reload(storage)
    code, out = run_cli_cmd(['create'], monkeypatch)
    assert code == 0
    assert 'Item created' in out
    assert 'Name:' in out


def test_cli_search_and_list(monkeypatch, tmp_path):
    data_file = str(tmp_path / 'items.json')
    monkeypatch.setenv('DATA_FILE', data_file)
    import storage; importlib.reload(storage)
    items = [
        Item(id=generate_uuid(), name="foo", tags=['abc']),
        Item(id=generate_uuid(), name="alpha", tags=['x','y']),
        Item(id=generate_uuid(), name="bar", tags=['abc']),
    ]
    save_items(items)
    # List
    code, out = run_cli_cmd(['list'], monkeypatch)
    assert code == 0
    assert 'foo' in out and 'bar' in out and 'alpha' in out
    # Search by --name partial
    code2, out2 = run_cli_cmd(['search', '--name', 'al'], monkeypatch)
    assert code2 == 0
    assert 'alpha' in out2
    assert 'foo' not in out2
    # Search by --tag
    code3, out3 = run_cli_cmd(['search', '--tag', 'abc'], monkeypatch)
    assert code3 == 0
    assert 'foo' in out3 and 'bar' in out3

def test_cli_search_not_found(monkeypatch, tmp_path):
    data_file = str(tmp_path / 'items.json')
    monkeypatch.setenv('DATA_FILE', data_file)
    import storage; importlib.reload(storage)
    # Empty
    code, out = run_cli_cmd(['search', '--name', 'zzz'], monkeypatch)
    assert code == 0
    assert 'No items found' in out
    # List also empty
    code2, out2 = run_cli_cmd(['list'], monkeypatch)
    assert code2 == 0
    assert 'No items found' in out2

def test_cli_create_tag_parse_error(monkeypatch, tmp_path):
    data_file = str(tmp_path / 'items.json')
    monkeypatch.setenv('DATA_FILE', data_file)
    import storage; importlib.reload(storage)
    code, out = run_cli_cmd(['create', '--tags', 'foo,"bad,tag"'], monkeypatch)
    assert code == 1
    assert 'Error in tags' in out

def test_cli_help(monkeypatch):
    # "ek_unique_cli.py --help", i.e. cli.py will print help and exit 0
    std_out, std_err = StringIO(), StringIO()
    monkeypatch.setattr(sys, 'stdout', std_out)
    monkeypatch.setattr(sys, 'stderr', std_err)
    with pytest.raises(SystemExit) as e:
        dispatch(['--help'])
    output = std_out.getvalue()
    assert 'usage:' in output or 'ek-unique-search-cli' in output
