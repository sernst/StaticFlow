# LocalImage.py
# (C)2013
# Scott Ernst

import os

from PIL import Image

from pyaid.file.FileUtils import FileUtils

#___________________________________________________________________________________________________ LocalImage
class LocalImage(object):
    """ Wrapper class for locally accessible images within the site. Used for quick referencing
        their various properties. """

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, urlPath, site, page =None):
        """Creates a new instance of LocalImage."""
        self._site    = site
        self._page    = page
        self._urlPath = urlPath
        self._width   = 0
        self._height  = 0
        self._isValid = True

        if not self.exists:
            return

        try:
            im = Image.open(self.path)
            self._width, self._height = im.size
        except Exception, err:
            self._isValid = False
            site.writeLogWarning(u'Corrupt image file "%s"' % self.path)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: exists
    @property
    def exists(self):
        """ Whether or not the image was found to exist at the specified location on disk """
        return self._isValid and os.path.exists(self.path)

#___________________________________________________________________________________________________ GS: width
    @property
    def width(self):
        """ The width of the image in pixels """
        return self._width

#___________________________________________________________________________________________________ GS: height
    @property
    def height(self):
        """ The height of the image in pixels """
        return self._height

#___________________________________________________________________________________________________ GS: url
    @property
    def url(self):
        """ The URL for the image specific to the current type of deployment """
        return self._site.getSiteUrl(self.urlPath)

#___________________________________________________________________________________________________ GS: cdnUrl
    @property
    def cdnUrl(self):
        """ The deployed CDN URL for the image for the current type of deployment """
        return self._site.cdnRootUrl + self.urlPath

#___________________________________________________________________________________________________ GS: urlPath
    @property
    def urlPath(self):
        """ The path portion of the URL for the image """
        return self._urlPath

#___________________________________________________________________________________________________ GS: path
    @property
    def path(self):
        """ The absolute path of the image on disk """
        return FileUtils.createPath(
            self._site.sourceWebRootPath, self.urlPath.lstrip('/'), isFile=True)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getUrl
    def getUrl(self, forceHttp =False, forceHttps =False, forceDeploy =False):
        """ Returns the URL for the image formatted according to the specified argument values """
        return self._site.getSiteUrl(
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
