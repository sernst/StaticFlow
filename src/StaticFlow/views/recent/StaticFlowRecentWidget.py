# StaticFlowRecentWidget.py
# (C)2013
# Scott Ernst

from PySide import QtGui

from pyglass.elements.buttons.PyGlassPushButton import PyGlassPushButton
from pyglass.elements.icons.IconSheetMap import IconSheetMap
from pyglass.enum.SizeEnum import SizeEnum
from pyglass.themes.ColorSchemes import ColorSchemes
from pyglass.widgets.PyGlassWidget import PyGlassWidget

from StaticFlow.enum.AppConfigEnum import AppConfigEnum
from StaticFlow.views.recent.RecentPathElement import RecentPathElement

#___________________________________________________________________________________________________ StaticFlowRecentWidget
class StaticFlowRecentWidget(PyGlassWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _HEADER_STYLE = "QLabel { font-size:12px; } "

    _serverThread = None

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of StaticFlowRecentWidget."""
        super(StaticFlowRecentWidget, self).__init__(parent, widgetFile=False, id='recent', **kwargs)

        self._pathWidgets = []

        mainLayout = self._getLayout(self, QtGui.QVBoxLayout)
        mainLayout.setContentsMargins(6, 6, 6, 6)
        mainLayout.setSpacing(6)

        topWidget, topLayout = self._createWidget(self, QtGui.QHBoxLayout, True)

        label = QtGui.QLabel(topWidget)
        label.setText(u'Recent Project Paths:')
        label.setStyleSheet("QLabel { color:#333; font-weight:500; font-size:16px; }")
        topLayout.addWidget(label)
        topLayout.addStretch()

        btn = PyGlassPushButton(
            topWidget,
            text='Cancel',
            icon=IconSheetMap.CANCEL,
            size=SizeEnum.MEDIUM,
            colorScheme=ColorSchemes.BLUE
        )
        btn.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        btn.clicked.connect(self._handleCancel)
        topLayout.addWidget(btn)

        self._pathBox, layout = self._createWidget(self, QtGui.QVBoxLayout, True)

        mainLayout.addStretch()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________
    def _activateWidgetDisplayImpl(self, **kwargs):
        while len(self._pathWidgets) > 0:
            item = self._pathWidgets.pop()
            item.setParent(None)
            item.deleteLater()

        recentPaths = self.mainWindow.appConfig.get(AppConfigEnum.RECENT_PATHS, [])

        for path in recentPaths:
            w = RecentPathElement(self._pathBox, path)
            self._pathBox.layout().addWidget(w)
            self._pathWidgets.append(w)

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleCancel
    def _handleCancel(self):
        self.mainWindow.setActiveWidget('home')
