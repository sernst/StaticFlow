# StaticFlowHomeWidget.py
# (C)2013
# Scott Ernst

import os

from PySide import QtGui

from pyaid.file.FileUtils import FileUtils

from pyglass.dialogs.PyGlassBasicDialogManager import PyGlassBasicDialogManager
from pyglass.elements.buttons.PyGlassPushButton import PyGlassPushButton
from pyglass.elements.icons.IconSheetMap import IconSheetMap
from pyglass.enum.SizeEnum import SizeEnum
from pyglass.widgets.PyGlassWidget import PyGlassWidget

from StaticFlow.enum.AppConfigEnum import AppConfigEnum
from StaticFlow.enum.DeploymentTypeEnum import DeploymentTypeEnum

#___________________________________________________________________________________________________ StaticFlowHomeWidget
class StaticFlowHomeWidget(PyGlassWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _HEADER_STYLE = "QLabel { font-size:14px; }"
    _INFO_STYLE   = "QLabel { font-size:10px; color:#666; }"

    _serverThread = None

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of StaticFlowHomeWidget."""
        super(StaticFlowHomeWidget, self).__init__(parent, widgetFile=False, id='home', **kwargs)

        mainLayout = self._getLayout(self, QtGui.QVBoxLayout)
        mainLayout.setContentsMargins(6, 6, 6, 6)

        rootPath = self.mainWindow.appConfig.get(AppConfigEnum.ROOT_PATH, u'')

        label = QtGui.QLabel(self)
        label.setText(u'Project Root Path:')
        label.setStyleSheet(self._HEADER_STYLE)
        mainLayout.addWidget(label)

        label = QtGui.QLabel(self)
        label.setText(u'The absolute path where your Static Flow project resides')
        label.setStyleSheet(self._INFO_STYLE)
        mainLayout.addWidget(label)
        mainLayout.addSpacing(3)

        textWidget, textLayout = self._createWidget(self, QtGui.QHBoxLayout, True)

        text = QtGui.QLineEdit(textWidget)
        text.setText(rootPath)
        textLayout.addWidget(text)
        self._pathLineEdit = text
        self._pathLineEdit.textChanged.connect(self._handlePathUpdated)

        recent = PyGlassPushButton(textWidget, icon=IconSheetMap.DOWN, size=SizeEnum.SMALL)
        recent.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        recent.clicked.connect(self._handleRecentLocations)
        textLayout.addWidget(recent)
        self._recentBtn = recent

        browse = PyGlassPushButton(textWidget, icon=IconSheetMap.FOLDER, size=SizeEnum.SMALL)
        browse.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        browse.clicked.connect(self._handleLocatePath)
        textLayout.addWidget(browse)
        self._browseBtn = browse

        mainLayout.addSpacing(20)

        label = QtGui.QLabel(self)
        label.setText(u'Deployment:')
        label.setStyleSheet(self._HEADER_STYLE)
        mainLayout.addWidget(label)

        label = QtGui.QLabel(self)
        label.setText(u'Site deployment operations')
        label.setStyleSheet(self._INFO_STYLE)
        mainLayout.addWidget(label)
        mainLayout.addSpacing(3)

        buttonBox, boxLayout = self._createWidget(self, QtGui.QHBoxLayout, True)

        btn = PyGlassPushButton(buttonBox, text='Remote')
        btn.clicked.connect(self._handleRemoteDeploy)
        boxLayout.addWidget(btn)
        self._remoteBtn = btn

        btn = PyGlassPushButton(buttonBox, text='Local')
        btn.clicked.connect(self._handleLocalDeploy)
        boxLayout.addWidget(btn)
        self._localBtn = btn

        btn = PyGlassPushButton(buttonBox, text='Test')
        btn.clicked.connect(self._handleTestDeploy)
        boxLayout.addWidget(btn)
        self._testBtn = btn

        boxLayout.addStretch()

        mainLayout.addStretch()

        self._updateDisplay()

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: rootPath
    @property
    def rootPath(self):
        path = self._pathLineEdit.text()
        if path:
            return FileUtils.cleanupPath(path)
        return u''
    @rootPath.setter
    def rootPath(self, value):
        self._pathLineEdit.setText(FileUtils.cleanupPath(value))

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _updateDisplay
    def _updateDisplay(self):
        allow = self._serverThread is None
        if allow:
            allow = os.path.exists(self.rootPath)
            if allow:
                path = FileUtils.createPath(self.rootPath, 'src', isDir=True)
                allow = os.path.exists(path)

        self._remoteBtn.setEnabled(allow)
        self._localBtn.setEnabled(allow)
        self._testBtn.setEnabled(allow)
        self.mainWindow.appConfig.set(AppConfigEnum.ROOT_PATH, self.rootPath)

#___________________________________________________________________________________________________ _executeDeployment
    def _executeDeployment(self, deployType):
        self.mainWindow.setActiveWidget('deploy', args={'deployType':deployType})

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleLocatePath
    def _handleLocatePath(self):
        self.refreshGui()
        path = QtGui.QFileDialog.getExistingDirectory(
            self,
            caption=u'Specify Static Flow Project Path',
            dir=self.rootPath
        )

        if path:
            path = FileUtils.cleanupPath(path)
            self._pathLineEdit.setText(path)

#___________________________________________________________________________________________________ _handlePathUpdated
    def _handlePathUpdated(self):
        self._updateDisplay()

#___________________________________________________________________________________________________ _handleRecentLocations
    def _handleRecentLocations(self):
        self.mainWindow.setActiveWidget('recent')

#___________________________________________________________________________________________________ _handleRemoteDeploy
    def _handleRemoteDeploy(self):
        result = PyGlassBasicDialogManager.openYesNo(
            self,
            u'Confirm Remote Deploy',
            u'Are you sure you want to deploy this project?',
            False)

        if not result:
            return

        print u'Beginning Remote Deployment...'
        self._executeDeployment(DeploymentTypeEnum.REMOTE_DEPLOY)

#___________________________________________________________________________________________________ _handleLocalDeploy
    def _handleLocalDeploy(self):
        print u'Beginning Local Deployment...'
        self._executeDeployment(DeploymentTypeEnum.LOCAL_DEPLOY)

#___________________________________________________________________________________________________ _handleTestDeploy
    def _handleTestDeploy(self):
        print u'Beginning Test Deployment...'
        self._executeDeployment(DeploymentTypeEnum.TEST_DEPLOY)
