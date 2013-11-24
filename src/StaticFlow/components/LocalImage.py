# LocalImage.py
# (C)2013
# Scott Ernst

import os

from PIL import Image

from pyaid.file.FileUtils import FileUtils

#___________________________________________________________________________________________________ LocalImage
class LocalImage(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, page, urlPath):
        """Creates a new instance of LocalImage."""
        self._page    = page
        self._urlPath = urlPath
        self._width   = 0
        self._height  = 0

        if not os.path.exists(self.path):
            return

        im = Image.open(self.path)
        self._width, self._height = im.size

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: width
    @property
    def width(self):
        return self._width

#___________________________________________________________________________________________________ GS: height
    @property
    def height(self):
        return self._height

#___________________________________________________________________________________________________ GS: url
    @property
    def url(self):
        return self._page.site.getSiteUrl(self.urlPath)

#___________________________________________________________________________________________________ GS: cdnUrl
    @property
    def cdnUrl(self):
        return self._page.site.cdnRootUrl + self.urlPath

#___________________________________________________________________________________________________ GS: urlPath
    @property
    def urlPath(self):
        return self._urlPath

#___________________________________________________________________________________________________ GS: path
    @property
    def path(self):
        return FileUtils.createPath(
            self._page.site.sourceWebRootPath, self.urlPath.lstrip('/'), isFile=True)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getUrl
    def getUrl(self, forceHttp =False, forceHttps =False, forceDeploy =False):
        return self._page.site.getSiteUrl(
            self.urlPath,
            forceHttp=forceHttp,
            forceHttps=forceHttps,
            forceDeploy=forceDeploy)

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
