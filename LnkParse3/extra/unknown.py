from LnkParse3.extra.lnk_extra_base import LnkExtraBase


class UnknownExtra(LnkExtraBase):
    def name(self):
        return "UNKNOWN_EXTRA"

    @property
    def extra_data(self):
        start = 4
        return self._raw[start:]

    def as_dict(self):
        tmp = super().as_dict()
        return tmp
