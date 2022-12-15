import warnings
from struct import error as StructError

from LnkParse3.extra_factory import ExtraFactory

"""
EXTRA_DATA:
Zero or more ExtraData structures (section 2.5).
"""


class ExtraData:
    def __init__(self, indata=None, cp=None):
        self.cp = cp
        self._raw = indata
        self._size = None  # Lazy loading

    def __iter__(self):
        return self._iter()

    def _iter(self):
        rest = self._raw
        length = 0
        while rest:
            factory = ExtraFactory(indata=rest)
            try:
                size = factory.item_size()
            except StructError:
                break

            if not size:
                break

            length += size
            data, rest = rest[:size], rest[size:]

            cls = factory.extra_class()
            if cls:
                yield cls(indata=data, cp=self.cp)

        self._size = length

    def size(self):
        if self._size is None:
            [x for x in self]
        return self._size

    def as_dict(self):
        res = {}
        for extra in self:
            try:
                res[extra.name()] = extra.as_dict()
            except (StructError, ValueError) as e:
                msg = "Error while parsing `%s` (%s)" % (extra.name(), e)
                warnings.warn(msg)
                continue
        return res
