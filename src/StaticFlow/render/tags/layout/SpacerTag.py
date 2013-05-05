# SpacerTag.py
# (C)2012-2013
# Scott Ernst

from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.MarkupTag import MarkupTag

#___________________________________________________________________________________________________ SpacerTag
class SpacerTag(MarkupTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG           = 'spacer'
    TEMPLATE      = 'markup/divBase.mako'
    BLOCK_DISPLAY = True
    PRIMARY_ATTR  = TagAttributesEnum.HEIGHT[0]

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
        return MarkupTag.getAttributeList() + t.HEIGHT + t.COLOR

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a      = self.attrs
        height = a.getAsUnit(
            TagAttributesEnum.HEIGHT, 1.0, 'em'
        )

        a.styles.add(u'height', unicode(height))

        self._addColorToGroup(a.styleGroup, True)
