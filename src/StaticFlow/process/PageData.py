# PageData.py
# (C)2013
# Scott Ernst

import os
import datetime

from pyaid.ArgsUtils import ArgsUtils
from pyaid.NullUtils import NullUtils
from pyaid.dict.DictUtils import DictUtils
from pyaid.file.FileUtils import FileUtils
from pyaid.json.JSON import JSON
from pyaid.string.StringUtils import StringUtils
from pyaid.web.mako.MakoRenderer import MakoRenderer

from StaticFlow.StaticFlowEnvironment import StaticFlowEnvironment
from StaticFlow.render.MarkupProcessor import MarkupProcessor
from StaticFlow.process.SiteProcessUtils import SiteProcessUtils
from StaticFlow.process.rss.RssFileGenerator import RssFileGenerator

#___________________________________________________________________________________________________ PageData
class PageData(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _GET_NULL = NullUtils.NULL('PAGE_DATA_GET')

#___________________________________________________________________________________________________ __init__
    def __init__(self, processor, definitionPath, sourcePath =None, parentPage =None):
        """Creates a new instance of PageData."""
        self._processor         = processor
        self._markupProcessor   = None
        self._definitionPath    = FileUtils.cleanupPath(definitionPath, isFile=True)
        self._sourcePath        = sourcePath
        self._pageData          = dict()
        self._tempData          = dict()
        self._date              = None
        self._isProcessed       = False
        self._parentPage        = parentPage
        self._childPages        = []
        self._rssGenerator      = None

        self._loadPageData()

        # If an RSS definition exists create an RSS generator
        if self.get('RSS'):
            self._rssGenerator = RssFileGenerator(processor, self)

        sourcePath = self.sourcePath
        if sourcePath:
            self._date = FileUtils.getModifiedDatetime(sourcePath)

        # Creates multiple sub entries for universal folder files
        if not self.sourcePath and self.filename is None:
            folderPath = FileUtils.getDirectoryOf(self._definitionPath)
            for item in os.listdir(folderPath):
                if StringUtils.ends(item, ('.sfml', '.html')):
                    self._childPages.append(
                        processor.pages.create(
                            definitionPath=self._definitionPath,
                            sourcePath=FileUtils.createPath(folderPath, item, isFile=True),
                            parentPage=self
                        )
                    )

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: rssGenerator
    @property
    def rssGenerator(self):
        return self._rssGenerator
    @rssGenerator.setter
    def rssGenerator(self, value):
        self._rssGenerator = value

#___________________________________________________________________________________________________ GS: parentPage
    @property
    def parentPage(self):
        return self._parentPage

#___________________________________________________________________________________________________ GS: childPages
    @property
    def childPages(self):
        return self._childPages

#___________________________________________________________________________________________________ GS: filename
    @property
    def filename(self):
        filename = self.get('FILE_NAME')
        if filename is None:
            if self.sourcePath:
                filename = os.path.basename(self.sourcePath).rsplit('.', 1)[0]
            else:
                return None

        elif filename.endswith('.html'):
            filename = filename[:-5]

        if filename == '*':
            return None
        return filename

#___________________________________________________________________________________________________ GS: sourcePath
    @property
    def sourcePath(self):
        if self._sourcePath:
            return self._sourcePath

        fileNoExtension = self._definitionPath[:-3]
        if os.path.exists(fileNoExtension + 'sfml'):
            return fileNoExtension + 'sfml'
        if os.path.exists(fileNoExtension + 'html'):
            return fileNoExtension + 'html'
        return None

#___________________________________________________________________________________________________ GS: sourceFolder
    @property
    def sourceFolder(self):
        if self.sourcePath:
            return SiteProcessUtils.getFolderParts(
                self.sourcePath, self.processor.sourceWebRootPath
            )
        return  None

#___________________________________________________________________________________________________ GS: date
    @property
    def date(self):
        return self._date if self._date else datetime.datetime.now()

#___________________________________________________________________________________________________ GS: markupProcessor
    @property
    def markupProcessor(self):
        return self._markupProcessor
    @markupProcessor.setter
    def markupProcessor(self, value):
        self._markupProcessor = value

#___________________________________________________________________________________________________ GS: targetPath
    @property
    def targetPath(self):
        if not self.sourcePath:
            return None

        return FileUtils.createPath(
            self.processor.targetWebRootPath,
            self.sourceFolder,
            self.filename + '.html',
            isFile=True
        )

#___________________________________________________________________________________________________ GS: targetUrl
    @property
    def targetUrl(self):
        path = self.targetPath
        if not path:
            return None
        return SiteProcessUtils.getUrlFromPath(self.processor, self.get('DOMAIN'), path)

#___________________________________________________________________________________________________ GS: targetUrlLink
    @property
    def targetUrlLink(self):
        path = self.targetPath
        if not path:
            return None
        return '/' + path[len(self.processor.targetWebRootPath):]

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

#___________________________________________________________________________________________________ GS: isCompiled
    @property
    def isCompiled(self):
        path = self.sourcePath
        if not path:
            return True

        if self._markupProcessor or path.endswith('html'):
            return True
        return False

#___________________________________________________________________________________________________ GS: isProcessed
    @property
    def isProcessed(self):
        return self._isProcessed

#===================================================================================================
#                                                                                     P U B L I C

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

#___________________________________________________________________________________________________ compile
    def compile(self):
        for child in self._childPages:
            child.compile()

        if self.isCompiled:
            return True

        path = self.sourcePath
        if path and path.endswith('.sfml'):
            return self._compileMarkup()
        return True

#___________________________________________________________________________________________________ process
    def process(self):
        for child in self._childPages:
            child.process()

        if self.isProcessed:
            return True

        if self._createHtmlPage():
            self._isProcessed = True
        return self._isProcessed

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getSourceContent
    def _getSourceContent(self):
        if self._markupProcessor:
            return self._markupProcessor.get()
        elif not self.sourcePath:
            return u''
        return FileUtils.getContents(self.sourcePath)

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

#___________________________________________________________________________________________________ _loadPageData
    def _loadPageData(self):
        path = self._definitionPath
        if not path or not os.path.exists(path):
            return False
        self._pageData = DictUtils.lowerDictKeys(JSON.fromFile(path))

        pageVars = self.getMerged('PAGE_VARS', dict())
        self.addItem('PAGE_VARS', pageVars)
        for item in pageVars['SCRIPTS']:
            if len(item) == 3:
                item.pop(2 if self.processor.isLocal else 1)

        if 'DYNAMIC_DOMAIN' not in pageVars:
            pageVars['DYNAMIC_DOMAIN'] = '' if self.processor.isLocal else (
                u'//' + self.get('DYNAMIC_DOMAIN')
            )

#___________________________________________________________________________________________________ _compileMarkup
    def _compileMarkup(self):
        source = FileUtils.getContents(self.sourcePath)
        if source is None:
            return False

        mp = MarkupProcessor(source)
        mp.get()

        self._markupProcessor = mp

        if mp.hasErrors:
            for renderError in mp.renderErrors:
                print '\n' + 100*'-' + '\n   RENDER ERROR:\n', renderError.echo()
            return False

        self._date = self._parseDate(ArgsUtils.extract('date', None, mp.metadata))
        self.addItems(mp.metadata)
        return True

#___________________________________________________________________________________________________ _parseData
    def _parseDate(self, value):
        if not value:
            return None

        value = value.replace(u'/', u'-').strip().split(u'-')
        if len(value[-1]) < 4:
            value[-1] = u'20' + value[-1]

        return datetime.datetime(
            year=int(value[-1]),
            month=int(value[0]),
            day=int(value[1])
        )

#___________________________________________________________________________________________________ _createHtmlPage
    def _createHtmlPage(self):
        data = dict(
            processor=self.processor,
            loader=u'/js/int/loader.js',
            pageVars=JSON.asString(self.get('PAGE_VARS')),
            pageData=self,
            htmlSource=self._getSourceContent(),
        )

        mr = MakoRenderer(
            template=self.get('TEMPLATE'),
            rootPath=[
                self.processor.htmlTemplatePath,
                StaticFlowEnvironment.rootPublicTemplatePath
            ],
            data=data,
            minify=not self.processor.isLocal
        )
        result = mr.render()

        if not mr.success:
            print mr.errorMessage
            return False

        try:
            outDirectory = FileUtils.getDirectoryOf(self.targetPath)
            if not os.path.exists(outDirectory):
                os.makedirs(outDirectory)

            FileUtils.putContents(result, self.targetPath, raiseErrors=True)

            # Add the page to the sitemap
            self.processor.sitemap.add(self)

            print 'CREATED:', self.targetPath, ' -> ', self.targetUrl
        except Exception, err:
            print err
            return False
        return True

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

