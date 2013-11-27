# PageManager.py
# (C)2013
# Scott Ernst

from pyaid.ArgsUtils import ArgsUtils
from pyaid.file.FileUtils import FileUtils

from StaticFlow.process.Page import Page
from StaticFlow.process.PageProcessUtils import PageProcessUtils

#___________________________________________________________________________________________________ PageManager
class PageManager(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, site):
        """ Creates a new instance of PageManager """
        self._site       = site
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

#___________________________________________________________________________________________________ query
    def query(self, attribute, **kwargs):
        if 'filter' in kwargs:
            attrCompareFilter = ArgsUtils.get('filter', None, kwargs)
            attrExistsFilter  = False
        else:
            attrCompareFilter = None
            attrExistsFilter  = ArgsUtils.get('exists', True, kwargs)

        localOnly = ArgsUtils.get('localOnly', False, kwargs)
        out       = []

        #--- FILTER
        #       Filter the pages according to the specified kwargs and the initialization above
        for page in self._pages:
            #--- EXISTS FILTER ---#
            if attrExistsFilter:
                if page.has(attribute, localOnly=localOnly):
                    out.append(page)
                continue

            #--- COMPARE FILTER ---#
            value = page.get(attribute, defaultValue=ArgsUtils.get('defaultValue', None, kwargs))
            if value == attrCompareFilter:
                out.append(page)

        #--- SORTING ---#
        reverseSort = ArgsUtils.get('reverse', False, kwargs)
        if ArgsUtils.get('dateSort', False, kwargs):
            return PageProcessUtils.sortPagesByDate(out, reverse=reverseSort)

#___________________________________________________________________________________________________ create
    def create(self, definitionPath, **kwargs):
        """ Creates a page from an absolute path to its definition file, adds it to the pages
            managed, and returns the created page. """

        page = Page(
            site=self._site,
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
        for gen in self._site.rssGenerators:
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
        path = FileUtils.createPath(self._site.targetWebRootPath, *folder, isDir=True)
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

