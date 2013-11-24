# Sitemap.py
# (C)2013
# Scott Ernst

from pyaid.file.FileUtils import FileUtils
from pyaid.web.mako.MakoRenderer import MakoRenderer

from StaticFlow.StaticFlowEnvironment import StaticFlowEnvironment
from StaticFlow.process.sitemap.SitemapEntry import SitemapEntry
from StaticFlow.process.SiteProcessUtils import SiteProcessUtils

#___________________________________________________________________________________________________ Sitemap
class Sitemap(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _TEMPLATE = '/seo/sitemap.mako'

#___________________________________________________________________________________________________ __init__
    def __init__(self, site):
        """Creates a new instance of Sitemap."""
        self.site = site
        self._entries   = []

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: entries
    @property
    def entries(self):
        """ List of SitemapEntry instances for all the Pages that will be included in the sitemap
            when generated """
        return self._entries

#___________________________________________________________________________________________________ GS: targetPath
    @property
    def targetPath(self):
        """ Absolute path to the location on disk where the generated Sitemap will be written """
        return FileUtils.createPath(self.site.targetWebRootPath, 'sitemap.xml', isFile=True)

#___________________________________________________________________________________________________ GS: targetUrl
    @property
    def targetUrl(self):
        """ The URL of the sitemap formatted in accordance with the type of site deployment """
        domain = self.site.get('DOMAIN', None)
        if not domain:
            return u''
        return SiteProcessUtils.getUrlFromPath(self.site, domain, self.targetPath)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ has
    def has(self, page):
        """ Specifies whether or not the Sitemap has an entry for the page in question """
        for entry in self._entries:
            if entry.page == page:
                return True
        return False

#___________________________________________________________________________________________________ add
    def add(self, page):
        """ Adds the specified page to the Sitemap's list of entries if it is not already listed """
        if not self.has(page):
            self._entries.append(SitemapEntry(self, page))

#___________________________________________________________________________________________________ write
    def write(self):
        """ Generates the sitemap and writes the result to the targetPath """

        mr = MakoRenderer(self._TEMPLATE, StaticFlowEnvironment.rootTemplatePath, {'sitemap':self})
        result = mr.render()

        if not mr.success:
            self.site.writeLogError(unicode(mr.errorMessage))
            return False

        if not FileUtils.putContents(result, self.targetPath):
            self.site.writeLogError(u'Unable to save sitemap file at: "%s"' % self.targetPath)
            return False

        self.site.writeLogSuccess(u'SITEMAP', u'Created sitemap at: "%s"' % self.targetPath)
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

