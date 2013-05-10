# PageData.py
# (C)2013
# Scott Ernst

import os

from pyaid.NullUtils import NullUtils
from pyaid.dict.DictUtils import DictUtils
from pyaid.file.FileUtils import FileUtils
from pyaid.json.JSON import JSON

from StaticFlow.render.MarkupProcessor import MarkupProcessor
from StaticFlow.process.SiteProcessUtils import SiteProcessUtils

#___________________________________________________________________________________________________ PageData
class PageData(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _GET_NULL = NullUtils.NULL('PAGE_DATA_GET')

#___________________________________________________________________________________________________ __init__
    def __init__(self, processor, sourcePath =None):
        """Creates a new instance of PageData."""
        self._processor  = processor
        self._sourcePath = sourcePath
        self._targetPath = None
        self._pageData        = dict()
        self._tempData        = dict()
        self._markupProcessor = None
        self._date            = None

        if not sourcePath:
            return

        if sourcePath.endswith('.sfml'):
            self._compileMarkup()

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: date
    @property
    def date(self):
        return self._date
    @date.setter
    def date(self, value):
        self._date = value

#___________________________________________________________________________________________________ GS: markupProcessor
    @property
    def markupProcessor(self):
        return self._markupProcessor
    @markupProcessor.setter
    def markupProcessor(self, value):
        self._markupProcessor = value

#___________________________________________________________________________________________________ GS: sourcePath
    @property
    def sourcePath(self):
        return self._sourcePath

#___________________________________________________________________________________________________ GS: targetPath
    @property
    def targetPath(self):
        return self._targetPath
    @targetPath.setter
    def targetPath(self, value):
        self._targetPath = value

#___________________________________________________________________________________________________ GS: targetUrl
    @property
    def targetUrl(self):
        path = self.targetPath
        if not path:
            return None
        return SiteProcessUtils.getUrlFromPath(self.processor, self.get('DOMAIN'), path)

#___________________________________________________________________________________________________ GS: dataSources
    @property
    def dataSources(self):
        return [self._tempData, self._pageData, self.processor.siteData]

#___________________________________________________________________________________________________ GS: processor
    @property
    def processor(self):
        return self._processor

#___________________________________________________________________________________________________ GS: siteData
    @property
    def siteData(self):
        return self._processor.siteData

#___________________________________________________________________________________________________ GS: pageData
    @property
    def pageData(self):
        return self._pageData
    @pageData.setter
    def pageData(self, value):
        self._pageData = value

#___________________________________________________________________________________________________ GS: tempData
    @property
    def tempData(self):
        return self._tempData
    @tempData.setter
    def tempData(self, value):
        self._tempData = value

#___________________________________________________________________________________________________ GS: htmlSource
    @property
    def htmlSource(self):
        return None
    @htmlSource.setter
    def htmlSource(self, value):
        pass


#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ clone
    def clone(self, page =False, temp =False):
        out = PageData(self._processor)
        if page:
            out.pageData = DictUtils.clone(self._pageData)
        if temp:
            out.pageData = DictUtils.clone(self._tempData)
        return out

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
        self._pageData = DictUtils.lowerDictKeys(JSON.fromFile(path))

#___________________________________________________________________________________________________ has
    def has(self, key, allowFalse =True):
        out     = self.get(key, self._GET_NULL)
        result  = out != self._GET_NULL
        if allowFalse:
            return result
        return out and result

#___________________________________________________________________________________________________ get
    def get(self, key, defaultValue =None):
        if not key:
            return defaultValue

        if not isinstance(key, basestring):
            sources = self.dataSources
            for k in key:
                sources = self._getFromDataDicts(k.lower(), sources)
                if sources == self._GET_NULL:
                    return defaultValue
            return sources[0]

        out = self._getFromDataDicts(key.lower(), self.dataSources)
        if out == self._GET_NULL:
            return defaultValue
        return out[0]

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
            self._processor.siteData[key] = value
        elif page:
            self._pageData[key] = value
        else:
            self._tempData[key] = value

#___________________________________________________________________________________________________ addItems
    def addItems(self, values, page =False):
        if page:
            self._pageData = dict(self._pageData.items() + DictUtils.lowerDictKeys(values).items())
        else:
            self._tempData = dict(self._tempData.items() + DictUtils.lowerDictKeys(values).items())

#___________________________________________________________________________________________________ removeItem
    def removeItem(self, key, page =False, temp =False):
        key = key.lower()
        if not page and not temp:
            temp = True

        if page and key in self._pageData:
            del self._pageData[key]
        if temp and key in self._tempData:
            del self._tempData[key]

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getFromDataDicts
    def _getFromDataDicts(self, key, items):
        out = []
        for item in items:
            for value in item.items():
                if value[0].lower() == key:
                    out.append(value[1])
        if out:
            return out
        return self._GET_NULL

#___________________________________________________________________________________________________ _compileMarkup
    def _compileMarkup(self):
        source = FileUtils.getContents(self.sourcePath)
        if not source:
            return False

        p = MarkupProcessor(source)
        result = p.get()
        self._markupProcessor = p

        if p.hasErrors:
            for renderError in p.renderErrors:
                print '\n' + 100*'-' + '\n   RENDER ERROR:\n', renderError.echo()

        targetPath = FileUtils.changePathRoot(
            self.sourcePath,
            self.processor.sourceWebRootPath,
            self.processor.targetWebRootPath
        )
        targetPath = targetPath.rsplit('.', 1)[0] + '.sfmlp'

        FileUtils.getDirectoryOf(targetPath, createIfMissing=True)
        if not FileUtils.putContents(result, targetPath, raiseErrors=True):
            return False

        targetPath = targetPath.rsplit('.', 1)[0] + '.sfmeta'
        return FileUtils.putContents(JSON.asString(p.metadata), targetPath)

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

