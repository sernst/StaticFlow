# RssEntry.py
# (C)2013
# Scott Ernst

import os

from PIL import Image

from pyaid.file.FileUtils import FileUtils
from pyaid.time.TimeUtils import TimeUtils

#___________________________________________________________________________________________________ RssEntry
class RssEntry(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, processor, generator, pageData):
        """Creates a new instance of RssEntry."""
        self.processor = processor
        self.generator = generator
        self.pageData  = pageData

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: thumbnailUrl
    @property
    def thumbnailUrl(self):
        path = self.pageData.get('THUMBNAIL')
        if not path:
            return None

        return self.processor.getSiteUrl(path, forceHttp=True, forceDeploy=True)

#___________________________________________________________________________________________________ GS: title
    @property
    def title(self):
        return self.pageData.title

#___________________________________________________________________________________________________ GS: url
    @property
    def url(self):
        return self.pageData.targetUrl

#___________________________________________________________________________________________________ GS: description
    @property
    def description(self):
        return self.pageData.description

#___________________________________________________________________________________________________ GS: date
    @property
    def date(self):
        return self.pageData.date

#___________________________________________________________________________________________________ GS: publishedDate
    @property
    def publishedDate(self):
        return TimeUtils.dateTimeToWebTimestamp(self.date)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________
    def createThumbnailMediaTag(self):
        url = self.thumbnailUrl
        if not url:
            return u''

        path = FileUtils.createPath(
            self.processor.sourceWebRootPath,
            self.pageData.get('THUMBNAIL').lstrip('/'), isFile=True)
        if not os.path.exists(path):
            return u''

        img = Image.open(path)
        w, h = img.size

        return u'<media:thumbnail url="%s" height="%s" width="%s" />' % (self.thumbnailUrl, w, h)

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

