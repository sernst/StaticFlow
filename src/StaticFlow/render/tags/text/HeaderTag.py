# HeaderTag.py
# (C)2012-2013
# Scott Ernst

from pyaid.text.InsertCapPolicy import InsertCapPolicy
from StaticFlow.render.attributes.InsertAttributeParser import InsertAttributeParser
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.MarkupBlockTag import MarkupBlockTag

#___________________________________________________________________________________________________ HeaderTag
class HeaderTag(MarkupBlockTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'header'
    TEMPLATE       = 'markup/definitions/title.mako'
    BLOCK_DISPLAY  = True
    STRIP_POLICY   = MarkupBlockTag.STRIP_ALL
    NEWLINE_POLICY = MarkupBlockTag.REMOVE_NEWLINES
    PRIMARY_ATTR   = TagAttributesEnum.LEVEL[0]

    _BACK_CAP = InsertCapPolicy(
        InsertCapPolicy.BACK_TYPE, addExp=InsertCapPolicy.NEWLINE_BACK, addReplace=u'<br />')

    _AHEAD_CAP = InsertCapPolicy(
        InsertCapPolicy.AHEAD_TYPE, removeExp=InsertCapPolicy.NEWLINE_AHEAD)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: apiLevel
    @property
    def apiLevel(self):
        return 0

#___________________________________________________________________________________________________ GS: aheadCapPolicy
    @property
    def aheadCapPolicy(self):
        return HeaderTag._AHEAD_CAP

#___________________________________________________________________________________________________ GS: backCapPolicy
    @property
    def backCapPolicy(self):
        return HeaderTag._BACK_CAP

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        TAE = TagAttributesEnum
        return MarkupBlockTag.getAttributeList() + TAE.LEVEL + TAE.TEXT_SECTION + TAE.SECTION \
            + TAE.PATH + TAE.TEXT_PATH + TAE.COLOR

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a = self.attrs

        self._addColorToGroup()

        a.render['level'] = str(a.getAsInt(
            TagAttributesEnum.LEVEL,
            1, kwargs))

        result = InsertAttributeParser.parseText(self.attrs)
        self.attrs.render['text'] = u'' if not result else result

        # self._processor.addAnchor({'id':a.id.get(), 'lbl':a.content, 'lvl':level})


