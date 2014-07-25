# FooterTag.py
# (C)2012-2013
# Scott Ernst

from pyaid.color.ColorValue import ColorValue
from pyaid.ArgsUtils import ArgsUtils
from StaticFlow.render.enum.GeneralSizeEnum import GeneralSizeEnum
from StaticFlow.render.attributes.LayoutAttributeParser import LayoutAttributeParser
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.MarkupBlockTag import MarkupBlockTag

#___________________________________________________________________________________________________ FooterTag
class FooterTag(MarkupBlockTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'footer'
    TEMPLATE       = 'markup/box/default.mako'
    BLOCK_DISPLAY  = True
    STRIP_POLICY   = MarkupBlockTag.STRIP_ALL
    NEWLINE_POLICY = MarkupBlockTag.BREAK_ON_NEWLINES
    INSERTS_TAG    = False

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
        return MarkupBlockTag.getAttributeList() + t.COLOR + t.ALIGNMENT + t.PADDING \
               + t.COLOR + t.REACH + t.SCALE + t.BORDER

#___________________________________________________________________________________________________ render
    def render(self, **kwargs):
        self._processor.footerDom = super(FooterTag, self).render()
        return u''

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

        #-------------------------------------------------------------------------------------------
        # BACKGROUND COLOR
        if not ArgsUtils.get('skipBackground', False, kwargs):
            if isinstance(color, ColorValue):
                a.styles.add('background-color', color.web, a.styleGroup)
            elif a.explicitAccent or a.themeChanged:
                self.useBackground()

        a.classes.add('sfml-push', a.styleGroup)
