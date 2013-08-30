# StaticFlowEnvironment.py
# (C)2013
# Scott Ernst

import os

from pyaid.decorators.ClassGetter import ClassGetter
from pyaid.file.FileUtils import FileUtils

#___________________________________________________________________________________________________ StaticFlowEnvironment
class StaticFlowEnvironment(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _ENV_PATH = FileUtils.getDirectoryOf(__file__)

    _templateRootOverridePath = None

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
        return FileUtils.createPath(os.environ['APPDATA'], 'npm', isDir=True)

#___________________________________________________________________________________________________ GS: rootTemplatePath
    @ClassGetter
    def rootTemplatePath(cls):
        if cls._templateRootOverridePath is not None:
            return cls._templateRootOverridePath
        return FileUtils.createPath(
            cls._ENV_PATH, '..', '..', 'resources', 'apps', 'StaticFlow', 'templates', isDir=True)

#___________________________________________________________________________________________________ GS: rootPublicTemplatePath
    @ClassGetter
    def rootPublicTemplatePath(cls):
        return FileUtils.createPath(cls.rootTemplatePath, 'public', isDir=True)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ setTemplateRootPath
    @classmethod
    def setTemplateRootPath(cls, path):
        cls._templateRootOverridePath = FileUtils.cleanupPath(path, isDir=True)
