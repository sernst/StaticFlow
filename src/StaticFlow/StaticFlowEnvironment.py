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

#___________________________________________________________________________________________________ GS: nodePackageManagerPath
    @ClassGetter
    def nodePackageManagerPath(self):
        return FileUtils.createPath(os.environ['APPDATA'], 'npm', isDir=True)

#___________________________________________________________________________________________________ GS: rootTemplatePath
    @ClassGetter
    def rootTemplatePath(cls):
        return FileUtils.createPath(cls._ENV_PATH, '..', '..', 'templates', isDir=True)

#___________________________________________________________________________________________________ GS: rootPublicTemplatePath
    @ClassGetter
    def rootPublicTemplatePath(cls):
        return FileUtils.createPath(cls.rootTemplatePath, 'public', isDir=True)
