# LineTag.py
# (C)2012-2013
# Scott Ernst

from StaticFlow.render.enum.GeneralSizeEnum import GeneralSizeEnum
from StaticFlow.render.enum.LineTypesEnum import LineTypesEnum
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.MarkupTag import MarkupTag

#___________________________________________________________________________________________________ LineTag
class LineTag(MarkupTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG           = 'line'
    TEMPLATE      = 'markup/divBase.mako'
    BLOCK_DISPLAY = True
    PRIMARY_ATTR  = TagAttributesEnum.LINE_TYPE

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
        return MarkupTag.getAttributeList() + t.LINE_WIDTH + t.WIDTH + t.LINE_TYPE + t.TYPE + \
               t.COLOR + t.SPACING

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a = self.attrs

        spacing = a.getAsTShirtSize(
            TagAttributesEnum.SPACING,
            0.25,
            kwargs,
            values=[0.1, 0.2, 0.25, 0.5, 1.0, 2.0, 4.0, 0.0]
        )

        lineType = a.getAsEnumerated(
            TagAttributesEnum.LINE_TYPE + TagAttributesEnum.TYPE,
            LineTypesEnum,
            LineTypesEnum.SOLID
        )

        color = a.getAsColorMixer(
            TagAttributesEnum.COLOR,
            None,
        )

        lineWidth = a.getAsInt(
            TagAttributesEnum.LINE_WIDTH + TagAttributesEnum.WIDTH,
            None,
            allowFailure=True
        )

        if lineWidth is None:
            lineWidthEnum = a.getAsEnumerated(
                TagAttributesEnum.LINE_WIDTH + TagAttributesEnum.WIDTH,
                GeneralSizeEnum,
                GeneralSizeEnum.xxsmall
            )
            if lineWidthEnum == GeneralSizeEnum.xxsmall[0]:
                lineWidth = 1
            elif lineWidthEnum == GeneralSizeEnum.xsmall[0]:
                lineWidth = 2
            elif lineWidthEnum == GeneralSizeEnum.small[0]:
                lineWidth = 3
            elif lineWidthEnum == GeneralSizeEnum.medium[0]:
                lineWidth = 4
            elif  lineWidthEnum == GeneralSizeEnum.large[0]:
                lineWidth = 5
            elif  lineWidthEnum == GeneralSizeEnum.xlarge[0]:
                lineWidth = 6
            elif lineWidthEnum == GeneralSizeEnum.xxlarge[0]:
                lineWidth = 7
            else:
                lineWidth = 1

        lineColor = color.web if color else 'currentColor'

        a.styles.add('border-top', '%spx %s %s' % (str(lineWidth), lineType, lineColor),
                     a.styleGroup)

        if lineColor == 'currentColor':
            a.classes.add('v-S-borbor', a.styleGroup)

        if spacing:
            a.styles.add('margin', str(spacing) + 'em auto')


