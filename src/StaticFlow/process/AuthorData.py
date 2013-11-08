# AuthorData.py
# (C)2013
# Scott Ernst

import urllib
import urlparse

from pyaid.config.ConfigsDict import ConfigsDict

#___________________________________________________________________________________________________ AuthorData
class AuthorData(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, pageData):
        """Creates a new instance of AuthorData."""
        self._pageData  = pageData
        self._id        = pageData.get('AUTHOR')
        self._data      = None

        if self._id is None:
            return

        authId = self._id.strip().replace(' ', '').lower()
        self._data = pageData.get(['SITE_AUTHORS', authId])
        if self._data is not None:
            self._data = ConfigsDict(self._data)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: name
    @property
    def name(self):
        if self._id is None:
            return u'Unknown'

        if self._data is None:
            return self._id

        n = self._data.get('NAME')
        if n is None:
            return self._id
        return n

#___________________________________________________________________________________________________ GS: gplusAuthorUrl
    @property
    def gplusAuthorUrl(self):
        if self._data is None:
            return None

        gplus = self._data.get('GPLUS')
        if gplus is None:
            return None

        # If the google plus profile url exists, parse it to add the rel=author query parameter,
        # which is required to prove authorship, and then return the modified url
        gplus = list(urlparse.urlsplit(gplus))
        if not gplus[0]:
            gplus[0] = u'http'

        query        = urlparse.parse_qs(gplus[3]) if gplus[3] else dict()
        query['rel'] = 'author'
        gplus[3]     = urllib.urlencode(query)

        return urlparse.urlunsplit(gplus)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ createAuthorLink
    def createAuthorLink(self, linkContents =None):
        if self._id is None:
            return u'Unknown'

        if self._data is None:
            return self._id

        url = self.gplusAuthorUrl
        if not url:
            return self._id
        return u'<a href="%s">%s</a>' % (url, self.name if linkContents is None else linkContents)

#___________________________________________________________________________________________________ exists
    def exists(self):
        return self._id is not None

