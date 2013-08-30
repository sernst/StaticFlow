# StaticFlowApplication.py
# (C)2013
# Scott Ernst

from pyglass.app.PyGlassApplication import PyGlassApplication
from pyglass.app.PyGlassEnvironment import PyGlassEnvironment

from StaticFlow.StaticFlowEnvironment import StaticFlowEnvironment

#___________________________________________________________________________________________________ StaticFlowApplication
class StaticFlowApplication(PyGlassApplication):

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: debugRootResourcePath
    @property
    def debugRootResourcePath(self):
        return ['..', '..', 'resources']

#___________________________________________________________________________________________________ GS: splashScreenUrl
    @property
    def splashScreenUrl(self):
        return 'splashscreen.png'

#___________________________________________________________________________________________________ GS: appGroupID
    @property
    def appGroupID(self):
        return 'staticFlow'

#___________________________________________________________________________________________________ GS: appID
    @property
    def appID(self):
        return 'StaticFlow'

#___________________________________________________________________________________________________ GS: mainWindowClass
    @property
    def mainWindowClass(self):
        from StaticFlow.views.StaticFlowMainWindow import StaticFlowMainWindow
        return StaticFlowMainWindow

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________  _runPreMainWindowImpl
    def _runPreMainWindowImpl(self):
        templatePath = PyGlassEnvironment.getRootResourcePath(
            'apps', self.appID, 'templates', isDir=True)
        StaticFlowEnvironment.setTemplateRootPath(templatePath)

####################################################################################################
####################################################################################################

if __name__ == '__main__':
    StaticFlowApplication().run()


