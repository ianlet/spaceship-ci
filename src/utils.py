class ValueObject(object):
    __slots__ = ()

    def __init__(self, *vals):
        if len(vals) != len(self.__slots__):
            raise TypeError(
                "%s.__init__ accepts %d arguments, got %d" % (type(self).__name__, len(self.__slots__), len(vals)))
        for slot, val in zip(self.__slots__, vals):
            super(ValueObject, self).__setattr__(slot, val)

    def __repr__(self):
        return ('<%s[0x%x] %s>'
                % (type(self).__name__, id(self),
                   ' '.join('%s=%r' % (slot, getattr(self, slot))
                            for slot in self.__slots__)))

    def _vals(self):
        return tuple(getattr(self, slot) for slot in self.__slots__)

    def __eq__(self, other):
        if not isinstance(other, ValueObject):
            return NotImplemented
        return self.__slots__ == other.__slots__ and self._vals() == other._vals()

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self._vals())

    def __setattr__(self, attr, val):
        if attr in self.__slots__:
            raise AttributeError("%s slot '%s' is read-only" % (type(self).__name__, attr))
        super(ValueObject, self).__setattr__(attr, val)
