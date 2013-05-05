# OEmbedRequest.py
# (C)2012
# Eric David Wills

import requests
import urllib2

from pyaid.json.JSON import JSON

#___________________________________________________________________________________________________ OEmbedRequest
class OEmbedRequest:
    """Base class for oEmbed requests."""

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ get
    @classmethod
    def get(cls, url, config):
        """Returns the embedding object for the specified URL and config."""

        try:
            req = requests.get(config['url'] + '?url=' + urllib2.quote(url) + '&format=json')
            return JSON.fromString(req.text)
        except Exception, err:
            return None

