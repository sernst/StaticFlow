# ListDataOrganizer.py
# (C)2012-2013
# Scott Ernst

import re

from pyaid.ArgsUtils import ArgsUtils
from pyaid.json.JSON import JSON
from StaticFlow.render.dom.organizer.DomDataOrganizer import DomDataOrganizer

#___________________________________________________________________________________________________ ListDataOrganizer
class ListDataOrganizer(DomDataOrganizer):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _WS_DELIMITER = re.compile('[\s\t\n]+')

#___________________________________________________________________________________________________ __init__
    def __init__(self, *args, **kwargs):
        """Creates a new instance of ListDataOrganizer."""
        root = ArgsUtils.extract('root', None, kwargs, args, 0)
        if isinstance(root, basestring):
            root = [root]

        super(ListDataOrganizer, self).__init__(list, root, **kwargs)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ add
    def add(self, *args, **kwargs):
        """Adds item(s) to the existing list of items, ignoring duplicates.

        @@@param items:mixed,list
            The items argument can be a single item or a list of items.

        @@@param group:string
            The name of the group in which to add the items. Default of None adds the items to the
            root group.
        """

        items = ArgsUtils.get('items', None, kwargs, args, 0)
        if items is None or not items:
            return

        group = ArgsUtils.get('group', None, kwargs, args, 1)
        once  = ArgsUtils.get('once', False, kwargs)

        if group:
            target = self._tempSubs if once else self._subs
            if not group in target:
                target[group] = []
            for n in items:
                if not n in target[group]:
                    target[group].append(n)
        else:
            target = self._tempRoot if once else self._root
            for n in items:
                if not n in target:
                    target.append(n)

#___________________________________________________________________________________________________ remove
    def remove(self, items, group =None):
        """Rmoves item(s) from the existing list of items, ignoring duplicates.

        @@@param items:string,list
            The items argument can be a single item or a list of items.
        """

        if items is None or not items:
            return

        if group:
            if not group in self._subs:
                return

            for n in items:
                try:
                    self._subs[group].remove(n)
                except Exception, err:
                    pass
        else:
            for n in items:
                try:
                    self._root.remove(n)
                except Exception, err:
                    pass

#___________________________________________________________________________________________________ get
    def get(self, group =None, recursive =False, allowEmpty =False):
        """Retrieves the list of values for the specified group."""

        if group is None:
            g = self._root if self._root else []
        else:
            g = self._subs.get(group, [])

        if recursive and self._joins:
            for j in self._joins:
                g = g + j.get(group, recursive=True, allowEmpty=True)

        return g if g else ([] if allowEmpty else None)

#___________________________________________________________________________________________________ write
    def write(self, *args, **kwargs):
        """Doc..."""
        group = ArgsUtils.get('group', None, kwargs, args, 0)
        if group is None:
            target         = self._root + self._tempRoot
            self._tempRoot = []
        elif group in self._subs:
            target = self._subs[group]
            if group in self._tempSubs:
                target                = target + self._tempSubs[group]
                self._tempSubs[group] = []
            else:
                target = target + []
        else:
            target = []

        if self._joins:
            for j in self._joins:
                joinGroup = j.get(group, recursive=True)
                if joinGroup:
                    target.extend(joinGroup)
            target = set(target)

        return self._writeImpl(target, kwargs)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _writeImpl
    def _writeImpl(self, value, params):
        if len(value) == 0:
            return u''

        return JSON.asString(value)


