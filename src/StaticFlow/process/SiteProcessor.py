# SiteProcessor.py
# (C)2013
# Scott Ernst

import os
import shutil
import datetime

from pyaid.ArgsUtils import ArgsUtils
from pyaid.debug.Logger import Logger
from pyaid.dict.DictUtils import DictUtils
from pyaid.file.FileUtils import FileUtils
from pyaid.json.JSON import JSON
from pyaid.string.StringUtils import StringUtils
from pyaid.system.SystemUtils import SystemUtils
from pyaid.web.mako.MakoRenderer import MakoRenderer

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

    _FILE_COPY_TYPES = ('.js', '.css', '.png', '.gif', '.jpg', '.ico')

#___________________________________________________________________________________________________ __init__
    def __init__(self, targetPath, containerPath,  sourceRootFolder ='src', **kwargs):
        """Creates a new instance of SiteProcessor."""
        self._log = Logger(self)
        self._sourceRootFolderName = sourceRootFolder

        # NGinx root path in which all files reside
        self._containerPath     = FileUtils.cleanupPath(containerPath, isDir=True)

        # Location of the source files used to create the website
        self._sourceWebRootPath = FileUtils.createPath(containerPath, sourceRootFolder, isDir=True)

        # Locations where files should be deployed. If the target root path is None, which is the
        # default value, the local web root path is used in its place.
        self._targetWebRootPath = FileUtils.cleanupPath(targetPath, isDir=True)
        self._localWebRootPath  = FileUtils.createPath(
            containerPath, ArgsUtils.get('localRootFolder', 'root', kwargs), isDir=True
        )

        try:
            self._siteData = DictUtils.lowerDictKeys(JSON.fromFile(
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

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getSiteData
    def getSiteData(self, key, defaultValue =None):
        key = key.lower()
        if key in self._siteData:
            return self._siteData[key]
        return defaultValue

#___________________________________________________________________________________________________ run
    def run(self):
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
        args = dict(npmPath=os.path.join(os.environ['APPDATA'], 'npm'))
        currentPath = os.curdir
        os.path.walk(self.sourceWebRootPath, self._compileWalker, args)
        os.chdir(currentPath)

        #-------------------------------------------------------------------------------------------
        # GENERATE FROM DEFS
        #       Renders HTML files from the source definition files
        os.path.walk(self.sourceWebRootPath, self._htmlDefinitionWalker, None)

        self._sitemap.write()
        self._robots.write()

        for rssGenerator in self._rssGenerators:
            rssGenerator.write()

        #-------------------------------------------------------------------------------------------
        # CLEANUP
        #       Removes temporary and excluded file types from the target root folder
        os.path.walk(self.targetWebRootPath, self._cleanupWalker, dict())

        return True

#===================================================================================================
#                                                                               P R O T E C T E D

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
            print 'COPIED: %s -> %s' % (sourcePath, destPath)

#___________________________________________________________________________________________________ _compileWalker
    def _compileWalker(self, args, path, names):
        os.chdir(path)

        for name in names:
            if name.endswith('.coffee'):
                self._compileCoffeescript(path, name, args)
            elif name.endswith('.css'):
                self._compileCss(path, name, args)
            elif name.endswith('.sfml'):
                self._pages.create(sourcePath=FileUtils.createPath(path, name, isFile=True))

#___________________________________________________________________________________________________ _compileCss
    def _compileCss(self, path, name, args):
        if self.isLocal:
            return False

        sourcePath = FileUtils.createPath(path, name, isFile=True)
        outPath = FileUtils.changePathRoot(
            sourcePath, self.sourceWebRootPath, self.targetWebRootPath
        )
        FileUtils.getDirectoryOf(outPath, createIfMissing=True)

        result = SystemUtils.executeCommand([
            FileUtils.createPath(args['npmPath'], 'minify', isFile=True),
            sourcePath,
            outPath
        ])
        if result['code']:
            print result['error']
            print 'ERROR: CSS compilation failure'
            return False
        print 'COMPRESSED:', name
        return True

#___________________________________________________________________________________________________ _compileCoffeescript
    def _compileCoffeescript(self, path, name, args):
        coffeePath = os.path.join(args['npmPath'], 'coffee')
        uglifyPath = os.path.join(args['npmPath'], 'uglifyjs')

        csPath  = os.path.join(path, name)
        outPath = FileUtils.changePathRoot(
            csPath[:-6] + 'js', self.sourceWebRootPath, self.targetWebRootPath
        )
        FileUtils.getDirectoryOf(outPath, createIfMissing=True)

        result = SystemUtils.executeCommand(
            '%s --output "%s" --compile "%s"' % (coffeePath, os.path.dirname(outPath), csPath)
        )
        if result['code']:
            print 'FAILED >> Unable to compile:', name
            print result
            return False
        else:
            print 'COMPILED:', name

        if self.isLocal:
            return True

        tempOutPath = outPath + '.tmp'
        shutil.move(outPath, tempOutPath)
        result = SystemUtils.executeCommand(uglifyPath + ' ' + tempOutPath + ' > ' + outPath)
        os.remove(tempOutPath)

        if result['code']:
            print 'FAILED >> Unable to compress:', name
            print result
            return False
        else:
            print 'COMPRESSED:', name
        return True

#___________________________________________________________________________________________________ _htmlDefinitionWalker
    def _htmlDefinitionWalker(self, args, path, names):
        for name in names:
            if name in self._GLOBAL_DEFS or not name.endswith('.def'):
                continue

            defsPath = FileUtils.createPath(path, name, isFile=True)
            pageData = self._pages.create()
            pageData.loadPageData(defsPath, clear=True)

            sourceFolder = SiteProcessUtils.getFolderParts(defsPath, self.sourceWebRootPath)
            if pageData.has('HTML'):
                pageData.addItem(
                    'HTML', pageData.get('HTML').replace('\\', '/').strip('/').split('/')
                )

            filename = pageData.get('FILE_NAME')
            if filename is None:
                filename = name.rsplit('.', 1)[0]

            if filename.endswith('.html'):
                filename = filename[:-5]

            if filename != '*':
                self._createHtmlPage(filename, sourceFolder, pageData, args)
                continue

            # Create files from entries
            htmlRootPath = pageData.get('HTML')
            htmlSourceDirectory = FileUtils.createPath(
                self.targetWebRootPath, *htmlRootPath, isDir=True
            )

            for item in os.listdir(htmlSourceDirectory):
                if not item.endswith('.sfmlp'):
                    continue
                itemPageData = self._pages.clone(pageData, page=True)
                itemPageData.addItem('HTML', htmlRootPath + [item])
                self._createHtmlPage(item[:-6], sourceFolder, itemPageData, args)

#___________________________________________________________________________________________________ _createHtmlPage
    def _createHtmlPage(self, filename, sourceFolder, pageData, args):
        pageData.targetPath = FileUtils.createPath(
            self.targetWebRootPath, sourceFolder, filename + '.html', isFile=True
        )

        pageVars = pageData.getMerged('PAGE_VARS', dict())
        pageData.addItem('PAGE_VARS', pageVars)
        for item in pageVars['SCRIPTS']:
            if len(item) == 3:
                item.pop(2 if self.isLocal else 1)

        if 'DYNAMIC_DOMAIN' not in pageVars:
            pageVars['DYNAMIC_DOMAIN'] = '' if self.isLocal else (
                u'//' + pageData.get('DYNAMIC_DOMAIN')
            )

        if 'HTML'in pageVars and not self.isLocal:
            pageVars['HTML'] = u'//' + pageData.get('DYNAMIC_DOMAIN') + pageVars['HTML']

        if pageData.has('HTML'):
            try:
                htmlSourceType = pageData.get('HTML')[-1].rsplit('.', 1)[0].lower()
            except Exception, err:
                htmlSourceType = 'html'

            htmlSourcePath = FileUtils.createPath(
                self.sourceWebRootPath,
                *pageData.get('HTML'),
                isFile=True
            )
            if not os.path.exists(htmlSourcePath) and htmlSourceType != 'html':
                htmlSourcePath = FileUtils.createPath(
                    self.targetWebRootPath,
                    *pageData.get('HTML'),
                    isFile=True
                )

            if not os.path.exists(htmlSourcePath):
                print 'ERROR[Missing HTML source file]:', htmlSourcePath
                htmlSource = u''
            else:
                try:
                    htmlSource = FileUtils.getContents(htmlSourcePath, raiseErrors=True)
                except Exception, err:
                    print 'ERROR[Failed to read HTML file]:', htmlSourcePath
                    print err
                    htmlSource = u''

            metaSourcePath = htmlSourcePath.rsplit('.')[0] + '.sfmeta'
            if os.path.exists(metaSourcePath):
                try:
                    metadata = JSON.fromFile(metaSourcePath)
                except Exception, err:
                    metadata = dict()
            else:
                metadata = dict()
        else:
            htmlSource = u''
            metadata   = dict()

        metaDate = ArgsUtils.extract('date', None, metadata)
        pageData.addItems(metadata)
        if metaDate:
            metaDate = metaDate.replace(u'/', u'-').strip().split(u'-')
            if len(metaDate[-1]) < 4:
                metaDate[-1] = u'20' + metaDate[-1]

            pageData.date = datetime.datetime(
                year=int(metaDate[-1]),
                month=int(metaDate[0]),
                day=int(metaDate[1])
            )
        elif not pageData.date:
            pageData.date = datetime.datetime.now()

        data = dict(
            loader=u'/js/int/loader.js',
            pageVars=JSON.asString(pageVars),
            pageData=pageData,
            htmlSource=htmlSource,
            metadata=metadata
        )

        mr = MakoRenderer(
            template=pageData.get('TEMPLATE'),
            rootPath=self.htmlTemplatePath,
            data=data,
            minify=not self.isLocal
        )
        result = mr.render()

        if not mr.success:
            print mr.errorMessage

        try:
            outDirectory = FileUtils.getDirectoryOf(pageData.targetPath)
            if not os.path.exists(outDirectory):
                os.makedirs(outDirectory)

            FileUtils.putContents(result, pageData.targetPath, raiseErrors=True)

            # Add the page to the sitemap
            self._sitemap.add(pageData)

            print 'CREATED:', pageData.targetPath, ' -> ', pageData.targetUrl
        except Exception, err:
            print err

#___________________________________________________________________________________________________ _cleanupWalker
    def _cleanupWalker(self, args, path, names):
        for name in names:
            itemPath = FileUtils.createPath(path, name)
            if not os.path.isfile(itemPath) or not StringUtils.ends(name, self._SKIP_EXTENSIONS):
                continue
            os.remove(itemPath)

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

