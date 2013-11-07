# TitleTag.py
# (C)2013
# Scott Ernst

from StaticFlow.render.tags.MarkupBlockTag import MarkupBlockTag
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum

#___________________________________________________________________________________________________ TitleTag
class TitleTag(MarkupBlockTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'title'
    TEMPLATE       = 'markup/definitions/title.mako'
    BLOCK_DISPLAY  = True
    STRIP_POLICY   = MarkupBlockTag.STRIP_NEWLINES
    NEWLINE_POLICY = MarkupBlockTag.BREAK_ON_NEWLINES

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        return TagAttributesEnum.LEVEL

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a = self.attrs

        self.attrs.render['level'] = str(a.getAsInt(
            TagAttributesEnum.LEVEL,
            1, kwargs))

        self._processor.metadata['title'] = self.attrs.content

