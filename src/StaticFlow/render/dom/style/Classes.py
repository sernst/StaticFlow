# Classes.py
# (C)2012-2013
# Scott Ernst

import re

from pyaid.ArgsUtils import ArgsUtils

from StaticFlow.render.dom.organizer.ListDataOrganizer import ListDataOrganizer

#___________________________________________________________________________________________________ Classes
class Classes(ListDataOrganizer):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _WS_DELIMITER = re.compile('[\s\t\n]+')

#___________________________________________________________________________________________________ __init__
    def __init__(self, root, **kwargs):
        """Creates a new instance of Classes."""
        ListDataOrganizer.__init__(self, root, **kwargs)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ add
    def add(self, *args, **kwargs):
        """Adds class(es) to the existing list of classes, ignoring duplicates.

        @@@param names:string,list
            The names argument can be a single class name, a whitespace-delimited list of class
            names or a list of class names.
        """

        names = ArgsUtils.get('items', None, kwargs, args, 0)
        if names is None or not names:
            return

        if isinstance(names, basestring):
            names = Classes._WS_DELIMITER.split(names)

        group = ArgsUtils.get('group', None, kwargs, args, 1)

        ListDataOrganizer.add(self, names, group)

#___________________________________________________________________________________________________ remove
    def remove(self, items, group =None):
        """Rmoves class(es) from the existing list of classes, ignoring duplicates.

        @@@param names:string,list
            The names argument can be a single class name, a whitespace-delimited list of class
            names or a list of class names.
        """

        if items is None or not items:
            return

        if isinstance(items, basestring):
            items = Classes._WS_DELIMITER.split(items)

        ListDataOrganizer.remove(self, items, group)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _writeImpl
    def _writeImpl(self, value, params):
        if len(value) == 0:
            return u''

        res = u' '.join(value)

        if params.get('wrap', True):
            return u'class=\'%s\'' % res
        else:
            return res

