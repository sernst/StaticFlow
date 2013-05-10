# SitemapEntry.py
# (C)2013
# Scott Ernst

import datetime

from pyaid.ArgsUtils import ArgsUtils

from StaticFlow.process.sitemap.SitemapFrequencyEnum import SitemapFrequencyEnum

#___________________________________________________________________________________________________ SitemapEntry
class SitemapEntry(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, manager, pageData, **kwargs):
        """Creates a new instance of SitemapEntry."""
        self._manager      = manager
        self._pageData     = pageData
        self._url          = pageData.targetUrl

        self._frequency    = ArgsUtils.get('frequency', None, kwargs)
        if self._frequency is None:
            self._frequency = pageData.get(('SEO', 'FREQUENCY'), SitemapFrequencyEnum.WEEKLY)

        self._priority = ArgsUtils.get('priority', None, kwargs)
        if self._priority is None:
            self._priority = pageData.get(('SEO', 'PRIORITY'), 0.5)

        self._lastModified = ArgsUtils.get('lastModified', None, kwargs)
        if not self._lastModified:
            self._lastModified = pageData.date if pageData.date else datetime.datetime.now()

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: url
    @property
    def url(self):
        return self._url
    @url.setter
    def url(self, value):
        self._url = value

#___________________________________________________________________________________________________ GS: lastModified
    @property
    def lastModified(self):
        return self._lastModified
    @lastModified.setter
    def lastModified(self, value):
        self._lastModified = value

#___________________________________________________________________________________________________ GS: lastModifiedTimestamp
    @property
    def lastModifiedTimestamp(self):
        if not self._lastModified:
            return None
        return self._lastModified.strftime('%Y-%m-%d')

#___________________________________________________________________________________________________ GS: priority
    @property
    def priority(self):
        return self._priority
    @priority.setter
    def priority(self, value):
        self._priority = value

#___________________________________________________________________________________________________ GS: changeFrequency
    @property
    def changeFrequency(self):
        return self._frequency
    @changeFrequency.setter
    def changeFrequency(self, value):
        self._frequency = value

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
