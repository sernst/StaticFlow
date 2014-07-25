# TextTag.py
# (C)2013-2014
# Scott Ernst

from StaticFlow.render.attributes.InsertAttributeParser import InsertAttributeParser
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.MarkupTag import MarkupTag

#___________________________________________________________________________________________________ TextTag
class TextTag(MarkupTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'text'
    TEMPLATE       = 'markup/text.mako'
    BLOCK_DISPLAY  = False
    PRIMARY_ATTR  = TagAttributesEnum.TEXT[0]

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        t = TagAttributesEnum
        return t.TEXT + t.TEXT_PATH + t.TEXT_SECTION + t.PATH + t.SECTION

#===================================================================================================
#                                                                               P R O T E C T E D


#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        super(TextTag, self)._renderImpl(**kwargs)
        result = InsertAttributeParser.parseText(self.attrs)
        self.attrs.render['text'] = u'' if not result else result

