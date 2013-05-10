# PageDataManager.py
# (C)2013
# Scott Ernst

import os

from pyaid.file.FileUtils import FileUtils

from StaticFlow.process.PageData import PageData

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
        page = PageData(self._processor, definitionPath=definitionPath, **kwargs)
        if page.sourcePath:
            self._pages.append(page)
        else:
            self._emptyPages.append(page)
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

#___________________________________________________________________________________________________ getPagesInFolder
    def getPagesInFolder(self, folder, dateSort =False, reverse =False, limit =0):
        res  = []
        folder = folder.replace('\\', '/').strip().strip('/').split('/')
        path = FileUtils.createPath(self._processor.targetWebRootPath, *folder, isDir=True)
        for page in self._pages:
            if page.targetPath.startswith(path):
                res.append(page)

        if dateSort:
            res = self._sortByDate(res, reverse)

        if len(res) > limit > 0:
            res = res[:limit]
        return res

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _internalMethod
    def _sortByDate(self, pages, reverse =False):
        """Doc..."""
        if len(pages) < 2:
            return pages

        out = [pages[0]]
        src = pages[1:]
        while len(src) > 0:
            page = src.pop()
            for i in range(len(out)):
                if page.date > out[i].date:
                    continue
                out.insert(i, page)
                page = None
                break
            if page:
                out.append(page)

        if reverse:
            out.reverse()
        return out

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

