# RecentPathElement.py
# (C)2013
# Scott Ernst

from PySide import QtGui

from pyaid.string.StringUtils import StringUtils

from pyglass.elements.InteractiveElement import InteractiveElement
from pyglass.elements.icons.IconElement import IconElement
from pyglass.elements.icons.IconSheetMap import IconSheetMap
from pyglass.enum.InteractionStatesEnum import InteractionStatesEnum
from pyglass.enum.SizeEnum import SizeEnum
from pyglass.gui.PyGlassGuiUtils import PyGlassGuiUtils
from pyglass.widgets.LineSeparatorWidget import LineSeparatorWidget

#___________________________________________________________________________________________________ RecentPathElement
class RecentPathElement(InteractiveElement):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _LABEL_STYLE = "QLabel { color:#C#; font-weight:500; font-size:12px; }"

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, path, **kwargs):
        """Creates a new instance of RecentPathElement."""
        self._path = path
        super(RecentPathElement, self).__init__(parent, **kwargs)

        mainLayout = self._getLayout(self, QtGui.QVBoxLayout)

        line = LineSeparatorWidget(self)
        mainLayout.addWidget(line)
        mainLayout.addSpacing(6)

        widget, layout = self._createWidget(self, QtGui.QHBoxLayout, True)
        layout.setContentsMargins(6, 0, 12, 0)

        label = QtGui.QLabel(widget)
        label.setText(StringUtils.abbreviateCenter(path, 72))
        layout.addWidget(label)
        self._label = label

        layout.addStretch()

        icon = IconElement(widget, icon=IconSheetMap.FORWARD, size=SizeEnum.SMALL)
        layout.addWidget(icon)
        self._icon = icon

        mainLayout.addSpacing(6)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: path
    @property
    def path(self):
        return self._path

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ paintEvent
    def paintEvent(self, *args, **kwargs):
        """Doc..."""
        if self._mode == InteractionStatesEnum.OVER_MODE:
            PyGlassGuiUtils.fillPainter(self, self.size(), QtGui.QColor.fromRgb(200, 200, 200))

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _onClickEventImpl
    def _onClickEventImpl(self, event):
        self.mainWindow.widgets['home'].rootPath = self.path
        self.mainWindow.setActiveWidget('home')

#___________________________________________________________________________________________________ _updateDisplayImpl
    def _updateDisplayImpl(self):
        """Doc..."""
        if self._mode == InteractionStatesEnum.OVER_MODE:
            self._label.setStyleSheet(self._LABEL_STYLE.replace('#C#', '#222'))
            self._icon.opacity = 1.0
            return

        self._label.setStyleSheet(self._LABEL_STYLE.replace('#C#', '#444'))
        self._icon.opacity = 0.75

