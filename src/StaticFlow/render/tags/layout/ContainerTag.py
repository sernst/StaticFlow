# ContainerTag.py
# (C)2012
# Scott Ernst

from StaticFlow.render.enum.GeneralSizeEnum import GeneralSizeEnum
from StaticFlow.render.attributes.AttributeUtils import AttributeUtils
from StaticFlow.render.attributes.LayoutAttributeParser import LayoutAttributeParser
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.attributes.UnitAttribute import UnitAttribute
from StaticFlow.render.tags.MarkupBlockTag import MarkupBlockTag

#___________________________________________________________________________________________________ ContainerTag
class ContainerTag(MarkupBlockTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'container'
    TEMPLATE       = 'vml/box/default.mako'
    BLOCK_DISPLAY  = True
    STRIP_POLICY   = MarkupBlockTag.STRIP_ALL
    NEWLINE_POLICY = MarkupBlockTag.BREAK_ON_NEWLINES
    PRIMARY_ATTR   = TagAttributesEnum.MAX_WIDE[0]

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        t = TagAttributesEnum
        return MarkupBlockTag.getAttributeList() + t.MAX_WIDE + t.COLOR + t.SIZE + t.ALIGNMENT + \
               t.SCALE + t.GUTTER

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a = self.attrs

        LayoutAttributeParser.parseScale(a, True)
        LayoutAttributeParser.parseAlignment(a, True)

        self._addColorToGroup(a.styleGroup)

        gutter = a.getAsBool(
            TagAttributesEnum.GUTTER,
            None,
            kwargs,
            allowFailure=True
        )
        if gutter:
            gutter = GeneralSizeEnum.small[0]
        else:
            gutter = a.get(
                TagAttributesEnum.GUTTER,
                None,
                kwargs
            )

        maxW = a.get(
            TagAttributesEnum.MAX_WIDE + TagAttributesEnum.SIZE,
            GeneralSizeEnum.medium[0],
            kwargs
        )

        maxW = AttributeUtils.parseSizeEnumValues(
            maxW,
            [48, 64, 80, 92, 102, 160],
            minValue=24,
            maxValue=240,
            asInt=True
        )
        if isinstance(maxW, UnitAttribute):
            maxW.setDefaultUnit(u'')
            if not maxW.unit:
                maxW = u'~' + unicode(maxW.value)
            else:
                maxW = maxW.valueAndUnit
        elif maxW:
            maxW = u'~' + unicode(maxW)

        if maxW:
            a.vdata.add('maxw', maxW)

        if gutter:
            gutter = AttributeUtils.parseSizeEnumValues(
                gutter,
                [0.25, 0.5, 1.0, 1.5, 2.25, 3.0, 4.0],
                minValue=0.0,
                maxValue=5.0,
            )

            if isinstance(gutter, UnitAttribute):
                gutter.setDefaultUnit(u'em')
                gutter = gutter.valueAndUnit
            elif gutter:
                gutter = unicode(gutter) + u'em'

            if gutter:
                a.styles.add('padding', u'0 ' + unicode(gutter))
