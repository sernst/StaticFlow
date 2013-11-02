# StaticFlowMainWindow.py
# (C)2013
# Scott Ernst

from PySide import QtGui

from StaticFlow.views.BaseWindow import BaseWindow
from StaticFlow.views.deploy.StaticFlowDeployWidget import StaticFlowDeployWidget
from StaticFlow.views.home.StaticFlowHomeWidget import StaticFlowHomeWidget
from StaticFlow.views.recent.StaticFlowRecentWidget import StaticFlowRecentWidget

#___________________________________________________________________________________________________ StaticFlowMainWindow
class StaticFlowMainWindow(BaseWindow):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        super(StaticFlowMainWindow, self).__init__(
            title=u'Static Flow Project Manager',
            widgets={
                'home':StaticFlowHomeWidget,
                'recent':StaticFlowRecentWidget,
                'deploy':StaticFlowDeployWidget },
            **kwargs )

        self._projectData = None

        mainLayout = self.layout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        w = QtGui.QWidget(self)
        self.setCentralWidget(w)
        self._centerWidget = self.centralWidget()
        self.setActiveWidget('home')

        self.setMinimumSize(480, 180)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: isDeploying
    @property
    def isDeploying(self):
        return self.getWidgetFromID('deploy').isDeploying

