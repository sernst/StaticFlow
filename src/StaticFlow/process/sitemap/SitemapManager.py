# SitemapManager.py
# (C)2013
# Scott Ernst

from pyaid.file.FileUtils import FileUtils
from pyaid.web.mako.MakoRenderer import MakoRenderer

from StaticFlow.StaticFlowEnvironment import StaticFlowEnvironment
from StaticFlow.process.sitemap.SitemapEntry import SitemapEntry
from StaticFlow.process.SiteProcessUtils import SiteProcessUtils

#___________________________________________________________________________________________________ SitemapManager
class SitemapManager(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _TEMPLATE = '/seo/sitemap.mako'

#___________________________________________________________________________________________________ __init__
    def __init__(self, site):
        """Creates a new instance of SitemapManager."""
        self.site = site
        self._entries   = []

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: entries
    @property
    def entries(self):
        return self._entries

#___________________________________________________________________________________________________ GS: sitemapTargetPath
    @property
    def sitemapTargetPath(self):
        return FileUtils.createPath(self.site.targetWebRootPath, 'sitemap.xml', isFile=True)

#___________________________________________________________________________________________________ GS: sitemapTargetUrl
    @property
    def sitemapTargetUrl(self):
        domain = self.site.get('DOMAIN', None)
        if not domain:
            return u''
        return SiteProcessUtils.getUrlFromPath(self.site, domain, self.sitemapTargetPath)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ addUrl
    def add(self, page):
        """Doc..."""
        self._entries.append(SitemapEntry(self, page))

#___________________________________________________________________________________________________ write
    def write(self):
        mr = MakoRenderer(self._TEMPLATE, StaticFlowEnvironment.rootTemplatePath, {'sitemap':self})
        result = mr.render()

        if not mr.success:
            self.site.writeLogError(unicode(mr.errorMessage))
            return False

        return FileUtils.putContents(result, self.sitemapTargetPath)

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

