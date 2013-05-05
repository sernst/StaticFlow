# SqueezeBoxTag.py
# (C)2012
# Scott Ernst

from StaticFlow.render.enum.GeneralSizeEnum import GeneralSizeEnum
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.box.BoxTag import BoxTag

#___________________________________________________________________________________________________ SqueezeBoxTag
class SqueezeBoxTag(BoxTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG           = 'squeeze'
    PRIMARY_ATTR  = TagAttributesEnum.AMOUNT[0]

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        t = TagAttributesEnum
        return BoxTag.getAttributeList() + t.TYPE + t.SIZE + t.COLOR

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a = self.attrs

        class SqueezeEnum(object):
            VERTICAL = ['v', ['vertical','vert','v']]

            HORIZONTAL = ['h', ['horizontal', 'horiz', 'h']]

        squeezeType = a.getAsEnumerated(
            TagAttributesEnum.TYPE,
            SqueezeEnum,
            SqueezeEnum.HORIZONTAL,
            overrides=kwargs,
            extract=True
        )

        pad = a.getAsEnumerated(
            TagAttributesEnum.SIZE,
            GeneralSizeEnum,
            None,
            overrides=kwargs,
        )
        if pad is None:
            pad = a.getAsUnit(
                TagAttributesEnum.SIZE,
                None
            )

        if isinstance(pad, basestring):
            if pad == GeneralSizeEnum.xxsmall[0]:
                pad = '0.25em'
            elif pad == GeneralSizeEnum.xsmall[0]:
                pad = '0.5em'
            elif pad == GeneralSizeEnum.small[0]:
                pad = '0.75em'
            elif pad == GeneralSizeEnum.medium[0]:
                pad = '1.0em'
            elif pad == GeneralSizeEnum.large[0]:
                pad = '1.5em'
            elif pad == GeneralSizeEnum.xlarge[0]:
                pad = '2.0em'
            elif pad == GeneralSizeEnum.xxlarge[0]:
                pad = '3.0em'
            else:
                pad = '0'
        elif pad:
            pad = pad.valueAndUnit

        if pad is None:
            pad = '0.5em'

        if squeezeType == 'h':
            a.styles.add('margin', 'auto ' + pad)
        else:
            a.styles.add('margin', pad + ' auto')

        BoxTag._renderImpl(self, **kwargs)
