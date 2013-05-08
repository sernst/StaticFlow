# SiteProcessor.py
# (C)2013
# Scott Ernst

import os
import shutil
import datetime

from pyaid.debug.Logger import Logger
from pyaid.file.FileUtils import FileUtils
from pyaid.json.JSON import JSON
from pyaid.string.StringUtils import StringUtils
from pyaid.system.SystemUtils import SystemUtils
from pyaid.web.mako.MakoRenderer import MakoRenderer

from StaticFlow.process.PageDataManager import PageDataManager

#___________________________________________________________________________________________________ SiteProcessor
class SiteProcessor(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _SKIP_EXTENSIONS = (
        '.markdown', '.md', '.mdown', '.mkdn', '.mkd', '.coffee', '.blog', '.meta', '.sfml'
    )

    _FILE_COPY_PATHS = (
        ('js', 'ext'),
        ('img',),
        ('html',)
    )

#___________________________________________________________________________________________________ __init__
    def __init__(self, targetPath, containerPath, rootFolder ='root', **kwargs):
        """Creates a new instance of SiteProcessor."""
        self._log = Logger(self)
        self._rootFolderName    = rootFolder
        self._targetWebRootPath = FileUtils.cleanupPath(targetPath, isDir=True)
        self._containerPath     = FileUtils.cleanupPath(containerPath, isDir=True)
        self._sourceWebRootPath = FileUtils.createPath(containerPath, rootFolder, isDir=True)
        self._pages             = PageDataManager(self)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: rootFolderName
    @property
    def rootFolderName(self):
        return self._rootFolderName

#___________________________________________________________________________________________________ GS: isLocal
    @property
    def isLocal(self):
        return self._targetWebRootPath is None

#___________________________________________________________________________________________________ GS: htmlDefinitionPath
    @property
    def htmlDefinitionPath(self):
        return FileUtils.createPath(self._containerPath, 'definitions', isDir=True)

#___________________________________________________________________________________________________ GS: htmlTemplatePath
    @property
    def htmlTemplatePath(self):
        return FileUtils.createPath(self._containerPath, 'templates', isDir=True)

#___________________________________________________________________________________________________ GS: targetWebRootPath
    @property
    def targetWebRootPath(self):
        if self._targetWebRootPath:
            return self._targetWebRootPath
        return self.sourceWebRootPath

#___________________________________________________________________________________________________ GS: sourceWebRootPath
    @property
    def sourceWebRootPath(self):
        return self._sourceWebRootPath

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ run
    def run(self):
        if not self.isLocal:
            if not os.path.exists(self._targetWebRootPath):
                os.makedirs(self._targetWebRootPath)
            self.copyFiles()

        self.compile()
        self.generateHtml()

        if not self.isLocal:
            os.path.walk(self.targetWebRootPath, self._cleanupWalker, dict())

#___________________________________________________________________________________________________ compile
    def compile(self):
        args  = dict(npmPath=os.path.join(os.environ['APPDATA'], 'npm'))
        paths = ['js', 'html', 'css']

        for folder in paths:
            path = FileUtils.createPath(self.sourceWebRootPath, folder, isDir=True)
            currentPath = os.curdir
            os.path.walk(path, self._compileWalker, args)
            os.chdir(currentPath)

#___________________________________________________________________________________________________ generateHtml
    def generateHtml(self):
        os.path.walk(
            FileUtils.createPath(self.htmlDefinitionPath, 'root', isDir=True),
            self._htmlDefinitionWalker,
            None
        )

#___________________________________________________________________________________________________ copyFiles
    def copyFiles(self):
        if self.isLocal:
            return False

        for item in self._FILE_COPY_PATHS:
            sourcePath = FileUtils.createPath(self.sourceWebRootPath, *item, isDir=True)
            destPath   = FileUtils.createPath(self.targetWebRootPath, *item, isDir=True)
            if not os.path.exists(destPath):
                os.makedirs(destPath)
            FileUtils.mergeCopy(sourcePath, destPath)
            print 'COPIED: %s -> %s' % (sourcePath, destPath)
        return True

#===================================================================================================
#                                                                               P R O T E C T E D

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
        outPath    = FileUtils.changePathRoot(sourcePath, self.sourceWebRootPath, self.targetWebRootPath)
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

        csPath     = os.path.join(path, name)
        sourcePath = csPath[:-6] + 'js'
        outPath    = sourcePath
        if not self.isLocal:
            outPath = FileUtils.changePathRoot(outPath, self.sourceWebRootPath, self.targetWebRootPath)

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
            if not name.endswith('.def'):
                continue

            defsPath = FileUtils.createPath(path, name, isFile=True)
            pageData = self._pages.create()
            pageData.loadPageData(defsPath, clear=True)

            sourceFolder = pageData.getFolderParts(defsPath, self.htmlDefinitionPath)[1:]
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
            htmlSourceDirectory = FileUtils.createPath(self._sourceWebRootPath, *htmlRootPath, isDir=True)
            if not os.path.exists(htmlSourceDirectory):
                print 'ERROR[Unknown path]:', htmlSourceDirectory
                continue

            for item in os.listdir(htmlSourceDirectory):
                if not item.endswith('.html'):
                    continue
                itemPageData = self._pages.clone(pageData, page=True)
                itemPageData.addItem('HTML', htmlRootPath + [item])
                self._createHtmlPage(item[:-5], sourceFolder, itemPageData, args)

#___________________________________________________________________________________________________ _createHtmlPage
    def _createHtmlPage(self, filename, sourceFolder, pageData, args):
        outPath = FileUtils.createPath(
            self.targetWebRootPath, sourceFolder, filename + '.html', isFile=True
        )
        pageData.addItem('PAGE_URL', pageData.getUrlFromPath(outPath))

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
            htmlSourcePath = FileUtils.createPath(
                self.sourceWebRootPath, *pageData.get('HTML'), isFile=True
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

            metaSourcePath = htmlSourcePath.rsplit('.')[0] + '.meta'
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

        metaDate = metadata.get('date', None)
        if metaDate:
            metaDate = metaDate.replace(u'/', u'-').strip().split(u'-')
            if len(metaDate[-1]) < 4:
                metaDate[-1] = u'20' + metaDate[-1]

            metaDate = datetime.datetime(
                year=int(metaDate[-1]),
                month=int(metaDate[0]),
                day=int(metaDate[1])
            )
            metadata['date'] = metaDate
        else:
            metadata['date'] = datetime.datetime.now()
        pageData.addItems(metadata)

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
            outDirectory = FileUtils.getDirectoryOf(outPath)
            if not os.path.exists(outDirectory):
                os.makedirs(outDirectory)

            FileUtils.putContents(result, outPath, raiseErrors=True)
            print 'CREATED:', outPath
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

