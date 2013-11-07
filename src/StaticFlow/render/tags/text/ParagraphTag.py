# ParagraphTag.py
# (C)2013
# Scott Ernst

from StaticFlow.render.tags.MarkupBlockTag import MarkupBlockTag
from StaticFlow.render.tags.style.FontTag import FontTag

#___________________________________________________________________________________________________ ParagraphTag
class ParagraphTag(FontTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'p'
    TEMPLATE       = 'markup/paragraphBase.mako'
    BLOCK_DISPLAY  = True
    STRIP_POLICY   = MarkupBlockTag.STRIP_ALL
    NEWLINE_POLICY = MarkupBlockTag.STRIP_NEWLINES
