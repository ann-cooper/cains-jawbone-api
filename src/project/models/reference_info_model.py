import datetime
from typing import Optional

from attrs import define, field

def convert_info_dict(cls):
    """Handle nested object,
    
    Reference
    ---------
    https://github.com/python-attrs/attrs/issues/140
    """
    def converter(obj):
        if isinstance(obj, cls):
            return obj
        else:
            print(obj)
            return cls(**obj)
    return converter

@define
class InfoDict:
    source: str = field()
    link: str = field()
    info: str = field()

@define
class ReferenceInfo:
    """Clue reference research info."""
    page: int = field()
    clue: str = field()
    created_date: datetime.date = field(default=None)
    reference: Optional[InfoDict] = field(default=None, converter=convert_info_dict(cls=InfoDict))
    _id: Optional[str] = field(default=None)

    def __attrs_post_init__(self):
        if not self.created_date:
            self.created_date = datetime.date.today().isoformat()

