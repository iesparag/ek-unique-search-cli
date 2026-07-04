import uuid
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any
from datetime import datetime
from utils import sanitize_and_validate_name, parse_tags

@dataclass
class Item:
    id: str
    name: str
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def __post_init__(self):
        # Validation
        object.__setattr__(self, 'name', sanitize_and_validate_name(self.name))
        if not isinstance(self.tags, list):
            raise ValueError('tags must be a list of strings')
        self.tags = [t.strip() for t in self.tags if t.strip()]
        # created_at validation (ensure ISO format)
        try:
            datetime.fromisoformat(self.created_at)
        except Exception:
            raise ValueError('created_at must be a valid ISO timestamp')
        # id validation
        try:
            uuid.UUID(self.id)
        except Exception:
            raise ValueError('id must be a valid UUID string')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'tags': self.tags,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        # Defensive: assign empty list if tags is None
        return cls(
            id=data['id'],
            name=data['name'],
            tags=data.get('tags', []) or [],
            created_at=data['created_at'],
        )
