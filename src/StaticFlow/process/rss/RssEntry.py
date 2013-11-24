# RssEntry.py
# (C)2013
# Scott Ernst

from pyaid.time.TimeUtils import TimeUtils

#___________________________________________________________________________________________________ RssEntry
class RssEntry(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, site, generator, page):
        """Creates a new instance of RssEntry."""
        self.site      = site
        self.generator = generator
        self.page      = page

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: thumbnailUrl
    @property
    def thumbnailUrl(self):
        thumb = self.page.thumbnail
        if not thumb:
            return None

        return thumb.getUrl(forceHttp=True, forceDeploy=True)

#___________________________________________________________________________________________________ GS: title
    @property
    def title(self):
        return self.page.title

#___________________________________________________________________________________________________ GS: url
    @property
    def url(self):
        return self.page.targetUrl

#___________________________________________________________________________________________________ GS: description
    @property
    def description(self):
        return self.page.description

#___________________________________________________________________________________________________ GS: date
    @property
    def date(self):
        return self.page.date

#___________________________________________________________________________________________________ GS: publishedDate
    @property
    def publishedDate(self):
        return TimeUtils.dateTimeToWebTimestamp(self.date)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________
    def createThumbnailMediaTag(self):
        thumb = self.page.thumbnail
        if not thumb:
            return u''

        return u'<media:thumbnail url="%s" height="%s" width="%s" />' % (
            self.thumbnailUrl, thumb.width, thumb.height)

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

