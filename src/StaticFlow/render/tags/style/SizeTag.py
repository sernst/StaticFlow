# SizeTag.py
# (C)2012
# Scott Ernst

from StaticFlow.render.attributes.LayoutAttributeParser import LayoutAttributeParser
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.MarkupBlockTag import MarkupBlockTag

#___________________________________________________________________________________________________ SizeTag
class SizeTag(MarkupBlockTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'size'
    TEMPLATE       = 'markup/spanBase.mako'
    STRIP_POLICY   = MarkupBlockTag.STRIP_NEWLINES
    NEWLINE_POLICY = MarkupBlockTag.BREAK_ON_NEWLINES
    PRIMARY_ATTR   = TagAttributesEnum.SIZE[0]

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
        return MarkupBlockTag.getAttributeList() + t.SIZE + t.COLOR + t.SCALE

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a = self.attrs
        LayoutAttributeParser.parseScale(a, True, useSizeKeys=True)

        self._addColorToGroup(a.styleGroup)

