# RssFileGenerator.py
# (C)2013
# Scott Ernst

import datetime

from pyaid.file.FileUtils import FileUtils
from pyaid.string.StringUtils import StringUtils
from pyaid.time.TimeUtils import TimeUtils
from pyaid.web.mako.MakoRenderer import MakoRenderer

from StaticFlow.StaticFlowEnvironment import StaticFlowEnvironment
from StaticFlow.process.rss.RssEntry import RssEntry

#___________________________________________________________________________________________________ RssFileGenerator
class RssFileGenerator(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _TEMPLATE = '/rss/rss.mako'

#___________________________________________________________________________________________________ __init__
    def __init__(self, processor, pageData):
        """Creates a new instance of RssFileGenerator."""
        self._processor = processor
        self._pageData  = pageData
        self._entries   = []
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

#___________________________________________________________________________________________________ GS: thumbnail
    @property
    def thumbnail(self):
        return self._processor.getSiteUrl(
            self._pageData.get('THUMBNAIL', u''), forceHttp=True, forceDeploy=True)

#___________________________________________________________________________________________________ GS: homeUrl
    @property
    def homeUrl(self):
        return self._pageData.targetUrl

#___________________________________________________________________________________________________ GS: rssUrl
    @property
    def rssUrl(self):
        return self.homeUrl + 'rss.xml'

#___________________________________________________________________________________________________ GS: entries
    @property
    def entries(self):
        return self._entries

#___________________________________________________________________________________________________ GS: targetPath
    @property
    def targetPath(self):
        return FileUtils.createPath(
            FileUtils.getDirectoryOf(self._pageData.targetPath), 'rss.xml', isFile=True)

#___________________________________________________________________________________________________ GS: compiledTimestamp
    @property
    def compiledTimestamp(self):
        return TimeUtils.dateTimeToWebTimestamp(datetime.datetime.utcnow())

#___________________________________________________________________________________________________ GS: lastModifiedTimestamp
    @property
    def lastModifiedTimestamp(self):
        if not self._entries:
            return self.compiledTimestamp

        lastDate = self._entries[0].date
        for entry in self._entries[1:]:
            if entry.date > lastDate:
                lastDate = entry.date

        return TimeUtils.dateTimeToWebTimestamp(lastDate)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ hasPage
    def hasPage(self, pageData):
        for entry in self._entries:
            if entry.pageData == pageData:
                return True
        return False

#___________________________________________________________________________________________________ populate
    def populate(self):
        # Create the entry and add a reference to this generator in the rss owners of the page
        for page in self._pageData.referencedPages:
            if not self.hasPage(page):
                self._entries.append(RssEntry(self._processor, self, page))
                page.addRssOwner(self)

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

