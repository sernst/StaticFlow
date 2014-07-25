# ParagraphTag.py
# (C)2013-2014
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

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        super(ParagraphTag, self)._renderImpl(**kwargs)

        # Forces the template to remain a paragraph template even if the parent FontTag class
        # reassigns the template from span to div because of the presence of a non-span property.
        self._renderTemplate = self.TEMPLATE
