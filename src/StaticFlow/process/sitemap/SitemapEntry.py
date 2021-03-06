# SitemapEntry.py
# (C)2013
# Scott Ernst

from pyaid.ArgsUtils import ArgsUtils

from StaticFlow.process.sitemap.SitemapFrequencyEnum import SitemapFrequencyEnum

#___________________________________________________________________________________________________ SitemapEntry
class SitemapEntry(object):
    """ Represents a page within a sitemap """

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, sitemap, page, **kwargs):
        """Creates a new instance of SitemapEntry."""
        self.sitemap = sitemap
        self.page    = page
        self.url     = page.targetUrl
        self._data   = kwargs

        self.changeFrequency = ArgsUtils.get('frequency', None, kwargs)
        if self.changeFrequency is None:
            self.changeFrequency = page.get(('SEO', 'FREQUENCY'), SitemapFrequencyEnum.WEEKLY)

        self.priority = ArgsUtils.get('priority', None, kwargs)
        if self.priority is None:
            self.priority = page.get(('SEO', 'PRIORITY'), 0.5)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: lastModified
    @property
    def lastModified(self):
        out = ArgsUtils.get('lastModified', None, self._data)
        if not out:
            out = self.page.lastModified
        return out

#___________________________________________________________________________________________________ GS: lastModifiedTimestamp
    @property
    def lastModifiedTimestamp(self):
        if not self.lastModified:
            return None
        return self.lastModified.strftime('%Y-%m-%d')

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
