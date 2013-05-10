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

#___________________________________________________________________________________________________ create
    def create(self, definitionPath, **kwargs):
        page = PageData(self._processor, definitionPath=definitionPath, **kwargs)
        self._pages.append(page)
        return page

#___________________________________________________________________________________________________ process
    def process(self):
        """Doc..."""
        for page in self._pages:
            page.compile()

        # Adds pages to their respective RSS generators
        for page in self._pages:
            if page.rssGenerator:
                continue
            for gen in self._processor.rssGenerators:
                gen.addEntry(page)

        for page in self._pages:
            page.process()
        return True

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

