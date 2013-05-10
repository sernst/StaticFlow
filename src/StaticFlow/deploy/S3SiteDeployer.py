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

from StaticFlow.deploy.S3Bucket import S3Bucket

#___________________________________________________________________________________________________ S3SiteDeployer
class S3SiteDeployer(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _SKIP_EXTENSIONS = ('.headers', '.def')

    _STRING_EXTENSIONS = ('.html', '.js', '.css', '.xml', '.json', '.txt')

#___________________________________________________________________________________________________ __init__
    def __init__(self, localRootPath, sourceWebRootPath, forceHtml =False, forceAll =False):
        """Creates a new instance of S3SiteDeployer."""
        self._localRootPath     = FileUtils.cleanupPath(localRootPath, isDir=True)
        self._sourceWebRootPath = FileUtils.cleanupPath(sourceWebRootPath, isDir=True)
        self._forceHtml         = forceHtml
        self._forceAll          = forceAll

        self._settings = DictUtils.lowerDictKeys(
            DictUtils.lowerDictKeys(
                JSON.fromFile(FileUtils.createPath(sourceWebRootPath, '__site__.def', isFile=True))
            ).get('s3', None)
        )

        self._bucket = S3Bucket(
            self._settings['bucket'],
            self._settings['aws_id'],
            self._settings['aws_secret']
        )

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
        os.path.walk(self._localRootPath, self._deployWalker, None)
        return True

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _deployWalker
    def _deployWalker(self, args, path, names):
        """Doc..."""
        for name in names:
            namePath = FileUtils.createPath(path, name)
            if os.path.isdir(namePath) or StringUtils.ends(name, self._SKIP_EXTENSIONS):
                continue

            headersPath = namePath + '.headers'
            if os.path.exists(headersPath):
                headers = JSON.fromFile(headersPath)
            else:
                headers = dict()

            lastModified = ArgsUtils.extract('_LAST_MODIFIED', None, headers)
            if lastModified:
                lastModified = TimeUtils.webTimestampToDateTime(lastModified)

            kwargs = dict(
                key=u'/' + namePath[len(self._localRootPath):].replace(u'\\', u'/').strip(u'/'),
                maxAge=headers.get('max-age', -1),
                eTag=headers.get('eTag', None),
                newerThanDate=lastModified,
                policy=S3Bucket.PUBLIC_READ
            )

            if StringUtils.ends(name, self._STRING_EXTENSIONS):
                result = self._bucket.put(
                    contents=FileUtils.getContents(namePath),
                    zipContents=True,
                    **kwargs
                )
            else:
                result = self._bucket.putFile(filename=namePath, **kwargs)

            if result:
                print 'DEPLOYED:', namePath, '->', kwargs['key']

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

