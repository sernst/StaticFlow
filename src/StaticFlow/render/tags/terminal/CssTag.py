# CssTag.py
# (C)2013
# Scott Ernst

from pyaid.text.InsertCapPolicy import InsertCapPolicy
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.MarkupBlockTag import MarkupBlockTag

#___________________________________________________________________________________________________ CssTag
class CssTag(MarkupBlockTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'css'
    LEAF_TAG       = True
    VOID_TAG       = True
    STRIP_POLICY   = MarkupBlockTag.STRIP_ALL
    PRIMARY_ATTR   = TagAttributesEnum.TYPE[0]

    BACK_CAP_POLICY = InsertCapPolicy(
        InsertCapPolicy.BACK_TYPE, removeExp=InsertCapPolicy.NEWLINE_BACK)

    AHEAD_CAP_POLICY = InsertCapPolicy(
        InsertCapPolicy.AHEAD_TYPE, removeExp=InsertCapPolicy.NEWLINE_AHEAD)

#___________________________________________________________________________________________________ __init__
    def __init__(self, *args, **kwargs):
        MarkupBlockTag.__init__(self, *args, **kwargs)
        self._content   = None
        self._cachePath = None
        self._minify    = True

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: styles
    @property
    def styles(self):
        return self._content

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
        return MarkupBlockTag.getAttributeList() + t.TYPE + t.MINIFY + t.MINIMIZE + t.SHRINK

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a = self.attrs

        self._minify = a.getAsBool(
            TagAttributesEnum.MINIFY + TagAttributesEnum.MINIMIZE + TagAttributesEnum.SHRINK,
            self._minify)

        self._content = a.content
        self._processor.addCSSStyles(self._content)

        MarkupBlockTag._renderImpl(self, **kwargs)

