# PageData.py
# (C)2013
# Scott Ernst

import os

from pyaid.dict.DictUtils import DictUtils
from pyaid.file.FileUtils import FileUtils
from pyaid.json.JSON import JSON

#___________________________________________________________________________________________________ PageData
class PageData(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, processor):
        """Creates a new instance of PageData."""
        self._processor  = processor
        self._rootWebPath = FileUtils.createPath(processor.htmlDefinitionPath, 'root', isDir=True)

        try:
            self._commonData = self._cleanDictKeys(JSON.fromFile(
                FileUtils.createPath(processor.htmlDefinitionPath, 'common.def', isFile=True)
            ))
        except Exception, err:
            self._commonData = dict()

        self._pageData   = dict()
        self._tempData   = dict()

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: dataSources
    @property
    def dataSources(self):
        return [self._tempData, self._pageData, self._commonData]

#___________________________________________________________________________________________________ GS: processor
    @property
    def processor(self):
        return self._processor

#___________________________________________________________________________________________________ GS: rootWebPath
    @property
    def rootWebPath(self):
        return self._rootWebPath

#___________________________________________________________________________________________________ GS: commonData
    @property
    def commonData(self):
        return self._commonData

#___________________________________________________________________________________________________ GS: pageData
    @property
    def pageData(self):
        return self._pageData

#___________________________________________________________________________________________________ GS: tempData
    @property
    def tempData(self):
        return self._tempData

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getUrlFromPath
    def getUrlFromPath(self, path):
        if not self.has('DOMAIN'):
            return u''

        isIndex = path.endswith('index.html')

        url = u'http://' + self.get('DOMAIN') + u'/'
        if path.startswith(self.rootWebPath):
            url += u'/'.join(
                self.getFolderParts(path, self.rootWebPath, includeFilename=not isIndex)
            )
        elif path.startswith(self.processor.targetRootPath):
            url += u'/'.join(
                self.getFolderParts(path, self.processor.targetRootPath, includeFilename=not isIndex)
            )
        else:
            return u''

        if isIndex and not url.endswith(u'/'):
            url += u'/'
        return url

#___________________________________________________________________________________________________ getFolderParts
    def getFolderParts(self, path, rootPath, includeFilename =False):
        if includeFilename:
            return path[len(rootPath):].strip(os.sep).split(os.sep)
        return os.path.dirname(path)[len(rootPath):].strip(os.sep).split(os.sep)

#___________________________________________________________________________________________________ clear
    def clear(self, page =True, temp =True):
        if page:
            self._pageData = dict()
        if temp:
            self._tempData = dict()

#___________________________________________________________________________________________________ loadPageData
    def loadPageData(self, path, clear =False):
        if clear:
            self.clear()

        if not os.path.exists(path):
            return False
        self._pageData = self._cleanDictKeys(JSON.fromFile(path))

#___________________________________________________________________________________________________ has
    def has(self, key, allowFalse =True):
        key = key.lower()
        for source in self.dataSources:
            if key not in source:
                continue
            if not allowFalse and not source[key]:
                continue

            return True
        return False

#___________________________________________________________________________________________________ get
    def get(self, key, defaultValue =None):
        key = key.lower()
        if key in self._tempData:
            return self._tempData[key]
        if key in self._pageData:
            return self._pageData[key]
        if key in self._commonData:
            return self._commonData[key]
        return defaultValue

#___________________________________________________________________________________________________ getMerged
    def getMerged(self, key, defaultValue =None):
        key = key.lower()
        items = []
        for source in self.dataSources:
            if key in source:
                items.append(source[key])
        if len(items) == 0:
            return defaultValue
        if len(items) == 1:
            return items[0]

        out = items.pop()
        while len(items):
            out = DictUtils.merge(out, items.pop())
        return out

#___________________________________________________________________________________________________ addItem
    def addItem(self, key, value, common =False, page =False):
        """Doc..."""
        key = key.lower()
        if common:
            self._commonData[key] = value
        elif page:
            self._pageData[key] = value
        else:
            self._tempData[key] = value

#___________________________________________________________________________________________________ addItems
    def addItems(self, values, common =False, page =False):
        if common:
            self._commonData = dict(self._commonData.items() + self._cleanDictKeys(values).items())
        elif page:
            self._pageData = dict(self._pageData.items() + self._cleanDictKeys(values).items())
        else:
            self._tempData = dict(self._tempData.items() + self._cleanDictKeys(values).items())

#___________________________________________________________________________________________________ removeItem
    def removeItem(self, key, common =False, page =False, temp =False):
        key = key.lower()
        if not common and not page and not temp:
            temp = True

        if common and key in self._commonData:
            del self._commonData[key]
        if page and key in self._pageData:
            del self._pageData[key]
        if temp and key in self._tempData:
            del self._tempData[key]

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _cleanDictKeys
    def _cleanDictKeys(self, source):
        out = dict()
        for key, value in source.iteritems():
            out[key.lower()] = value
        return out

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

