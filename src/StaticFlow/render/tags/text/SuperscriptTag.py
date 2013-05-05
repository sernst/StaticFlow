# SuperscriptTag.py
# (C)2012
# Scott Ernst

from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.MarkupBlockTag import MarkupBlockTag

#___________________________________________________________________________________________________ SuperscriptTag
class SuperscriptTag(MarkupBlockTag):
    """VizmeML tag class for creating hyperlinks in web pages."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'super'
    TEMPLATE       = 'markup/text/superscript.mako'
    STRIP_POLICY   = MarkupBlockTag.STRIP_ALL
    NEWLINE_POLICY = MarkupBlockTag.REMOVE_NEWLINES

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: apiLevel
    @property
    def apiLevel(self):
        return 0

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        t = TagAttributesEnum
        return MarkupBlockTag.getAttributeList() + t.COLOR

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a = self.attrs
        self._addColorToGroup(a.styleGroup)

