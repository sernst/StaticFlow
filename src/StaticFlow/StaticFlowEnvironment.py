# StaticFlowEnvironment.py
# (C)2013
# Scott Ernst

from pyaid.decorators.ClassGetter import ClassGetter
from pyaid.file.FileUtils import FileUtils

#___________________________________________________________________________________________________ StaticFlowEnvironment
class StaticFlowEnvironment(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _ENV_PATH = FileUtils.getDirectoryOf(__file__)

#___________________________________________________________________________________________________ rootTemplatePath
    @ClassGetter
    def rootTemplatePath(cls):
        return FileUtils.createPath(cls._ENV_PATH, '..', '..', 'templates', isDir=True)
