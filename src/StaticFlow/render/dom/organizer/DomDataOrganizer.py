# DomDataOrganizer.py
# (C)2012-2013
# Scott Ernst

#___________________________________________________________________________________________________ DomDataOrganizer
class DomDataOrganizer(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, dataType, root, **kwargs):
        """Creates a new instance of DOMKeyOrganizer."""
        self._subs     = {}
        self._tempSubs = {}
        self._root     = dataType()
        self._tempRoot = dataType()
        self._joins    = []
        self._dataType = dataType

        if not root is None:
            self.add(root)

        if kwargs is None:
            return

        for n,v in kwargs.iteritems():
            self.add(v, n)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ join
    def join(self, *args):
        if not args:
            return

        for s in args:
            if not s in self._joins:
                self._joins.append(s)

#___________________________________________________________________________________________________ unjoin
    def unjoin(self, *args):
        if not args:
            return

        for s in args:
            try:
                self._joins.remove(s)
            except Exception, err:
                pass

#___________________________________________________________________________________________________ clearAllJoins
    def clearAllJoins(self, *args):
        self._joins = []

#___________________________________________________________________________________________________ add
    def add(self, *args, **kwargs):
        pass

#___________________________________________________________________________________________________ write
    def write(self, *args, **kwargs):
        pass

#===================================================================================================
#                                                                               P R O T E C T E D

