# ListTag.py
# (C)2012
# Scott Ernst

from StaticFlow.render.enum.GeneralSizeEnum import GeneralSizeEnum
from StaticFlow.render.attributes.LayoutAttributeParser import LayoutAttributeParser
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.MarkupBlockTag import MarkupBlockTag

#___________________________________________________________________________________________________ ListTag
class ListTag(MarkupBlockTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'list'
    TEMPLATE       = 'markup/list/listBase.mako'
    BLOCK_DISPLAY  = True
    STRIP_POLICY   = MarkupBlockTag.STRIP_ALL
    NEWLINE_POLICY = MarkupBlockTag.REMOVE_NEWLINES
    PRIMARY_ATTR   = TagAttributesEnum.TYPE[0]

#___________________________________________________________________________________________________ __init__
    def __init__(self, *args, **kwargs):
        MarkupBlockTag.__init__(self, *args, **kwargs)
        self._lineSpacing = None

#===================================================================================================
#                                                                                   G E T / S E T

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
        return MarkupBlockTag.getAttributeList() + t.COLOR + t.TYPE + t.START + t.INDEX + t.SPACING + \
               t.LINE_SPACING + t.SCALE

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: isOrdered
    @property
    def isOrdered(self):
        return self.attrs.getAsKeyword(
            TagAttributesEnum.TYPE,
            'bullet'
        ) != 'bullet'

#___________________________________________________________________________________________________ GS: lineSpacing
    @property
    def lineSpacing(self):
        if self._lineSpacing:
            return self._lineSpacing

        lineSpacing = self.attrs.getAsEnumerated(
            TagAttributesEnum.LINE_SPACING + TagAttributesEnum.SPACING,
            GeneralSizeEnum,
            None,
            allowFailure=True
        )
        if not lineSpacing:
            lineSpacing = self.attrs.getAsUnit(
                TagAttributesEnum.SPACING + TagAttributesEnum.LINE_SPACING,
                None
            )
            if lineSpacing:
                lineSpacing = lineSpacing.valueAndUnit
        else:
            if lineSpacing == GeneralSizeEnum.xxsmall[0]:
                lineSpacing = 0.5
            elif lineSpacing == GeneralSizeEnum.xsmall[0]:
                lineSpacing = 0.75
            elif lineSpacing == GeneralSizeEnum.small[0]:
                lineSpacing = 1.0
            elif lineSpacing == GeneralSizeEnum.medium[0]:
                lineSpacing = 1.25
            elif lineSpacing == GeneralSizeEnum.large[0]:
                lineSpacing = 1.5
            elif lineSpacing == GeneralSizeEnum.xlarge[0]:
                lineSpacing = 1.75
            elif lineSpacing == GeneralSizeEnum.xxlarge[0]:
                lineSpacing = 2.0
            else:
                lineSpacing = None

        if lineSpacing is None:
            lineSpacing = False

        self._lineSpacing = lineSpacing
        return self._lineSpacing

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a          = self.attrs

        LayoutAttributeParser.parseScale(a, True)

        startIndex = a.getAsInt(
            TagAttributesEnum.START + TagAttributesEnum.INDEX,
            None
        )

        self._addColorToGroup(a.styleGroup)

        if self.isOrdered and startIndex is not None:
            a.attrs.add('start', str(startIndex), a.styleGroup)

        if self.lineSpacing:
            a.styles.add(u'line-height', unicode(self.lineSpacing))

        a.render['listTag'] = 'ol' if self.isOrdered else 'ul'

        if self._procedural:
            self._renderTemplate = 'markup/list/nakedList.mako'

