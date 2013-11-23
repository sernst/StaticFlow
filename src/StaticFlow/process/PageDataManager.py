# PageDataManager.py
# (C)2013
# Scott Ernst

from pyaid.file.FileUtils import FileUtils

from StaticFlow.process.PageData import PageData
from StaticFlow.process.PageProcessUtils import PageProcessUtils

#___________________________________________________________________________________________________ PageDataManager
class PageDataManager(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, processor):
        """Creates a new instance of PageDataManager."""
        self._processor  = processor
        self._pages      = []
        self._emptyPages = []

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
        """ Creates a page from an absolute path to its definition file, adds it to the pages
            managed, and returns the created page. """

        page = PageData(
            processor=self._processor,
            definitionPath=definitionPath,
            **kwargs)

        if page.sourcePath:
            self._pages.append(page)
        else:
            self._emptyPages.append(page)
        return page

#___________________________________________________________________________________________________ process
    def process(self):
        """ Executes the compilation and build processing of all pages managed by this manager,
            including dynamic page generation for RSS, etc. """

        #--- COLLECT RENDER PASSES
        #       Create a list of all render passes needed to render the pages. The render pass is
        #       specified in the definition file for each page in the RENDER_PASS property with a
        #       default of 0 if not set explicitly.
        #
        #       This is a sparse list that is sorted in ascending order so that arbitrarily large
        #       numbers can be used as desired to keep passes from colliding on accident as page
        #       count grows.
        renderPasses = []
        for page in self._pages:
            if page.renderPass not in renderPasses:
                renderPasses.append(page.renderPass)
        renderPasses.sort()

        #--- COMPILE PAGES
        #       Iterate over each render pass and create the pages in that pass
        for renderPass in renderPasses:
            for page in self._pages:
                if page.renderPass == renderPass:
                    page.compile()

        #--- RSS GENERATION
        #       Adds pages to their respective RSS generators by using their references
        for gen in self._processor.rssGenerators:
            gen.populate()

        #--- PROCESS PAGES
        #       Iterate over each render pass again and create pages in that pass
        for renderPass in renderPasses:
            for page in self._pages:
                if page.renderPass == renderPass:
                    page.process()

        return True

#___________________________________________________________________________________________________ getPagesInFolder
    def getPagesInFolder(self, folder, dateSort =False, reverse =False, limit =0):
        res  = []
        folder = folder.replace('\\', '/').strip().strip('/').split('/')
        path = FileUtils.createPath(self._processor.targetWebRootPath, *folder, isDir=True)
        for page in self._pages:
            if page.targetPath.startswith(path):
                res.append(page)

        if dateSort:
            res = PageProcessUtils.sortPagesByDate(pages=res, reverse=reverse)

        if len(res) > limit > 0:
            res = res[:limit]
        return res

#___________________________________________________________________________________________________ getPageBySourcePath
    def getPageBySourcePath(self, sourcePath):
        for page in self._pages:
            if page.sourcePath == sourcePath:
                return page
        return None

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

