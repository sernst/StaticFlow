# SingleValuedDataOrganizer.py
# (C)2012-2013
# Scott Ernst

from pyaid.ArgsUtils import ArgsUtils
from pyaid.json.JSON import JSON
from StaticFlow.render.dom.organizer.DomDataOrganizer import DomDataOrganizer

#___________________________________________________________________________________________________ SingleValuedDataOrganizer
class SingleValuedDataOrganizer(DomDataOrganizer):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, *args, **kwargs):
        """Creates a new instance of SingleValuedDataOrganizer."""
        root     = ArgsUtils.extract('root', None, kwargs, args, 0)
        DomDataOrganizer.__init__(self, unicode, root, **kwargs)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ add
    def add(self, *args, **kwargs):
        """Adds value to the existing item, replacing existing entries.

        @@@param value:string
            The value argument can be a single value.

        @@@param group:string
            The name of the group in which to add the value. Default of None adds the value to the
            root group.
        """

        value = ArgsUtils.get('value', None, kwargs, args, 0)
        if value is None:
            value = u''
        elif isinstance(value, dict) or isinstance(value, list):
            value = JSON.asString(value)
        else:
            value = unicode(value)

        group = ArgsUtils.get('group', None, kwargs, args, 1)
        once  = ArgsUtils.get('once', False, kwargs)

        if group:
            target        = self._tempSubs if once else self._subs
            target[group] = value
        else:
            if once:
                self._tempRoot = value
            else:
                self._root = value

#___________________________________________________________________________________________________ get
    def get(self, group =None):
        """Doc..."""
        if group is None:
            return self._root

        return self._subs.get(group, None)

#___________________________________________________________________________________________________ write
    def write(self, *args, **kwargs):
        """Doc..."""
        group = ArgsUtils.get('group', None, kwargs, args, 0)
        if group is None:
            value = self._tempRoot if self._tempRoot else self._root
            self._tempRoot = u''
        elif group in self._subs:
            if group in self._tempSubs:
                value = self._tempSubs[group]
                del(self._tempSubs[group])
            else:
                value = self._subs[group]
        else:
            value = u''

        return self._writeImpl(value, *args, **kwargs)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _writeImpl
    def _writeImpl(self, value, *args, **kwargs):
        if not value:
            for j in self._joins:
                v = j.write(**kwargs)
                if v:
                    return v

            return u''

        return value


