# KeyDataOrganizer.py
# (C)2012-2013
# Scott Ernst

from pyaid.ArgsUtils import ArgsUtils
from pyaid.NullUtils import NullUtils
from pyaid.json.JSON import JSON
from StaticFlow.render.dom.organizer.DomDataOrganizer import DomDataOrganizer

#___________________________________________________________________________________________________ KeyDataOrganizer
class KeyDataOrganizer(DomDataOrganizer):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, *args, **kwargs):
        """Creates a new instance of KeyDataOrganizer."""
        root = ArgsUtils.extract('root', None, kwargs, args, 0)
        super(KeyDataOrganizer, self).__init__(dict, root, **kwargs)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ add
    def add(self, *args, **kwargs):
        """Adds a style or multiple styles to the KeyDataOrganizer.

        @@@param key:string
            If adding one style, the first argument is the name of the style to add. If adding
            multiple styles this argument is omitted.

        @@@param value:mixed,dict
            When adding a single style, this value can be any basic type that can be converted
            to a string. When adding multiple values this is the first argument and should be a
            dictionary of style name/value pairs.

        @@@param group:string
            Defaults to None, in which case the style(s) are added to the root group. Otherwise,
            specified the style group in which to add the style.
        """

        once = ArgsUtils.get('once', False, kwargs)

        if (len(args) > 0 and isinstance(args[0], basestring)) or 'key' in kwargs:
            key   = ArgsUtils.get('key', None, kwargs, args, 0)
            value = ArgsUtils.get('value', None, kwargs, args, 1)
            group = ArgsUtils.get('group', None, kwargs, args, 2)
            if key is None or value is None:
                return

            self._addKey(key, value, group, once)
            return

        value = ArgsUtils.get('value', None, kwargs, args, 0)
        group = ArgsUtils.get('group', None, kwargs, args, 1)

        if value is None:
            return

        self._addMultipleKeys(value, group, once)

#___________________________________________________________________________________________________ getKey
    def getKey(self, key, group =None, globalNull =False):
        """Doc..."""

        null = NullUtils.UNIVERSAL_NULL if globalNull else None

        if group is None:
            if key in self._root:
                return self._root.get(key, null)
        elif group in self._subs:
            if key in self._subs[group]:
                return self._subs[group].get(key, null)
        elif self._joins:
            for j in self._joins:
                k = j.getKey(key, group, globalNull=True)
                if k == NullUtils.UNIVERSAL_NULL:
                    continue
                return k

        return null

#___________________________________________________________________________________________________ getKeyGroup
    def getKeyGroup(self, group =None):
        """Doc..."""
        if group is None:
            items = self._root
        elif group in self._subs:
            items = self._subs[group]
        else:
            return None

        if self._joins:
            items = items.items()
            for j in self._joins:
                joinItems = j.getKeyGroup(group)
                if joinItems:
                    items += joinItems.items()
            items = dict(items)

        return items

#___________________________________________________________________________________________________ write
    def write(self, *args, **kwargs):
        """Doc..."""
        group = ArgsUtils.get('group', None, kwargs, args, 0)
        if group is None:
            target = self._root.items()
            if self._tempRoot:
                target         = target + self._tempRoot.items()
                self._tempRoot = {}

        elif group in self._subs:
            target = self._subs[group].items()
            if group in self._tempSubs:
                target = target + self._tempSubs[group].items()
        else:
            target = []

        if self._joins:
            for j in self._joins:
                joinGroup = j.getKeyGroup(group)
                if joinGroup:
                    target = (joinGroup.items() + target)

        if len(target) == 0:
            return u''

        return self._writeImpl(dict(target), kwargs)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _writeImpl
    def _writeImpl(self, value, kwargs):
        return JSON.asString(value)

#___________________________________________________________________________________________________ _addMultipleKeys
    def _addMultipleKeys(self, value, group, once):
        for n,v in value.iteritems():
            self._addKey(n, v, group, once)

#___________________________________________________________________________________________________ _addKey
    def _addKey(self, key, value, group, once):
        """Doc..."""
        if group is None:
            target      = self._tempRoot if once else self._root
            target[key] = value
        else:
            target = self._tempSubs if once else self._subs
            if not group in target:
                target[group] = {}
            target[group][key] = value
