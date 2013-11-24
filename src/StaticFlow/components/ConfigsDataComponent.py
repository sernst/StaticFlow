# ConfigsDataComponent.py
# (C)2013
# Scott Ernst

from pyaid.NullUtils import NullUtils
from pyaid.config.ConfigsDict import ConfigsDict
from pyaid.dict.DictUtils import DictUtils

#___________________________________________________________________________________________________ ConfigsDataComponent
class ConfigsDataComponent(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    DATA_GET_NULL = NullUtils.NULL('PAGE_DATA_GET')

#___________________________________________________________________________________________________ __init__
    def __init__(self):
        """Creates a new instance of ConfigsDataComponent."""
        self._data     = ConfigsDict()
        self._tempData = ConfigsDict()

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: dataSources
    @property
    def dataSources(self):
        return [self._tempData, self._data]

#___________________________________________________________________________________________________ GS: localDataSources
    @property
    def localDataSources(self):
        return [self._tempData, self._data]

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ has
    def has(self, key, allowFalse =True, localOnly =False):
        out     = self.get(key, self.DATA_GET_NULL, localOnly=localOnly)
        result  = out != self.DATA_GET_NULL
        if allowFalse:
            return result
        return out and result

#___________________________________________________________________________________________________ get
    def get(self, key, defaultValue =None, localOnly =False, **kwargs):
        if not key:
            return defaultValue
        sources = self.localDataSources if localOnly else self.dataSources
        for source in sources:
            out = source.get(key, defaultValue=self.DATA_GET_NULL)
            if out != self.DATA_GET_NULL:
                return out
        return defaultValue

#___________________________________________________________________________________________________ getMerged
    def getMerged(self, key, defaultValue =None, localOnly =False):
        items = []
        sources = self.localDataSources if localOnly else self.dataSources
        for source in sources:
            res = source.get(key, self.DATA_GET_NULL)
            if res != self.DATA_GET_NULL:
                items.append(res)

        if len(items) == 0:
            return defaultValue

        if len(items) == 1:
            return DictUtils.clone(items[0])

        out = items.pop()
        while len(items):
            out = DictUtils.merge(out, items.pop())
        return out

#___________________________________________________________________________________________________ addItem
    def addItem(self, key, value, temp =True):
        """Doc..."""
        key = key.lower()
        if temp:
            self._tempData.add(key, value)
        else:
            self._data.add(key, value)

#___________________________________________________________________________________________________ addItems
    def addItems(self, values, temp =True):
        for name, value in values.iteritems():
            self.addItem(name, value, temp=temp)

#___________________________________________________________________________________________________ removeItem
    def removeItem(self, key, fromData =False, fromTemp =False):
        key = key.lower()
        if not fromData and not fromTemp:
            fromTemp = True

        if fromTemp:
            self._tempData.remove(key)
        if fromData:
            self._data.remove(key)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _internalMethod
    def _internalMethod(self):
        """Doc..."""
        pass

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return unicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__

