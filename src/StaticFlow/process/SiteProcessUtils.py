# SiteProcessUtils.py
# (C)2013
# Scott Ernst

import os

#___________________________________________________________________________________________________ SiteProcessUtils
class SiteProcessUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ getUrlFromPath
    @classmethod
    def getUrlFromPath(cls, processor, domain, path):
        if not domain:
            return u''

        isIndex = path.endswith('index.html')

        url = u'http://' + domain + u'/'
        if path.startswith(processor.sourceWebRootPath):
            url += u'/'.join(cls.getFolderParts(
                path, processor.sourceWebRootPath, includeFilename=not isIndex
            ))
        elif path.startswith(processor.targetWebRootPath):
            url += u'/'.join(cls.getFolderParts(
                path, processor.targetWebRootPath, includeFilename=not isIndex
            ))
        else:
            return u''

        if isIndex and not url.endswith(u'/'):
            url += u'/'
        return url

#___________________________________________________________________________________________________ getFolderParts
    @classmethod
    def getFolderParts(cls, path, rootPath, includeFilename =False):
        if includeFilename:
            return path[len(rootPath):].strip(os.sep).split(os.sep)
        return os.path.dirname(path)[len(rootPath):].strip(os.sep).split(os.sep)
