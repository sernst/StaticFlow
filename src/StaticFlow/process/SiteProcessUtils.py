# SiteProcessUtils.py
# (C)2013
# Scott Ernst

import os
import re
import shutil
import datetime

from pyaid.OsUtils import OsUtils
from pyaid.file.FileUtils import FileUtils
from pyaid.json.JSON import JSON
from pyaid.string.StringUtils import StringUtils
from pyaid.system.SystemUtils import SystemUtils
from pyaid.time.TimeUtils import TimeUtils

from StaticFlow.StaticFlowEnvironment import StaticFlowEnvironment
from StaticFlow.components.LocalImage import LocalImage

#___________________________________________________________________________________________________ SiteProcessUtils
class SiteProcessUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _CSS_CDN_IMAGE_RE = re.compile('url\([\s]*(?P<quote>["\']*)/(?!/)')

#___________________________________________________________________________________________________ createFavicon
    @classmethod
    def createFavicon(cls, site):
        sourceFilename = site.get('FAVICON_SOURCE')
        if not sourceFilename:
            return True

        sourcePath = FileUtils.createPath(
            site.sourceWebRootPath,
            sourceFilename.strip('/'), isFile=True)

        if not os.path.exists(sourcePath):
            site.writeLogWarning(u'Favicon source file not found "%s"' % sourceFilename)
            return False

        img = LocalImage(sourcePath, site)
        if not img.exists:
            return False

        targetPath = FileUtils.createPath(site.targetWebRootPath, 'favicon.ico')

        cmd = ['convert', '"%s"' % sourcePath, '-bordercolor', 'white', '-border', '0',
          '\( -clone 0 -resize 16x16 \)']

        if img.width >= 32:
          cmd.append('\( -clone 0 -resize 32x32 \)')
        if img.width >= 48:
          cmd.append('\( -clone 0 -resize 48x48 \)')
        if img.width >= 64:
          cmd.append('\( -clone 0 -resize 64x64 \)')

        cmd.extend(['-delete', '0', '-alpha', 'off', '-colors', '256', '"%s"' % targetPath])

        result = SystemUtils.executeCommand(cmd)
        if result['code']:
            site.writeLogWarning(u'Unable to create favicon.ico file')
            return False

        return True

#___________________________________________________________________________________________________ copyToCdnFolder
    @classmethod
    def copyToCdnFolder(cls, targetPath, processor, lastModified =None, headers =None):
        if processor.isLocal:
            return False

        folder = targetPath[len(processor.targetWebRootPath):].replace('\\', '/').strip('/').split('/')
        destPath = FileUtils.createPath(
            processor.targetWebRootPath, processor.cdnRootFolder, folder, isFile=True)
        destFolder = FileUtils.getDirectoryOf(destPath)
        if not os.path.exists(destFolder):
            os.makedirs(destFolder)
        shutil.copy(targetPath, destPath)

        if not headers:
            headers = dict()

        if 'Expires' not in headers:
            headers['Expires'] = TimeUtils.dateTimeToWebTimestamp(
                datetime.datetime.utcnow() + datetime.timedelta(days=360))
        cls.createHeaderFile(destPath, lastModified=lastModified, headers=headers)
        return True

#___________________________________________________________________________________________________ createHeaderFile
    @classmethod
    def createHeaderFile(cls, path, lastModified =None, headers =None):
        if not lastModified:
            lastModified = datetime.datetime.utcnow()

        if isinstance(lastModified, tuple) or isinstance(lastModified, list):
            modTime = lastModified[0]
            for newTime in lastModified[1:]:
                if newTime and newTime > modTime:
                    modTime = newTime
            lastModified = modTime

        if not headers:
            headers = dict()
        headers['_LAST_MODIFIED'] = TimeUtils.dateTimeToWebTimestamp(lastModified)

        return JSON.toFile(path + '.headers', headers)

#___________________________________________________________________________________________________ getUrlFromPath
    @classmethod
    def getUrlFromPath(cls, processor, domain, path):
        if not domain:
            return u''

        isIndex = path.endswith('index.html')

        url = u'http://' + domain + u'/'
        if path.startswith(processor.sourceWebRootPath):
            url += u'/'.join(cls.getFolderParts(
                path, processor.sourceWebRootPath, includeFilename=not isIndex))
        elif path.startswith(processor.targetWebRootPath):
            url += u'/'.join(cls.getFolderParts(
                path, processor.targetWebRootPath, includeFilename=not isIndex))
        else:
            return u''

        url = url.replace(u'\\', u'/')
        if isIndex and not url.endswith(u'/'):
            url += u'/'
        return url

#___________________________________________________________________________________________________ getFolderParts
    @classmethod
    def getFolderParts(cls, path, rootPath, includeFilename =False):
        if not includeFilename:
            path = os.path.dirname(path)
        out = path[len(rootPath):].replace('\\', '/').strip('/')
        if not out:
            return []
        return out.split('/')

#___________________________________________________________________________________________________ compileCoffeescriptFile
    @classmethod
    def compileCoffeescriptFile(cls, source, destFolder, minify =True):
        iniDirectory = os.curdir
        os.chdir(os.path.dirname(source))

        cmd = cls.modifyNodeCommand([
            StaticFlowEnvironment.getNodeCommandAbsPath('coffee'),
            '--output', '"%s"' % FileUtils.stripTail(destFolder),
            '--compile', '"%s"' % source ])

        result = SystemUtils.executeCommand(cmd)
        if not minify or result['code']:
            os.chdir(iniDirectory)
            return result

        name = os.path.splitext(os.path.basename(source))[0] + '.js'
        dest = FileUtils.createPath(destFolder, name, isFile=True)

        tempOutPath = dest + '.tmp'
        shutil.move(dest, tempOutPath)

        cmd = cls.modifyNodeCommand([
            StaticFlowEnvironment.getNodeCommandAbsPath('uglifyjs'),
            '"%s"' % tempOutPath,
            '>',
            '"%s"' % dest ])

        result = SystemUtils.executeCommand(cmd)
        os.remove(tempOutPath)
        os.chdir(iniDirectory)
        return result

#___________________________________________________________________________________________________ compileCoffeescript
    @classmethod
    def compileCoffeescript(cls, site, path):
        csPath  = FileUtils.cleanupPath(path, isFile=True)
        outPath = FileUtils.changePathRoot(
            csPath[:-6] + 'js', site.sourceWebRootPath, site.targetWebRootPath)
        FileUtils.getDirectoryOf(outPath, createIfMissing=True)

        outDir = os.path.dirname(outPath)
        result = cls.compileCoffeescriptFile(csPath, outDir, minify=not site.isLocal)
        if result['code']:
            site.writeLogError(u'Failed to compile: "%s"' % unicode(path))
            print result
            return False
        else:
            site.writeLogSuccess(u'COMPILED', unicode(path))

        lastModified = FileUtils.getUTCModifiedDatetime(csPath)
        SiteProcessUtils.createHeaderFile(outPath, lastModified)
        if site.isLocal:
            return True

        cls.copyToCdnFolder(outPath, site, lastModified)
        site.writeLogSuccess(u'COMPRESSED', unicode(outPath))

        return True

#___________________________________________________________________________________________________ compileCss
    @classmethod
    def compileCss(cls, site, path):
        outPath = FileUtils.changePathRoot(
            path, site.sourceWebRootPath, site.targetWebRootPath)
        FileUtils.getDirectoryOf(outPath, createIfMissing=True)

        if site.isLocal:
            shutil.copy(path, outPath)
            site.writeLogSuccess(u'COPIED', unicode(path))
        else:
            cmd = cls.modifyNodeCommand([
                FileUtils.createPath(
                    StaticFlowEnvironment.nodePackageManagerPath, 'minify', isFile=True),
                '"%s"' % path,
                '"%s"' % outPath])

            iniDirectory = os.curdir
            os.chdir(os.path.dirname(path))
            result = SystemUtils.executeCommand(cmd)
            if result['code']:
                site.logger.write(unicode(result['error']))
                site.writeLogError(u'CSS compilation failure:', extras={
                    'PATH':path,
                    'ERROR':result['error']})
                os.chdir(iniDirectory)
                return False

            site.writeLogSuccess(u'COMPRESSED', unicode(path))
            os.chdir(iniDirectory)

        source = FileUtils.getContents(outPath)
        if not source:
            return False
        FileUtils.putContents(
            cls._CSS_CDN_IMAGE_RE.sub('url(\g<quote>' + site.cdnRootUrl + '/', source),
            outPath)

        lastModified = FileUtils.getUTCModifiedDatetime(path)
        SiteProcessUtils.createHeaderFile(outPath, lastModified)
        cls.copyToCdnFolder(outPath, site, lastModified)
        return True

#___________________________________________________________________________________________________ testFileFilter
    @classmethod
    def testFileFilter(cls, path, extensionFilter =None, nameFilter =None):
        # Skip extensions not included in the filter if the filter exists
        if extensionFilter and not StringUtils.ends(path, extensionFilter):
            print 'FOLDER[skipped extension]:', path
            return False

        # Skip names not included in the filter if the filter exists
        if nameFilter and isinstance(nameFilter, basestring):
            nameFilter = re.compile(nameFilter)

        if nameFilter and not nameFilter.search(os.path.basename(path)):
            print 'FOLDER[skipped name]:', path
            return False

        return True

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________
    @classmethod
    def modifyNodeCommand(cls, cmd):
        if OsUtils.isMac():
            return [
                'export',
                'PATH=%s:$PATH;' % StaticFlowEnvironment.nodePackageManagerPath] + cmd
        return cmd
