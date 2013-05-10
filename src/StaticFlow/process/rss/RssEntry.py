# RssEntry.py
# (C)2013
# Scott Ernst

#___________________________________________________________________________________________________ RssEntry
class RssEntry(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, processor, generator, pageData):
        """Creates a new instance of RssEntry."""
        self._processor = processor
        self._generator = generator
        self._pageData  = pageData

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: title
    @property
    def title(self):
        return self._pageData.get('TITLE')

#___________________________________________________________________________________________________ GS: url
    @property
    def url(self):
        return self._pageData.targetUrl

#___________________________________________________________________________________________________ GS: description
    @property
    def description(self):
        return self._pageData.get('DESCRIPTION')

#___________________________________________________________________________________________________ GS: publishedDate
    @property
    def publishedDate(self):
        return self._pageData.date.strftime(self._generator.RSS_DATE_FORMAT)

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

