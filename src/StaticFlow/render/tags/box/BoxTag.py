# BoxTag.py
# (C)2012-2013
# Scott Ernst

from pyaid.color.ColorValue import ColorValue
from pyaid.ArgsUtils import ArgsUtils
from StaticFlow.render.enum.GeneralSizeEnum import GeneralSizeEnum
from StaticFlow.render.attributes.LayoutAttributeParser import LayoutAttributeParser
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.MarkupBlockTag import MarkupBlockTag

#___________________________________________________________________________________________________ BoxTag
class BoxTag(MarkupBlockTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'box'
    TEMPLATE       = 'markup/box/default.mako'
    BLOCK_DISPLAY  = True
    STRIP_POLICY   = MarkupBlockTag.STRIP_ALL
    NEWLINE_POLICY = MarkupBlockTag.BREAK_ON_NEWLINES

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
        return MarkupBlockTag.getAttributeList() + t.COLOR + t.ALIGNMENT + t.PADDING + t.ROUNDNESS + \
               t.COLOR + t.REACH + t.SCALE + t.BORDER

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a = self.attrs

        LayoutAttributeParser.parseScale(a, True, kwargs)
        LayoutAttributeParser.parseAlignment(a, True, kwargs)
        LayoutAttributeParser.parsePadding(
            a, True, kwargs, group=a.styleGroup, defaultValue=GeneralSizeEnum.xsmall[0])

        color = a.getAsColorValue(
            TagAttributesEnum.COLOR,
            ArgsUtils.get('colorDef', None, kwargs),
            kwargs)

        if not ArgsUtils.get('skipBorder', False, kwargs):
            LayoutAttributeParser.parseBorder(
                a, True, kwargs,
                group=a.styleGroup,
                defaultColor=ArgsUtils.get(
                    'borderColorDef', color.shiftColors[1] if color else None, kwargs) )

        inline = a.getAsBool(
            TagAttributesEnum.INLINE,
            ArgsUtils.get('inlineDef', None, kwargs),
            kwargs)

        roundness = a.getAsEnumerated(
            TagAttributesEnum.ROUNDNESS,
            GeneralSizeEnum,
            ArgsUtils.get('roundnessDef', GeneralSizeEnum.none, kwargs),
            kwargs)

        #-------------------------------------------------------------------------------------------
        # BACKGROUND COLOR
        if not ArgsUtils.get('skipBackground', False, kwargs):
            if isinstance(color, ColorValue):
                a.styles.add('background-color', color.web, a.styleGroup)
            elif a.explicitAccent or a.themeChanged:
                self.useBackground()

        #-------------------------------------------------------------------------------------------
        # ROUNDNESS
        if roundness == 'xxs':
            r = '0.13em'
        elif roundness == 'xs':
            r = '0.25em'
        elif roundness == 's':
            r = '0.5em'
        elif roundness == 'm':
            r = '0.75em'
        elif roundness == 'l':
            r = '1.0em'
        elif roundness == 'xl':
            r = '1.25em'
        elif roundness == 'xxl':
            r = '1.5em'
        else:
            r = None

        if r:
            a.styles.add('border-radius', r, a.styleGroup)

        if inline:
            a.styles.add('display', 'inline-block')

        a.classes.add('v-gvml-push', a.styleGroup)
