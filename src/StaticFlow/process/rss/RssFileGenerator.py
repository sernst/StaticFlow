# RssFileGenerator.py
# (C)2013
# Scott Ernst

import datetime

from pyaid.file.FileUtils import FileUtils
from pyaid.string.StringUtils import StringUtils
from pyaid.web.mako.MakoRenderer import MakoRenderer

from StaticFlow.StaticFlowEnvironment import StaticFlowEnvironment
from StaticFlow.process.rss.RssEntry import RssEntry

#___________________________________________________________________________________________________ RssFileGenerator
class RssFileGenerator(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    RSS_DATE_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

    _TEMPLATE = '/rss/rss.mako'


#___________________________________________________________________________________________________ __init__
    def __init__(self, processor, pageData):
        """Creates a new instance of RssFileGenerator."""
        self._processor = processor
        self._pageData  = pageData
        self._entries   = []

        self._includePaths = []
        incs = pageData.get(('RSS', 'INCLUDES'))
        if incs and isinstance(incs, basestring):
            incs = [incs]
        for inc in incs:
            self._includePaths.append(FileUtils.createPath(
                self._processor.sourceWebRootPath,
                inc.strip().replace('\\', '/').strip('/').split('/'),
                isDir=True
            ))

        self._processor.rssGenerators.append(self)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: title
    @property
    def title(self):
        out = self._pageData.get(('RSS', 'TITLE'), None)
        if not out:
            return self._pageData.get('TITLE', u'')
        return out

#___________________________________________________________________________________________________ GS: description
    @property
    def description(self):
        out = self._pageData.get(('RSS', 'DESCRIPTION'), None)
        if not out:
            return self._pageData.get('DESCRIPTION', u'')
        return out

#___________________________________________________________________________________________________ GS: homeUrl
    @property
    def homeUrl(self):
        return self._pageData.targetUrl

#___________________________________________________________________________________________________ GS: entries
    @property
    def entries(self):
        return self._entries

#___________________________________________________________________________________________________ GS: targetPath
    @property
    def targetPath(self):
        return FileUtils.createPath(
            FileUtils.getDirectoryOf(self._pageData.targetPath), 'rss.xml', isFile=True
        )

#___________________________________________________________________________________________________ GS: compiledTimestamp
    @property
    def compiledTimestamp(self):
        return datetime.datetime.utcnow().strftime(self.RSS_DATE_FORMAT)

#___________________________________________________________________________________________________ GS: lastModifiedTimestamp
    @property
    def lastModifiedTimestamp(self):
        if not self._entries:
            return self.compiledTimestamp

        lastDate = self._entries[0].date
        for entry in self._entries[1:]:
            if entry.date > lastDate:
                lastDate = entry.date

        return lastDate.strftime(self.RSS_DATE_FORMAT)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ addEntry
    def addEntry(self, pageData):
        sourcePath = pageData.sourcePath
        if not sourcePath or not StringUtils.begins(sourcePath, self._includePaths):
            return False
        self._entries.append(RssEntry(self._processor, self, pageData))
        pageData.rssGenerator = self
        return True

#___________________________________________________________________________________________________ write
    def write(self):
        """Doc..."""

        mr = MakoRenderer(self._TEMPLATE, StaticFlowEnvironment.rootTemplatePath, {'rss':self})
        result = mr.render()
        if not mr.success:
            print mr.errorMessage
            return False

        return FileUtils.putContents(result, self.targetPath)

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

