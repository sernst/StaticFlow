# SiteProcessUtils.py
# (C)2013
# Scott Ernst

import os
import re
import shutil
import datetime

from pyaid.file.FileUtils import FileUtils
from pyaid.json.JSON import JSON
from pyaid.string.StringUtils import StringUtils
from pyaid.system.SystemUtils import SystemUtils
from pyaid.time.TimeUtils import TimeUtils

from StaticFlow.StaticFlowEnvironment import StaticFlowEnvironment

#___________________________________________________________________________________________________ SiteProcessUtils
class SiteProcessUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _CSS_CDN_IMAGE_RE = re.compile('url\([\s]*(?P<quote>["\']*)/(?!/)')

#___________________________________________________________________________________________________ copyToCdnFolder
    @classmethod
    def copyToCdnFolder(cls, targetPath, processor, lastModified =None, headers =None):
        if processor.isLocal:
            return False

        folder = targetPath[len(processor.targetWebRootPath):].replace('\\', '/').strip('/').split('/')
        destPath = FileUtils.createPath(
            processor.targetWebRootPath, processor.cdnRootFolder, folder, isFile=True
        )
        destFolder = FileUtils.getDirectoryOf(destPath)
        if not os.path.exists(destFolder):
            os.makedirs(destFolder)
        shutil.copy(targetPath, destPath)

        if not headers:
            headers = dict()

        if 'Expires' not in headers:
            headers['Expires'] = TimeUtils.dateTimeToWebTimestamp(
                datetime.datetime.utcnow() + datetime.timedelta(days=360)
            )
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
        if not includeFilename:
            path = os.path.dirname(path)
        out = path[len(rootPath):].replace('\\', '/').strip('/')
        if not out:
            return []
        return out.split('/')

#___________________________________________________________________________________________________ compileCoffeescript
    @classmethod
    def compileCoffeescript(cls, processor, path):
        iniDirectory = os.curdir
        os.chdir(os.path.dirname(path))

        coffeePath = FileUtils.createPath(
            StaticFlowEnvironment.nodePackageManagerPath, 'coffee', isFile=True
        )
        uglifyPath = FileUtils.createPath(
            StaticFlowEnvironment.nodePackageManagerPath, 'uglifyjs', isFile=True
        )

        csPath  = FileUtils.cleanupPath(path, isFile=True)
        outPath = FileUtils.changePathRoot(
            csPath[:-6] + 'js', processor.sourceWebRootPath, processor.targetWebRootPath
        )
        FileUtils.getDirectoryOf(outPath, createIfMissing=True)

        result = SystemUtils.executeCommand(
            '%s --output "%s" --compile "%s"' % (coffeePath, os.path.dirname(outPath), csPath)
        )
        if result['code']:
            print 'ERROR: [Failed to compile]:', path
            print result
            os.chdir(iniDirectory)
            return False
        else:
            print 'COMPILED [js]:', path

        lastModified = FileUtils.getUTCModifiedDatetime(csPath)
        SiteProcessUtils.createHeaderFile(outPath, lastModified)
        if processor.isLocal:
            os.chdir(iniDirectory)
            return True

        tempOutPath = outPath + '.tmp'
        shutil.move(outPath, tempOutPath)
        result = SystemUtils.executeCommand(uglifyPath + ' ' + tempOutPath + ' > ' + outPath)
        os.remove(tempOutPath)

        if result['code']:
            print 'ERROR [Failed to compress]:', outPath
            print result
            os.chdir(iniDirectory)
            return False

        cls.copyToCdnFolder(outPath, processor, lastModified)
        print 'COMPRESSED [js]:', outPath
        return True

#___________________________________________________________________________________________________ compileCss
    @classmethod
    def compileCss(cls, processor, path):
        outPath = FileUtils.changePathRoot(
            path, processor.sourceWebRootPath, processor.targetWebRootPath
        )
        FileUtils.getDirectoryOf(outPath, createIfMissing=True)

        if processor.isLocal:
            shutil.copy(path, outPath)
            print 'COPIED [css]:', path
        else:
            iniDirectory = os.curdir
            os.chdir(os.path.dirname(path))
            result = SystemUtils.executeCommand([
                FileUtils.createPath(
                    StaticFlowEnvironment.nodePackageManagerPath, 'minify', isFile=True
                ),
                path,
                outPath
            ])
            if result['code']:
                print result['error']
                print 'ERROR [CSS compilation failure]:', path
                os.chdir(iniDirectory)
                return False

            print 'COMPRESSED [css]:', path
            os.chdir(iniDirectory)

        source = FileUtils.getContents(outPath)
        if not source:
            return False
        FileUtils.putContents(
            cls._CSS_CDN_IMAGE_RE.sub('url(\g<quote>' + processor.cdnRootUrl + '/', source),
            outPath
        )

        lastModified = FileUtils.getUTCModifiedDatetime(path)
        SiteProcessUtils.createHeaderFile(outPath, lastModified)
        cls.copyToCdnFolder(outPath, processor, lastModified)
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
