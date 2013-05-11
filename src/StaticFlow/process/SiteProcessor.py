# SiteProcessor.py
# (C)2013
# Scott Ernst

import os
import shutil
import tempfile

from pyaid.ArgsUtils import ArgsUtils
from pyaid.config.ConfigsDict import ConfigsDict
from pyaid.debug.Logger import Logger
from pyaid.file.FileUtils import FileUtils
from pyaid.json.JSON import JSON
from pyaid.string.StringUtils import StringUtils
from pyaid.time.TimeUtils import TimeUtils

from StaticFlow.process.PageDataManager import PageDataManager
from StaticFlow.process.SiteProcessUtils import SiteProcessUtils
from StaticFlow.process.robots.RobotFileGenerator import RobotFileGenerator
from StaticFlow.process.sitemap.SitemapManager import SitemapManager

#___________________________________________________________________________________________________ SiteProcessor
class SiteProcessor(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _GLOBAL_DEFS = ('__site__.def', '__robots__.def')

    _SKIP_EXTENSIONS = (
        '.markdown', '.md', '.mdown', '.mkdn', '.mkd', '.coffee', '.blog', '.meta', '.sfml',
        '.sfmlp', '.sfmeta'
    )

    _FILE_COPY_TYPES = ('.js', '.png', '.gif', '.jpg', '.ico')

#___________________________________________________________________________________________________ __init__
    def __init__(self, containerPath, isRemoteDeploy =False, sourceRootFolder ='src', **kwargs):
        """Creates a new instance of SiteProcessor."""
        self._log = Logger(self, printOut=True)
        self._sourceRootFolderName = sourceRootFolder

        # NGinx root path in which all files reside
        self._containerPath = FileUtils.cleanupPath(containerPath, isDir=True)

        # Location of the source files used to create the website
        self._sourceWebRootPath = FileUtils.createPath(containerPath, sourceRootFolder, isDir=True)

        # Locations where files should be deployed. If the target root path is None, which is the
        # default value, the local web root path is used in its place.

        if isRemoteDeploy:
            self._targetWebRootPath = FileUtils.cleanupPath(
                tempfile.mkdtemp(prefix='staticFlow_'), isDir=True
            )
        else:
            self._targetWebRootPath = None

        self._localWebRootPath  = FileUtils.createPath(
            containerPath, ArgsUtils.get('localRootFolder', 'root', kwargs), isDir=True
        )

        try:
            self._siteData = ConfigsDict(JSON.fromFile(
                FileUtils.createPath(self.sourceWebRootPath, '__site__.def', isFile=True)
            ))
        except Exception, err:
            self._siteData = dict()

        # Manages the data for all of the path definitions
        self._pages         = PageDataManager(self)
        self._sitemap       = SitemapManager(self)
        self._robots        = RobotFileGenerator(self)
        self._rssGenerators = []

        # Specifies whether the website processing is local or deployed. In the deployed case
        self._isLocal = ArgsUtils.get('isLocal', None, kwargs)

        self._cdnRootFolder = '' if self.isLocal else TimeUtils.getUtcTagTimestamp()

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: sourceRootFolderName
    @property
    def sourceRootFolderName(self):
        """Folder name within the container path where the source files (definitions, etc.) reside"""
        return self._sourceRootFolderName

#___________________________________________________________________________________________________ GS: sourceWebRootPath
    @property
    def sourceWebRootPath(self):
        """Absolute path to the source folder where the source files (definitions, etc.) reside"""
        return self._sourceWebRootPath

#___________________________________________________________________________________________________ GS: isLocal
    @property
    def isLocal(self):
        """Specifies whether or not the processor is deploying locally or remotely"""
        if self._isLocal is None:
            return self._targetWebRootPath is None
        return bool(self._isLocal)

#___________________________________________________________________________________________________ GS: htmlTemplatePath
    @property
    def htmlTemplatePath(self):
        """Root Mako template path"""
        return FileUtils.createPath(self._containerPath, 'templates', isDir=True)

#___________________________________________________________________________________________________ GS: targetWebRootPath
    @property
    def targetWebRootPath(self):
        """Web root path where processed files should be deployed"""
        if self._targetWebRootPath:
            return self._targetWebRootPath
        return self._localWebRootPath

#___________________________________________________________________________________________________ GS: siteData
    @property
    def siteData(self):
        return self._siteData

#___________________________________________________________________________________________________ GS: sitemap
    @property
    def sitemap(self):
        return self._sitemap

#___________________________________________________________________________________________________ GS: pages
    @property
    def pages(self):
        return self._pages

#___________________________________________________________________________________________________ GS: rssGenerators
    @property
    def rssGenerators(self):
        return self._rssGenerators

#___________________________________________________________________________________________________ GS: cdnRootFolder
    @property
    def cdnRootFolder(self):
        return self._cdnRootFolder

#___________________________________________________________________________________________________ GS: cdnRootUrl
    @property
    def cdnRootUrl(self):
        if self.isLocal:
            return u''
        domain = self.siteData.get('CDN_DOMAIN')
        if not domain:
            return u''
        return u'//' + domain + u'/' + self.cdnRootFolder

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ run
    def run(self):
        try:
            self._runImpl()
        except Exception, err:
            self.cleanup()
            raise
        return True

#___________________________________________________________________________________________________ cleanup
    def cleanup(self):
        if self.isLocal or not os.path.exists(self.targetWebRootPath):
            return False
        try:
            shutil.rmtree(self.targetWebRootPath)
        except Exception, err:
            raise
        return True

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _runImpl
    def _runImpl(self):
        if not os.path.exists(self.targetWebRootPath):
            os.makedirs(self.targetWebRootPath)

        #-------------------------------------------------------------------------------------------
        # COPY FILES
        #       Copies files from the source folders to the target root folder, maintaining folder
        #       structure in the process
        os.path.walk(self.sourceWebRootPath, self._copyWalker, None)

        #-------------------------------------------------------------------------------------------
        # COMPILE
        #       Compiles source files to the target root folder
        currentPath = os.curdir
        os.path.walk(self.sourceWebRootPath, self._compileWalker, None)
        os.chdir(currentPath)

        #-------------------------------------------------------------------------------------------
        # CREATE PAGE DEFS
        #       Creates the page data files that define the pages to be generated
        os.path.walk(self.sourceWebRootPath, self._htmlDefinitionWalker, None)
        self._pages.process()

        self._sitemap.write()
        self._robots.write()

        for rssGenerator in self._rssGenerators:
            rssGenerator.write()

        self._writeGoogleFiles()

        #-------------------------------------------------------------------------------------------
        # CLEANUP
        #       Removes temporary and excluded file types from the target root folder
        os.path.walk(self.targetWebRootPath, self._cleanupWalker, dict())

        return True

#___________________________________________________________________________________________________ _copyWalker
    def _copyWalker(self, args, path, names):
        for item in names:
            if not StringUtils.ends(item, self._FILE_COPY_TYPES):
                continue

            sourcePath = FileUtils.createPath(path, item)
            destPath   = FileUtils.changePathRoot(
                sourcePath, self.sourceWebRootPath, self.targetWebRootPath
            )
            FileUtils.getDirectoryOf(destPath, createIfMissing=True)
            shutil.copy(sourcePath, destPath)

            lastModified = FileUtils.getUTCModifiedDatetime(sourcePath)
            SiteProcessUtils.createHeaderFile(destPath, lastModified)
            SiteProcessUtils.copyToCdnFolder(destPath, self, lastModified)

            self._log.write('COPIED: %s -> %s' % (sourcePath, destPath))

#___________________________________________________________________________________________________ _compileWalker
    def _compileWalker(self, args, path, names):
        for name in names:
            namePath = FileUtils.createPath(path, name, isFile=True)
            if name.endswith('.coffee'):
                SiteProcessUtils.compileCoffeescript(self, namePath)
            elif name.endswith('.css'):
                SiteProcessUtils.compileCss(self, namePath)

#___________________________________________________________________________________________________ _htmlDefinitionWalker
    def _htmlDefinitionWalker(self, args, path, names):
        for name in names:
            if name.endswith('.def') and name not in self._GLOBAL_DEFS:
                self._pages.create(FileUtils.createPath(path, name, isFile=True))

#___________________________________________________________________________________________________ _cleanupWalker
    def _cleanupWalker(self, args, path, names):
        for name in names:
            itemPath = FileUtils.createPath(path, name)
            if not os.path.isfile(itemPath) or not StringUtils.ends(name, self._SKIP_EXTENSIONS):
                continue
            os.remove(itemPath)

#___________________________________________________________________________________________________ _writeGoogleFiles
    def _writeGoogleFiles(self):
        vid = self.siteData.get(('GOOGLE', 'SITE_VERIFY_ID'))
        if not vid:
            return False

        if not vid.endswith('.html'):
            vid += '.html'

        path = FileUtils.createPath(self.targetWebRootPath, vid, isFile=True)
        FileUtils.putContents(u'google-site-verification: ' + vid, path)
        SiteProcessUtils.createHeaderFile(path, None)
        return True

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

