# PageDataManager.py
# (C)2013
# Scott Ernst

from StaticFlow.process.PageData import PageData

#___________________________________________________________________________________________________ PageDataManager
class PageDataManager(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, processor):
        """Creates a new instance of PageDataManager."""
        self._processor = processor
        self._pages     = []

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: pages
    @property
    def pages(self):
        return self._pages

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ setCurrent
    def setCurrent(self, pageData):
        if pageData not in self._pages:
            self.add(pageData)
        self._current = pageData
        return pageData

#___________________________________________________________________________________________________ create
    def create(self, **kwargs):
        page = PageData(self._processor, **kwargs)
        self.add(page)
        return page

#___________________________________________________________________________________________________ clone
    def clone(self, pageData =None, page =False, temp =False):
        return self.add(pageData.clone(page=page, temp=temp))

#___________________________________________________________________________________________________ add
    def add(self, pageData):
        """Doc..."""
        if pageData not in self._pages:
            self._pages.append(pageData)
        return pageData

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _internalMethod
    def _internalMethod(self):
        """Doc..."""
        pass

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

