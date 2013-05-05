# JumpTag.py
# (C)2012
# Scott Ernst

from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.MarkupBlockTag import MarkupBlockTag

#___________________________________________________________________________________________________ JumpTag
class JumpTag(MarkupBlockTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'jump'
    TEMPLATE       = 'shared/vml/spanBase.mako'
    STRIP_POLICY   = MarkupBlockTag.STRIP_ALL
    NEWLINE_POLICY = MarkupBlockTag.REMOVE_NEWLINES
    PRIMARY_ATTR   = TagAttributesEnum.TO[0]

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        t = TagAttributesEnum
        return MarkupBlockTag.getAttributeList() + t.TO + t.TARGET

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a      = self.attrs

        jumpID = a.get(
            TagAttributesEnum.TO + TagAttributesEnum.TARGET,
            None
        )

        self._addColorToGroup(a.styleGroup)

        if jumpID:
            a.vdata.add('jid', jumpID, a.styleGroup)
            a.classes.add(['v-S-lnk-h', 'v-hoverLink'], a.styleGroup)
