# AttributeDataOrganizer.py
# (C)2012-2013
# Scott Ernst

from pyaid.ArgsUtils import ArgsUtils
from pyaid.json.JSON import JSON
from StaticFlow.render.dom.organizer.KeyDataOrganizer import KeyDataOrganizer

#___________________________________________________________________________________________________ AttributeDataOrganizer
class AttributeDataOrganizer(KeyDataOrganizer):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, *args, **kwargs):
        """Creates a new instance of AttributeDataOrganizer."""
        root         = ArgsUtils.extract('root', None, kwargs, args, 0)
        self._prefix = ArgsUtils.extract('prefix', '', kwargs, args, 1)
        KeyDataOrganizer.__init__(self, root, **kwargs)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: prefix
    @property
    def prefix(self):
        return self._prefix
    @prefix.setter
    def prefix(self, value):
        self._prefix = value

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _createAttrs
    def _createAttrs(self, src):
        d = []
        for n,v in src.iteritems():
            out = self._createAttr(n, v)
            if out and len(out) > 0:
                d.append(out)

        return u' '.join(d)

#___________________________________________________________________________________________________ _createAttr
    def _createAttr(self, name, value):
        if not value:
            return u''
        elif isinstance(value, dict) or isinstance(value, list):
            value = JSON.asString(value)
        elif not isinstance(value, basestring):
            value = str(value)
        value = value.replace("'", "\'").replace('\n',' ')

        offset = value.find('\'')
        while offset != -1:
            if offset == 0 or value[offset-1] != '\\':
                value = value[:offset] + '\\' + value[offset:]
            offset = value.find('\'', offset + 1)

        return u'%s%s=\'%s\'' % (self._prefix, name, value)

#___________________________________________________________________________________________________ _writeImpl
    def _writeImpl(self, value, params):
        return self._createAttrs(value)
