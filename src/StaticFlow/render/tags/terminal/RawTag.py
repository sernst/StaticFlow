# RawTag.py
# (C)2012-2013
# Scott Ernst

import textwrap

from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.MarkupBlockTag import MarkupBlockTag

#___________________________________________________________________________________________________ RawTag
class RawTag(MarkupBlockTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'raw'
    TEMPLATE       = 'vml/raw/rawDefault.mako'
    LEAF_TAG       = True
    BLOCK_DISPLAY  = True
    STRIP_POLICY   = MarkupBlockTag.STRIP_NEWLINES
    NEWLINE_POLICY = None

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
        return MarkupBlockTag.getAttributeList() + t.TITLE + t.STRIP + t.TAB_SIZE + t.COLOR

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a     = self.attrs

        title = a.get(
            TagAttributesEnum.TITLE,
            ''
        )

        strip = a.getAsBool(
            TagAttributesEnum.STRIP,
            True
        )

        tabSize = a.getAsInt(
            TagAttributesEnum.TAB_SIZE,
            4
        )

        self._addColorToGroup(a.styleGroup, extract=True, background=True)

        if title:
            a.render['title'] = title
            a.addTagClasses('title', 'title')

        a.content = a.content.replace('\t', tabSize*' ')
        if strip:
            a.content = textwrap.dedent(a.content)
