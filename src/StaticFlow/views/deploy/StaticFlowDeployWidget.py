# StaticFlowDeployWidget.py
# (C)2013
# Scott Ernst

from PySide import QtGui

from pyaid.ArgsUtils import ArgsUtils
from pyaid.list.ListUtils import ListUtils

from pyglass.elements.buttons.PyGlassPushButton import PyGlassPushButton
from pyglass.elements.icons.IconSheetMap import IconSheetMap
from pyglass.enum.SizeEnum import SizeEnum
from pyglass.themes.ColorSchemes import ColorSchemes
from pyglass.widgets.PyGlassWidget import PyGlassWidget

from StaticFlow.enum.AppConfigEnum import AppConfigEnum
from StaticFlow.threads.SiteDeploymentThread import SiteDeploymentThread

#___________________________________________________________________________________________________ StaticFlowDeployWidget
class StaticFlowDeployWidget(PyGlassWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _HEADER_STYLE = "QLabel { font-size:12px; } "

    _serverThread = None

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of StaticFlowDeployWidget."""
        super(StaticFlowDeployWidget, self).__init__(parent, widgetFile=False, id='deploy', **kwargs)

        self._pathWidgets = []

        mainLayout = self._getLayout(self, QtGui.QVBoxLayout)
        mainLayout.setContentsMargins(6, 6, 6, 6)
        mainLayout.setSpacing(6)

        topWidget, topLayout = self._createWidget(self, QtGui.QHBoxLayout, True)

        label = QtGui.QLabel(topWidget)
        label.setText(u'Deploying Site:')
        label.setStyleSheet("QLabel { color:#333; font-weight:500; font-size:16px; }")
        topLayout.addWidget(label)
        topLayout.addStretch()

        btn = PyGlassPushButton(
            topWidget,
            text='Close',
            icon=IconSheetMap.CHECK,
            size=SizeEnum.MEDIUM,
            colorScheme=ColorSchemes.COPPER)
        btn.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        btn.clicked.connect(self._handleClose)
        topLayout.addWidget(btn)
        self._closeBtn = btn

        self._statusText = QtGui.QTextEdit(self)
        self._statusText.setReadOnly(True)
        self._statusText.setWordWrapMode(QtGui.QTextOption.NoWrap)
        mainLayout.addWidget(self._statusText)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: isDeploying
    @property
    def isDeploying(self):
        return self._serverThread is not None

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _executeDeployment
    def _executeDeployment(self, deployType):
        rootPath = self.mainWindow.getWidgetFromID('home').rootPath

        recentPaths = self.mainWindow.appConfig.get(AppConfigEnum.RECENT_PATHS, [])
        ListUtils.addIfMissing(rootPath, recentPaths, reorder=True, frontOrdering=True)
        self.mainWindow.appConfig.set(AppConfigEnum.RECENT_PATHS, recentPaths)

        self._closeBtn.setEnabled(False)

        thread = SiteDeploymentThread(self, rootPath=rootPath, deployType=deployType)
        self._serverThread = thread
        thread.logSignal.signal.connect(self._handleLogData)
        thread.completeSignal.signal.connect(self._handleDeploymentExecutionComplete)
        thread.start()
        self.mainWindow.updateStatusBar(u'Deployment in progress')

#___________________________________________________________________________________________________ _activateWidgetDisplayImpl
    def _activateWidgetDisplayImpl(self, **kwargs):
        self._statusText.clear()

        deployType = ArgsUtils.get('deployType', None, kwargs)
        if deployType is not None:
            self._executeDeployment(deployType)

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleCancel
    def _handleClose(self):
        self.mainWindow.setActiveWidget('home')
        self.mainWindow.updateStatusBar()

#___________________________________________________________________________________________________ _handleLogData
    def _handleLogData(self, data):
        self._statusText.append(unicode(data))
        self._statusText.moveCursor(QtGui.QTextCursor.End)

#___________________________________________________________________________________________________ _handleDeploymentExecutionComplete
    def _handleDeploymentExecutionComplete(self, response):
        self._serverThread.completeSignal.signal.disconnect(self._handleDeploymentExecutionComplete)
        self._serverThread.logSignal.signal.disconnect(self._handleLogData)
        self._serverThread = None

        self.mainWindow.updateStatusBar(u'Deployment complete')
        self._closeBtn.setEnabled(True)
