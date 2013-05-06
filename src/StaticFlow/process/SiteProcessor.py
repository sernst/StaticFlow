# SiteProcessor.py
# (C)2013
# Scott Ernst

import os
import shutil

import markdown

from pyaid.debug.Logger import Logger
from pyaid.dict.DictUtils import DictUtils
from pyaid.file.FileUtils import FileUtils
from pyaid.json.JSON import JSON
from pyaid.string.StringUtils import StringUtils
from pyaid.system.SystemUtils import SystemUtils
from pyaid.web.DomUtils import DomUtils
from pyaid.web.mako.MakoRenderer import MakoRenderer

from StaticFlow.render.MarkupProcessor import MarkupProcessor

#___________________________________________________________________________________________________ SiteProcessor
class SiteProcessor(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _SKIP_EXTENSIONS = ('.markdown', '.md', '.mdown', '.mkdn', '.mkd', '.coffee', '.blog')

    _FILE_COPY_PATHS = (
        ('js', 'ext'),
        ('img',),
        ('html',)
    )

#___________________________________________________________________________________________________ __init__
    def __init__(self, targetPath, containerPath, rootFolder ='root', **kwargs):
        """Creates a new instance of SiteProcessor."""
        self._log           = Logger(self)
        self._targetPath    = FileUtils.cleanupPath(targetPath, isDir=True) if targetPath else None
        self._containerPath = FileUtils.cleanupPath(containerPath, isDir=True)
        self._webRootPath   = FileUtils.createPath(containerPath, rootFolder, isDir=True)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: isLocal
    @property
    def isLocal(self):
        return self._targetPath is None

#___________________________________________________________________________________________________ GS: htmlDefinitionPath
    @property
    def htmlDefinitionPath(self):
        return FileUtils.createPath(self._containerPath, 'definitions', isDir=True)

#___________________________________________________________________________________________________ GS: htmlTemplatePath
    @property
    def htmlTemplatePath(self):
        return FileUtils.createPath(self._containerPath, 'templates', isDir=True)

#___________________________________________________________________________________________________ GS: targetRootPath
    @property
    def targetRootPath(self):
        if self._targetPath:
            return self._targetPath
        return FileUtils.createPath(self._webRootPath, isDir=True)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ run
    def run(self):
        if not self.isLocal:
            if not os.path.exists(self._targetPath):
                os.makedirs(self._targetPath)
            self.copyFiles()

        self.compile()
        self.generateHtml()

        if not self.isLocal:
            os.path.walk(self.targetRootPath, self._cleanupWalker, dict())

#___________________________________________________________________________________________________ compile
    def compile(self):
        args  = dict(npmPath=os.path.join(os.environ['APPDATA'], 'npm'))
        paths = ['js', 'html', 'css']

        for folder in paths:
            path = FileUtils.createPath(self._webRootPath, folder, isDir=True)
            currentPath = os.curdir
            os.path.walk(path, self._compileWalker, args)
            os.chdir(currentPath)

#___________________________________________________________________________________________________ generateHtml
    def generateHtml(self):
        sourcePath = FileUtils.createPath(self.htmlDefinitionPath, 'root', isDir=True)
        commonDefs = JSON.fromFile(
            FileUtils.createPath(self.htmlDefinitionPath, 'common.def', isFile=True)
        )

        os.path.walk(sourcePath, self._htmlDefinitionWalker, dict(
            sourcePath=sourcePath,
            commonDefs=commonDefs
        ))

#___________________________________________________________________________________________________ copyFiles
    def copyFiles(self):
        if self.isLocal:
            return False

        for item in self._FILE_COPY_PATHS:
            sourcePath = FileUtils.createPath(self._webRootPath, *item, isDir=True)
            destPath   = FileUtils.createPath(self.targetRootPath, *item, isDir=True)
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
            elif StringUtils.ends(name, ('.markdown', '.md', '.mdown', '.mkdn', '.mkd')):
                self._compileMarkdown(path, name, args)
            elif name.endswith('.css'):
                self._compileCss(path, name, args)
            elif StringUtils.ends(name, ('.sfml', '.blog')):
                self._compileMarkup(path, name, args)

#___________________________________________________________________________________________________ _compileMarkup
    def _compileMarkup(self, path, name, args):
        sourcePath = FileUtils.createPath(path, name, isFile=True)
        source     = FileUtils.getContents(sourcePath)
        if not source:
            return False

        p      = MarkupProcessor(source)
        result = p.get()
        if p.hasErrors:
            print 'RENDER ERRORS:', p.renderErrors

        targetPath = FileUtils.changePathRoot(sourcePath, self._webRootPath, self.targetRootPath)
        targetPath = targetPath.rsplit('.', 1)[0] + '.html'
        return FileUtils.putContents(result, targetPath, raiseErrors=True)

#___________________________________________________________________________________________________ _compileCss
    def _compileCss(self, path, name, args):
        if self.isLocal:
            return False

        sourcePath = FileUtils.createPath(path, name, isFile=True)
        outPath    = FileUtils.changePathRoot(sourcePath, self._webRootPath, self.targetRootPath)
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

#___________________________________________________________________________________________________ _compileMarkdown
    def _compileMarkdown(self, path, name, args):
        parts      = name.rsplit('.', 1)
        sourcePath = FileUtils.createPath(path, name, isFile=True)
        destPath   = FileUtils.createPath(path, parts[0] + '.html', isFile=True)
        if not self.isLocal:
            destPath = FileUtils.changePathRoot(destPath, self._webRootPath, self.targetRootPath)

        try:
            f = open(sourcePath, 'r+')
            source = f.read().encode('utf-8', 'ignore')
            f.close()
        except Exception, err:
            return False

        try:
            content = markdown.markdown(source)
            if not self.isLocal:
                content = DomUtils.minifyDom(content)
        except Exception, err:
            return False

        destFolder = os.path.dirname(destPath)
        if not os.path.exists(destFolder):
            os.makedirs(destFolder)

        try:
            f = open(destPath, 'w+')
            f.write(content.decode('utf-8', 'ignore'))
            f.close()
        except Exception, err:
            return False
        return True

#___________________________________________________________________________________________________ _compileCoffeescript
    def _compileCoffeescript(self, path, name, args):
        coffeePath = os.path.join(args['npmPath'], 'coffee')
        uglifyPath = os.path.join(args['npmPath'], 'uglifyjs')

        csPath     = os.path.join(path, name)
        sourcePath = csPath[:-6] + 'js'
        outPath    = sourcePath
        if not self.isLocal:
            outPath = FileUtils.changePathRoot(outPath, self._webRootPath, self.targetRootPath)

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
            defs = DictUtils.merge(
                args['commonDefs'],
                JSON.fromFile(defsPath)
            )
            sourceFolder = os.path.dirname(defsPath)[len(args['sourcePath']):].strip(os.sep).split(os.sep)
            if 'HTML' in defs:
                defs['HTML'] = defs['HTML'].replace('\\', '/').strip('/').split('/')

            filename = defs.get('FILE_NAME', None)
            if filename is None:
                filename = name.rsplit('.', 1)[0]

            if filename.endswith('.html'):
                filename = filename[:-5]

            if filename != '*':
                self._createHtmlPage(filename, sourceFolder, defs, args)
                continue

            # Create files from entries
            htmlRootPath = defs['HTML']
            htmlSourceDirectory = FileUtils.createPath(self._webRootPath, *htmlRootPath, isDir=True)
            if not os.path.exists(htmlSourceDirectory):
                print 'ERROR[Unknown path]:', htmlSourceDirectory
                continue

            for item in os.listdir(htmlSourceDirectory):
                if not item.endswith('.html'):
                    continue
                defs['HTML'] = htmlRootPath + [item]
                self._createHtmlPage(item[:-5], sourceFolder, defs, args)

#___________________________________________________________________________________________________ _createHtmlPage
    def _createHtmlPage(self, filename, sourceFolder, defs, args):
        pageVars = defs['PAGE_VARS']
        for item in pageVars['SCRIPTS']:
            if len(item) == 3:
                item.pop(2 if self.isLocal else 1)

        if 'DYNAMIC_DOMAIN' not in pageVars:
            pageVars['DYNAMIC_DOMAIN'] = '' if self.isLocal else (u'//' + defs['DYNAMIC_DOMAIN'])

        if 'HTML'in pageVars and not self.isLocal:
            pageVars['HTML'] = u'//' + defs['DYNAMIC_DOMAIN'] + pageVars['HTML']

        if 'HTML' in defs:
            htmlSourcePath = FileUtils.createPath(self._webRootPath, *defs['HTML'], isFile=True)
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
        else:
            htmlSource = u''

        data = dict(
            title=defs.get('TITLE', u''),
            description=defs.get('DESCRIPTION', u''),
            loader=u'/js/int/loader.js',
            pageVars=JSON.asString(defs.get('PAGE_VARS', dict())),
            defs=defs,
            htmlSource=htmlSource
        )

        mr = MakoRenderer(
            template=defs['TEMPLATE'],
            rootPath=self.htmlTemplatePath,
            data=data,
            minify=not self.isLocal
        )
        result = mr.render()

        try:
            outPath = FileUtils.createPath(
                self.targetRootPath, sourceFolder, filename + '.html', isFile=True
            )

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

