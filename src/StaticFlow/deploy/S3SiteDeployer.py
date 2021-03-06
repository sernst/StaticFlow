# S3SiteDeployer.py
# (C)2013
# Scott Ernst

import os

from pyaid.ArgsUtils import ArgsUtils
from pyaid.dict.DictUtils import DictUtils
from pyaid.file.FileUtils import FileUtils
from pyaid.json.JSON import JSON
from pyaid.string.StringUtils import StringUtils
from pyaid.time.TimeUtils import TimeUtils

from StaticFlow.StaticFlowEnvironment import StaticFlowEnvironment
from StaticFlow.deploy.S3Bucket import S3Bucket

#___________________________________________________________________________________________________ S3SiteDeployer
class S3SiteDeployer(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _SKIP_EXTENSIONS = ('.headers', '.def')

    _STRING_EXTENSIONS = ('.html', '.js', '.css', '.xml', '.json', '.txt')

    _FORCE_HTML_EXTENSIONS = ('.html', '.xml', '.txt')

#___________________________________________________________________________________________________ __init__
    def __init__(self, localRootPath, sourceWebRootPath, forceHtml =False, forceAll =False, **kwargs):
        """Creates a new instance of S3SiteDeployer."""
        self._logger            = ArgsUtils.getLogger(self, kwargs)
        self._localRootPath     = FileUtils.cleanupPath(localRootPath, isDir=True)
        self._sourceWebRootPath = FileUtils.cleanupPath(sourceWebRootPath, isDir=True)
        self._forceHtml         = forceHtml
        self._forceAll          = forceAll
        self._cdnRootPath       = None

        try:
            siteData = JSON.fromFile(FileUtils.createPath(
                sourceWebRootPath, '__site__.def', isFile=True), throwError=True)
        except Exception, err:
            self._logger.writeError(
                u'Failed to read __site__.def file. Check to make sure JSON is valid.', err)
            siteData = {}

        self._settings = DictUtils.lowerDictKeys(DictUtils.lowerDictKeys(siteData).get('s3', None))

        self._bucket = S3Bucket(
            self._settings['bucket'],
            self._settings['aws_id'],
            self._settings['aws_secret'])

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: localRootPath
    @property
    def localRootPath(self):
        return self._localRootPath

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ deploy
    def deploy(self):
        """Doc..."""
        if not os.path.exists(self._localRootPath):
            return False

        # Find the CDN root path if it exists
        self._cdnRootPath = None
        for item in os.listdir(self._localRootPath):
            itemPath = FileUtils.createPath(self._localRootPath, item)
            if item.startswith(StaticFlowEnvironment.CDN_ROOT_PREFIX) and os.path.isdir(itemPath):
                self._cdnRootPath = FileUtils.cleanupPath(itemPath)
                break

        # Deploy CDN files first so they are available when the non-cdn files are deployed
        if self._cdnRootPath:
            os.path.walk(self._cdnRootPath, self._deployWalker, {'cdn':True})

        # Walk the rest of the files not on the CDN root path
        os.path.walk(self._localRootPath, self._deployWalker, {'cdn':False})
        return True

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _deployWalker
    def _deployWalker(self, args, path, names):
        """Doc..."""

        # Skip CDN file uploads when not walking the CDN root path explicitly
        if not args['cdn'] and path.find(StaticFlowEnvironment.CDN_ROOT_PREFIX) != -1:
            return

        for name in names:
            namePath = FileUtils.createPath(path, name)
            if os.path.isdir(namePath) or StringUtils.ends(name, self._SKIP_EXTENSIONS):
                continue

            headersPath = namePath + '.headers'
            if os.path.exists(headersPath):
                headers = JSON.fromFile(headersPath)
            else:
                headers = dict()

            if self._forceAll:
                lastModified = None
            elif self._forceHtml and StringUtils.ends(name, self._FORCE_HTML_EXTENSIONS):
                lastModified = None
            else:
                lastModified = ArgsUtils.extract('_LAST_MODIFIED', None, headers)
                if lastModified:
                    lastModified = TimeUtils.webTimestampToDateTime(lastModified)

            kwargs = dict(
                key=u'/' + namePath[len(self._localRootPath):].replace(u'\\', u'/').strip(u'/'),
                maxAge=headers.get('max-age', -1),
                eTag=headers.get('eTag', None),
                expires=headers.get('Expires'),
                newerThanDate=lastModified,
                policy=S3Bucket.PUBLIC_READ)

            if StringUtils.ends(name, self._STRING_EXTENSIONS):
                result = self._bucket.put(
                    contents=FileUtils.getContents(namePath),
                    zipContents=True,
                    **kwargs)
            else:
                result = self._bucket.putFile(filename=namePath, **kwargs)

            if result:
                self._logger.write(u'DEPLOYED: ' + unicode(namePath) + u'->' + unicode(kwargs['key']))

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

