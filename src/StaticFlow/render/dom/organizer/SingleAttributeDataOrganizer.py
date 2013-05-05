# SingleAttributeDataOrganizer.py
# (C)2012-2013
# Scott Ernst

from pyaid.ArgsUtils import ArgsUtils
from pyaid.json.JSON import JSON
from StaticFlow.render.dom.organizer.KeyDataOrganizer import KeyDataOrganizer

#___________________________________________________________________________________________________ SingleAttributeDataOrganizer
class SingleAttributeDataOrganizer(KeyDataOrganizer):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, *args, **kwargs):
        """Creates a new instance of SingleAttributeDataOrganizer."""
        self._name = ArgsUtils.extract('name', None, kwargs, args, 0)
        root       = ArgsUtils.extract('root', None, kwargs, args, 1)
        super(SingleAttributeDataOrganizer, self).__init__(root=root, **kwargs)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: name
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _writeImpl
    def _writeImpl(self, value, params):
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

        return u'%s=\'%s\'' % (self._name, value)
