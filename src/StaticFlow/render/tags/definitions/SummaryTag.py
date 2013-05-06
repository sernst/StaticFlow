# SummaryTag.py
# (C)2013
# Scott Ernst

from StaticFlow.render.tags.MarkupBlockTag import MarkupBlockTag

#___________________________________________________________________________________________________ SummaryTag
class SummaryTag(MarkupBlockTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'summary'
    TEMPLATE       = 'markup/empty.mako'
    BLOCK_DISPLAY  = False
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

#___________________________________________________________________________________________________
    def _renderImpl(self, **kwargs):
        self._processor.metadata['summary'] = self.attrs.content
