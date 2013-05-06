# TitleTag.py
# (C)2013
# Scott Ernst

from StaticFlow.render.tags.MarkupBlockTag import MarkupBlockTag

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
        return None

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        self._processor.metadata['title'] = self.attrs.content
