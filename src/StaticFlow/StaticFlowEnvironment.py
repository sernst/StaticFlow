# StaticFlowEnvironment.py
# (C)2013
# Scott Ernst

import os

from pyaid.decorators.ClassGetter import ClassGetter
from pyaid.file.FileUtils import FileUtils

from pyglass.app.PyGlassEnvironment import PyGlassEnvironment

#___________________________________________________________________________________________________ StaticFlowEnvironment
class StaticFlowEnvironment(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    CDN_ROOT_PREFIX = u'__cdn__'

    _ENV_PATH = FileUtils.getDirectoryOf(__file__)

    _resourceRootOverridePath = None

#___________________________________________________________________________________________________ GS: baseTime
    @ClassGetter
    def baseTime(self):
        """ Returns the base time off which all time codes are generated. This is Jan 1, 2013, the
            first day of the year StaticFlow was created.
        """
        return 1356998400

#___________________________________________________________________________________________________ GS: nodePackageManagerPath
    @ClassGetter
    def nodePackageManagerPath(self):
        if PyGlassEnvironment.isWindows:
            return FileUtils.createPath(os.environ['APPDATA'], 'npm', isDir=True)
        return '/usr/local/bin/'

#___________________________________________________________________________________________________ getNodeCommandAbsPath
    @classmethod
    def getNodeCommandAbsPath(cls, command):
        return FileUtils.createPath(cls.nodePackageManagerPath, command, isFile=True)

#___________________________________________________________________________________________________ GS: rootResourcePath
    @ClassGetter
    def rootResourcePath(cls):
        if cls._resourceRootOverridePath is None:
            return FileUtils.createPath(cls._ENV_PATH, '..', '..', 'resources')
        return cls._resourceRootOverridePath

#___________________________________________________________________________________________________ GS: rootTemplatePath
    @ClassGetter
    def rootTemplatePath(cls):
        return FileUtils.createPath(
            cls.rootResourcePath, 'apps', 'StaticFlow', 'templates', isDir=True)

#___________________________________________________________________________________________________ GS: rootPublicTemplatePath
    @ClassGetter
    def rootPublicTemplatePath(cls):
        return FileUtils.createPath(cls.rootTemplatePath, 'public', isDir=True)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ setTemplateRootPath
    @classmethod
    def setResourceRootPath(cls, path):
        cls._resourceRootOverridePath = FileUtils.cleanupPath(path, isDir=True)
