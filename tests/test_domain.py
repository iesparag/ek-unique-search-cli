import pytest
import uuid
from datetime import datetime
from domain import Item
from utils import generate_uuid, sanitize_and_validate_name, parse_tags, NameValidationError

def test_generate_uuid():
    u = generate_uuid()
    assert isinstance(u, str)
    assert uuid.UUID(u)

def test_sanitize_and_validate_name_valid():
    assert sanitize_and_validate_name('foo') == 'foo'
    assert sanitize_and_validate_name('   bar baz  ') == 'bar baz'
    # Max length
    name = 'a' * 120
    assert sanitize_and_validate_name(name) == name

def test_sanitize_and_validate_name_invalid():
    # Too long
    with pytest.raises(NameValidationError):
        sanitize_and_validate_name('a'*121)
    # Empty string
    with pytest.raises(NameValidationError):
        sanitize_and_validate_name('   ')
    # Control chars
    with pytest.raises(NameValidationError):
        sanitize_and_validate_name('foo\x05bar')
    with pytest.raises(NameValidationError):
        sanitize_and_validate_name('foo\u0000bar')
    # Non-str
    with pytest.raises(NameValidationError):
        sanitize_and_validate_name(123)

def test_parse_tags_valid():
    assert parse_tags('') == []
    assert parse_tags('foo') == ['foo']
    assert parse_tags('foo,bar,baz') == ['bar', 'baz', 'foo']
    # Duplicate tags collapsed, order sorted
    assert parse_tags('foo,bar,foo') == ['bar', 'foo']
    # Whitespace
    assert parse_tags('alpha,  beta , gamma  ,') == ['alpha', 'beta', 'gamma']

def test_parse_tags_invalid():
    # Control char
    with pytest.raises(ValueError):
        parse_tags('a\x04b')
    # Embedded comma in tag
    with pytest.raises(ValueError):
        parse_tags('foo,"invalid,tag"')

def make_raw_item_dict():
    return {
        'id': generate_uuid(),
        'name': 'foobaz',
        'tags': ['a', 'b', 'c'],
        'created_at': datetime.utcnow().isoformat(),
    }

def test_item_to_from_dict():
    raw = make_raw_item_dict()
    item = Item.from_dict(raw)
    d = item.to_dict()
    assert d['id'] == raw['id']
    assert d['name'] == raw['name']
    assert set(d['tags']) == set(raw['tags'])
    assert d['created_at'] == raw['created_at']
    # .from_dict roundtrip
def test_item_enforces_validation():
    # Invalid name
    d = make_raw_item_dict()
    d['name'] = '\x03badname'
    with pytest.raises(Exception):
        Item.from_dict(d)
    # Invalid id
    d = make_raw_item_dict()
    d['id'] = 'notauuid'
    with pytest.raises(Exception):
        Item.from_dict(d)
    # Invalid created_at
    d = make_raw_item_dict()
    d['created_at'] = 'notadate'
    with pytest.raises(Exception):
        Item.from_dict(d)
    # tags not a list
    d = make_raw_item_dict()
    d['tags'] = 'foo'
    with pytest.raises(Exception):
        Item.from_dict(d)
