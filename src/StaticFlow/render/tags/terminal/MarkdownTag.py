# MarkdownTag.py
# (C)2012-2013
# Scott Ernst

import markdown

from pyaid.text.InsertCapPolicy import InsertCapPolicy
from StaticFlow.render.tags.MarkupBlockTag import MarkupBlockTag

#___________________________________________________________________________________________________ MarkdownTag
class MarkdownTag(MarkupBlockTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'markdown'
    TEMPLATE       = 'shared/vml/empty.mako'
    LEAF_TAG       = True
    STRIP_POLICY   = MarkupBlockTag.STRIP_NEWLINES

    BACK_CAP_POLICY = InsertCapPolicy(
        InsertCapPolicy.BACK_TYPE, removeExp=InsertCapPolicy.NEWLINE_BACK
    )

    AHEAD_CAP_POLICY = InsertCapPolicy(
        InsertCapPolicy.AHEAD_TYPE, removeExp=InsertCapPolicy.NEWLINE_AHEAD
    )

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a = self.attrs
        a.content = markdown.markdown(a.content)
        MarkupBlockTag._renderImpl(self, **kwargs)
