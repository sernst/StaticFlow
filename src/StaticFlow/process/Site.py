# Site.py
# (C)2013
# Scott Ernst

import os
import shutil
import tempfile
import time

from pyaid.ArgsUtils import ArgsUtils
from pyaid.config.ConfigsDict import ConfigsDict
from pyaid.debug.Logger import Logger
from pyaid.file.FileUtils import FileUtils
from pyaid.json.JSON import JSON
from pyaid.string.StringUtils import StringUtils
from pyaid.system.SystemUtils import SystemUtils
from pyaid.time.TimeUtils import TimeUtils

from StaticFlow.StaticFlowEnvironment import StaticFlowEnvironment
from StaticFlow.components.ConfigsDataComponent import ConfigsDataComponent
from StaticFlow.process.PageManager import PageManager
from StaticFlow.process.SiteProcessUtils import SiteProcessUtils
from StaticFlow.process.robots.RobotFileGenerator import RobotFileGenerator
from StaticFlow.process.sitemap.Sitemap import Sitemap

#___________________________________________________________________________________________________ Site
class Site(ConfigsDataComponent):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _SKIP_EXTENSIONS = (
        '.markdown', '.md', '.mdown', '.mkdn', '.mkd', '.coffee', '.blog', '.meta', '.sfml',
        '.sfmlp', '.sfmeta')

    _FILE_COPY_TYPES = ('.js', '.png', '.gif', '.jpg', '.ico', '.map')

#___________________________________________________________________________________________________ __init__
    def __init__(self, containerPath, isRemoteDeploy =False, sourceRootFolder ='src', **kwargs):
        """Creates a new instance of Site."""
        super(Site, self).__init__()

        self.errorCount     = 0
        self.warningCount   = 0
        self._staticPaths   = []

        self._logger = ArgsUtils.getLogger(self, kwargs)
        self._sourceRootFolderName = sourceRootFolder

        # NGinx root path in which all files reside
        self._containerPath = FileUtils.cleanupPath(containerPath, isDir=True)

        # Location of the source files used to create the website
        self._sourceWebRootPath = FileUtils.createPath(containerPath, sourceRootFolder, isDir=True)

        # Locations where files should be deployed. If the target root path is None, which is the
        # default value, the local web root path is used in its place.

        if isRemoteDeploy:
            self._targetWebRootPath = FileUtils.cleanupPath(
                tempfile.mkdtemp(prefix='staticFlow_'), isDir=True)
        else:
            self._targetWebRootPath = None

        self._localWebRootPath  = FileUtils.createPath(
            containerPath, ArgsUtils.get('localRootFolder', 'root', kwargs), isDir=True)

        path = FileUtils.createPath(self.sourceWebRootPath, '__site__.def', isFile=True)
        try:
            self._data.data = JSON.fromFile(path)
        except Exception, err:
            self.writeLogError(u'Unable to load site definition file: "%s"' % path)
            pass

        # Manages the data for all of the path definitions
        self._pages         = PageManager(self)
        self._sitemap       = Sitemap(self)
        self._robots        = RobotFileGenerator(self)
        self._rssGenerators = []

        # Specifies whether the website processing is local or deployed
        self._isLocal = ArgsUtils.get('isLocal', None, kwargs)

        self._cdnRootFolder = u'' if self.isLocal else \
            StaticFlowEnvironment.CDN_ROOT_PREFIX + TimeUtils.getUtcTagTimestamp()

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: faviconUrl
    @property
    def faviconUrl(self):
        path = FileUtils.createPath(self.sourceWebRootPath, 'favicon.png', isFile=True)
        if os.path.exists(path):
            return self.getSiteUrl('/favicon.png')

        path = FileUtils.createPath(self.sourceWebRootPath, 'favicon.ico', isFile=True)
        if os.path.exists(path):
            return self.getSiteUrl('/favicon.ico')
        return None

#___________________________________________________________________________________________________ GS: logger
    @property
    def logger(self):
        """ The logger used to report activity during processing """
        return self._logger

#___________________________________________________________________________________________________ GS: containerPath
    @property
    def containerPath(self):
        """The Nginx container path where all files and management resides """
        return self._containerPath

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
        """Specifies whether or not the site is deploying locally or remotely"""
        if self._isLocal is None:
            return self._targetWebRootPath is None
        return bool(self._isLocal)

#___________________________________________________________________________________________________ GS: snippetsPath
    @property
    def snippetsPath(self):
        return FileUtils.createPath(self._containerPath, 'snippets', isDir=True)

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
        domain = self.get('CDN_DOMAIN')
        if not domain:
            return u''
        return u'//' + domain + u'/' + self.cdnRootFolder

#___________________________________________________________________________________________________ GS: siteRootUrl
    @property
    def siteRootUrl(self):
        if self.isLocal:
            return u''
        domain = self.get('DOMAIN')
        if not domain:
            return u''
        return u'//' + domain

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ writeLogError
    def writeLogError(self, message, extras =None, error =None, throw =True):
        """ Formats and writes the specified error message and data to the log and if critical
            raises an exception to halt Site generation """
        self.errorCount += 1
        self.writeLog(
            header=u'ERROR',
            message=message,
            extras=extras,
            headerColor=u'#FF9999',
            error=error,
            fontSize=16,
            prefix=u'<br />')

        if throw:
            if error:
                raise error
            else:
                raise Exception, message

#___________________________________________________________________________________________________ writeLogWarning
    def writeLogWarning(self, message, extras =None):
        """ Formats and writes the specified warning message and data to the log """
        self.warningCount += 1
        self.writeLog(
            header=u'WARNING',
            message=message,
            extras=extras,
            headerColor=u'#999900',
            headerBackColor=u'#FFFF99',
            fontSize=14,
            prefix=u'<br />')

#___________________________________________________________________________________________________ writeLogSuccess
    def writeLogSuccess(self, header, message, extras =None):
        """ Formats and writes the specified success action, message, and data to the log """
        self.writeLog(
            header, message, extras, headerColor=u'#66AA66', color=u'#999999')

#___________________________________________________________________________________________________ writeLog
    def writeLog(
            self, header, message, extras =None, headerColor =None, headerBackColor =None,
            color =None, backColor =None, fontSize =None, error =None, prefix =None, suffix =None
    ):
        """ Formats the specified header and message according to the various formatting arguments
            and writes resulting message the log """

        if not headerColor:
            headerColor = u'#000000'
        if not headerBackColor:
            headerBackColor = u'#FFFFFF'
        if not color:
            color = u'#333333'
        if not backColor:
            backColor = u'#FFFFFF'
        if not fontSize:
            fontSize = 11

        # Out is formatted on separate lines because Qt text edit widget requires newlines to
        # change styles
        out = [
            u'<div style="font-size:%spx;color:%s;background-color:%s;">' % (
                fontSize, color, backColor),
            u'<span style="font-weight:bold;color:%s;background-color:%s;font-size:%spx;">' % (
                headerColor, headerBackColor, fontSize + 2),
            unicode(header) + u': ',
              u'</span>',
            unicode(message),
            u'</div>']

        if prefix:
            out.insert(0, prefix)

        #--- EXTRAS
        #       If an extras argument (dict, list, or basestring) was included, format it for
        #       friendly display
        if extras:
            out.append(u'<div>\n<ul style="font-size:%spx;color:%s;background-color:%s">' % (
                fontSize, color, backColor))

            if isinstance(extras, list):
                for item in extras:
                    out.append(u'<li>%s</li>' % item)
            elif isinstance(extras, dict):
                for n,v in extras.iteritems():
                    out.append(u'<li><span style="font-weight:bold">%s:</span> %s</li>' % (n, v))
            else:
                out.append(u'<li>%s</li>' % extras)
            out.append(u'</ul>\n<div>')

        #--- ERROR
        #       Format the error and stack trace for friendly display if present
        if error:
            out.append(u'<div style="font-size:14px;color:%s">%s</div>' % (headerColor, error))
            stack = Logger.getFormattedStackTrace(0, 3)
            out.extend([
                u'<br />',
                u'<div style="font-size:10px;color:#AAAAAA">',
                u'<span style="font-weight:bold">Thrown At:</span> %s' % stack.replace(
                    '\n', u'<br />').replace(
                    '  ', '&nbsp;&nbsp;').replace(
                    '\t', '&nbsp;&nbsp;&nbsp;&nbsp;'),
                u'</div>\n<br />'])

        if suffix:
            out.append(suffix)

        # Create final combined string and shorten known paths for compact display
        out = u'\n'.join(out).replace(
            self.sourceWebRootPath, u'/').replace(
            self.containerPath, u'//')

        self.logger.write(out)

#___________________________________________________________________________________________________ getSiteUrl
    def getSiteUrl(self, uriPath, forceHttp =False, forceHttps =False, forceDeploy =False):
        """ Creates a URL from the specified path """
        if self.isLocal and not forceDeploy:
            return uriPath

        domain = self.get('DOMAIN')
        if not domain:
            return uriPath

        protocol = u'//'
        if forceHttps:
            protocol = u'https://'
        elif forceHttp:
            protocol = u'http://'

        sep = u'' if uriPath.startswith(u'/') else u'/'
        return protocol + domain + sep + uriPath

#___________________________________________________________________________________________________ run
    def run(self):
        """ Executes the site generation process """
        try:
            if os.path.exists(self.targetWebRootPath):
                if not SystemUtils.remove(self.targetWebRootPath):
                    # In unsuccessful wait a brief period and try again in case the OS delayed
                    # the allowance for the removal because of an application conflict
                    time.sleep(5)
                    SystemUtils.remove(self.targetWebRootPath, throwError=True)
            os.makedirs(self.targetWebRootPath)
        except Exception, err:
            self.writeLogError(
                u'Unable to Remove Existing Deployment',
                error=err,
                throw=False)
            return False

        try:
            return self._runImpl()
        except Exception, err:
            self.writeLogError(u'Site Generation Failure', error=err, throw=False)
            try:
                self.cleanup()
            except Exception, err:
                pass
            return False

#___________________________________________________________________________________________________ cleanup
    def cleanup(self):
        """ Removes any non-persistent files and folders generated by this Site during the
            generation process executed by Site.run() """

        if self.isLocal or not os.path.exists(self.targetWebRootPath):
            return True

        try:
            shutil.rmtree(self.targetWebRootPath)
            return True
        except Exception, err:
            self.writeLogError(u'Site Generation Cleanup Failure', error=err)
            return False

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _runImpl
    def _runImpl(self):
        if not os.path.exists(self.targetWebRootPath):
            os.makedirs(self.targetWebRootPath)

        for staticPath in self.get('STATIC_PATHS', []):
            self._staticPaths.append(FileUtils.createPath(
                self.sourceWebRootPath,
                *staticPath.strip(u'/').split(u'/')))

        #-------------------------------------------------------------------------------------------
        # COPY FILES
        #       Copies files from the source folders to the target root folder, maintaining folder
        #       structure in the process
        FileUtils.walkPath(self.sourceWebRootPath, self._copyWalker)

        #--- COMMON FILES ---#
        copies = [
            (u'StaticFlow Javascript', 'web/js', 'js/sflow'),
            (u'StaticFlow CSS', 'web/css', 'css/sflow') ]

        for item in copies:
            source = FileUtils.createPath(
                StaticFlowEnvironment.rootResourcePath, *item[1].split('/'), isDir=True)
            target = FileUtils.createPath(
                self.targetWebRootPath, *item[2].split('/'), isDir=True)

            if os.path.exists(target):
                SystemUtils.remove(target)

            targetFolder = FileUtils.createPath(target, '..', isDir=True)
            if not os.path.exists(targetFolder):
                os.makedirs(targetFolder)

            fileList = FileUtils.mergeCopy(source, target)
            for path, data in fileList.files.iteritems():
                SiteProcessUtils.copyToCdnFolder(
                    path, self, FileUtils.getUTCModifiedDatetime(source))

            self.writeLogSuccess(u'COPIED', u'%s | %s -&gt; %s' % (
                item[0], source.rstrip(os.sep), target.rstrip(os.sep) ))

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
    def _copyWalker(self, walkData):
        staticFolder = False
        for folder in self._staticPaths:
            path = FileUtils.cleanupPath(walkData.folder, isDir=True)
            folder = FileUtils.cleanupPath(folder, isDir=True)
            if path == folder or FileUtils.isInFolder(path, folder):
                staticFolder = True
                break

        copiedNames = []
        for item in walkData.names:
            if not staticFolder and not StringUtils.ends(item, self._FILE_COPY_TYPES):
                continue

            sourcePath = FileUtils.createPath(walkData.folder, item)
            if os.path.isdir(sourcePath):
                continue

            destPath = FileUtils.changePathRoot(
                sourcePath, self.sourceWebRootPath, self.targetWebRootPath)

            try:
                FileUtils.getDirectoryOf(destPath, createIfMissing=True)
                shutil.copy(sourcePath, destPath)

                lastModified = FileUtils.getUTCModifiedDatetime(sourcePath)
                SiteProcessUtils.createHeaderFile(destPath, lastModified)
                SiteProcessUtils.copyToCdnFolder(destPath, self, lastModified)
                copiedNames.append(item)
            except Exception, err:
                self.writeLogError(u'Unable to copy file', error=err, extras={
                    'SOURCE':sourcePath,
                    'TARGET':destPath })
                return

        #--- LOG COPIES ---#
        if copiedNames:
            self.writeLogSuccess(u'COPIED', u'%s: %s' % (
                walkData.folder.rstrip(os.sep),
                u', '.join(copiedNames)))

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
        # If a folder definition is found, use it to populate the directory with any missing
        # definition files before proceeding
        if '__folder__.def' in names:
            self._processFolderDefinitions(
                FileUtils.createPath(path, '__folder__.def', isFile=True))
            names = os.listdir(path)

        # For each definition file in the directory create page data for processing
        for name in names:
            if name.endswith('.def') and not name.startswith('__'):
                self._pages.create(FileUtils.createPath(path, name, isFile=True))

#___________________________________________________________________________________________________ _processFolderDefinitions
    def _processFolderDefinitions(self, path):
        cd        = ConfigsDict(JSON.fromFile(path))
        directory = FileUtils.getDirectoryOf(path)

        for item in os.listdir(directory):
            # Only find content source file types
            if not StringUtils.ends(item, ('.sfml', '.html')):
                continue

            # Skip files that already have a definitions file
            itemPath     = FileUtils.createPath(directory, item, isFile=True)
            itemDefsPath = itemPath.rsplit('.', 1)[0] + '.def'
            if os.path.exists(itemDefsPath):
                continue

            test = SiteProcessUtils.testFileFilter(
                itemPath,
                cd.get(('FOLDER', 'EXTENSION_FILTER')),
                cd.get(('FOLDER', 'NAME_FILTER')))
            if not test:
                continue

            JSON.toFile(itemDefsPath, dict(), pretty=True)
        return True

#___________________________________________________________________________________________________ _cleanupWalker
    def _cleanupWalker(self, args, path, names):
        for name in names:
            itemPath = FileUtils.createPath(path, name)
            if not os.path.isfile(itemPath) or not StringUtils.ends(name, self._SKIP_EXTENSIONS):
                continue
            os.remove(itemPath)

#___________________________________________________________________________________________________ _writeGoogleFiles
    def _writeGoogleFiles(self):
        vid = self.get(('GOOGLE', 'SITE_VERIFY_ID'))
        if not vid:
            return False

        if not vid.endswith('.html'):
            vid += '.html'

        path = FileUtils.createPath(self.targetWebRootPath, vid, isFile=True)
        FileUtils.putContents(u'google-site-verification: ' + vid, path)
        SiteProcessUtils.createHeaderFile(path, None)
        return True


