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

#___________________________________________________________________________________________________ __init__
    def __init__(self, *args, **kwargs):
        super(TitleTag, self).__init__(*args, **kwargs)
        self._processor.metadata['title'] = self.attrs.content

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        return None


