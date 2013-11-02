# StaticFlowCompiler.py
# (C)2013
# Scott Ernst

from pyglass.compile.PyGlassApplicationCompiler import PyGlassApplicationCompiler
from pyglass.compile.SiteLibraryEnum import SiteLibraryEnum

from StaticFlow.StaticFlowApplication import StaticFlowApplication

#___________________________________________________________________________________________________ StaticFlowCompiler
class StaticFlowCompiler(PyGlassApplicationCompiler):
    """A class for..."""

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: siteLibraries
    @property
    def siteLibraries(self):
        return [SiteLibraryEnum.PYSIDE]

#___________________________________________________________________________________________________ GS: binPath
    @property
    def binPath(self):
        return ['..', '..', 'bin']

#___________________________________________________________________________________________________ GS: appFilename
    @property
    def appFilename(self):
        return 'StaticFlow'

#___________________________________________________________________________________________________ GS: appDisplayName
    @property
    def appDisplayName(self):
        return 'StaticFlow'

#___________________________________________________________________________________________________ GS: applicationClass
    @property
    def applicationClass(self):
        return StaticFlowApplication

#___________________________________________________________________________________________________ GS: iconPath
    @property
    def iconPath(self):
        return ['apps', 'StaticFlow']

####################################################################################################
####################################################################################################

if __name__ == '__main__':
    StaticFlowCompiler().run()
