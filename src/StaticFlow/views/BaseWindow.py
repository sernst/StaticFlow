# BaseWindow.py
# (C)2013
# Scott Ernst

from PySide import QtGui

from pyglass.gui.PyGlassGuiUtils import PyGlassGuiUtils
from pyglass.windows.PyGlassWindow import PyGlassWindow

#___________________________________________________________________________________________________ BaseWindow
class BaseWindow(PyGlassWindow):
    """A class for..."""

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ paintEvent
    def paintEvent(self, paintEvent):
        PyGlassGuiUtils.gradientPainter(
            self,
            self.size(),
            QtGui.QColor.fromHsv(0, 0, 255),
            QtGui.QColor.fromHsv(0, 0, 200)
        )

