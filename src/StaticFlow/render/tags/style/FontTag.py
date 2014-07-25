# FontTag.py
# (C)2012-2013
# Scott Ernst

from pyaid.enum.FontFamilyEnum import FontFamilyEnum
from StaticFlow.render.attributes.InsertAttributeParser import InsertAttributeParser

from StaticFlow.render.enum.FontFamilyKeywordEnum import FontFamilyKeywordEnum
from StaticFlow.render.enum.GeneralSizeEnum import GeneralSizeEnum
from StaticFlow.render.attributes.LayoutAttributeParser import LayoutAttributeParser
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.MarkupBlockTag import MarkupBlockTag

#___________________________________________________________________________________________________ FontTag
class FontTag(MarkupBlockTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'font'
    TEMPLATE       = 'markup/text/font.mako'
    STRIP_POLICY   = MarkupBlockTag.STRIP_NEWLINES
    NEWLINE_POLICY = MarkupBlockTag.BREAK_ON_NEWLINES
    PRIMARY_ATTR   = TagAttributesEnum.FONT[0]

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
        return MarkupBlockTag.getAttributeList() + t.NAME + t.COLOR + t.SIZE + t.FONT + t.SPACING + \
               t.LINE_SPACING + t.LETTER_SPACING + t.WORD_SPACING + t.BOLD + t.ITALIC + \
               t.ALIGNMENT + t.SCALE + t.TEXT + t.TEXT_PATH + t.TEXT_SECTION + t.SECTION \
               + t.PATH

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a = self.attrs

        result = InsertAttributeParser.parseText(self.attrs)
        self.attrs.render['text'] = u'' if not result else result

        self._addColorToGroup(a.styleGroup)
        LayoutAttributeParser.parseScale(a, True, kwargs, useSizeKeys=True)

        if LayoutAttributeParser.parseAlignment(a, True, kwargs) is not None:
            self._renderTemplate = 'markup/divBase.mako'

        bold = a.getAsBool(TagAttributesEnum.BOLD, None)

        italic = a.getAsBool(TagAttributesEnum.ITALIC, None )

        font = a.getAsEnumerated(
            TagAttributesEnum.FONT,
            FontFamilyKeywordEnum,
            None)

        fontFamily = getattr(FontFamilyEnum, font, None) if font else None

        lineSpacing = a.getAsEnumerated(
            TagAttributesEnum.LINE_SPACING + TagAttributesEnum.SPACING,
            GeneralSizeEnum,
            None,
            allowFailure=True)

        if lineSpacing is None:
            lineSpacing = a.getAsUnit(
                TagAttributesEnum.LINE_SPACING + TagAttributesEnum.SPACING,
                None)

        letterSpacing = a.getAsEnumerated(
            TagAttributesEnum.LETTER_SPACING,
            GeneralSizeEnum,
            None,
            allowFailure=True)

        if letterSpacing is None:
            letterSpacing = a.getAsUnit(
                TagAttributesEnum.LETTER_SPACING,
                None)

        wordSpacing = a.getAsEnumerated(
            TagAttributesEnum.WORD_SPACING,
            GeneralSizeEnum,
            None,
            allowFailure=True
        )
        if wordSpacing is None:
            wordSpacing = a.getAsUnit(
                TagAttributesEnum.WORD_SPACING,
                None
            )

        if fontFamily:
            a.styles.add('font-family', fontFamily, a.styleGroup)

        if isinstance(lineSpacing, basestring):
            if lineSpacing == GeneralSizeEnum.xxsmall[0]:
                lineSpacing = '0.6'
            elif lineSpacing == GeneralSizeEnum.xsmall[0]:
                lineSpacing = '0.8'
            elif lineSpacing == GeneralSizeEnum.small[0]:
                lineSpacing = '1.1'
            elif lineSpacing == GeneralSizeEnum.medium[0]:
                lineSpacing = '1.2'
            elif lineSpacing == GeneralSizeEnum.large[0]:
                lineSpacing = '1.5'
            elif lineSpacing == GeneralSizeEnum.xlarge[0]:
                lineSpacing = '2.0'
            elif lineSpacing == GeneralSizeEnum.xxlarge[0]:
                lineSpacing = '2.5'
            else:
                lineSpacing = None
        elif lineSpacing:
            lineSpacing = lineSpacing.value

        if lineSpacing:
            a.styles.add('line-height', lineSpacing, a.styleGroup)

        if isinstance(letterSpacing, basestring):
            if letterSpacing == GeneralSizeEnum.xxsmall[0]:
                letterSpacing = '-2px'
            elif letterSpacing == GeneralSizeEnum.xsmall[0]:
                letterSpacing = '-1px'
            elif letterSpacing == GeneralSizeEnum.small[0]:
                letterSpacing = '0'
            elif letterSpacing == GeneralSizeEnum.medium[0]:
                letterSpacing = '1px'
            elif letterSpacing == GeneralSizeEnum.large[0]:
                letterSpacing = '2px'
            elif letterSpacing == GeneralSizeEnum.xlarge[0]:
                letterSpacing = '3px'
            elif letterSpacing == GeneralSizeEnum.xxlarge[0]:
                letterSpacing = '4px'
            else:
                letterSpacing = None
        elif letterSpacing:
            letterSpacing = letterSpacing.valueAndUnit

        if letterSpacing:
            a.styles.add('letter-spacing', letterSpacing, a.styleGroup)

        if isinstance(wordSpacing, basestring):
            if wordSpacing == GeneralSizeEnum.xxsmall[0]:
                wordSpacing = '-2px'
            elif wordSpacing == GeneralSizeEnum.xsmall[0]:
                wordSpacing = '-1px'
            elif wordSpacing == GeneralSizeEnum.small[0]:
                wordSpacing = '0'
            elif wordSpacing == GeneralSizeEnum.medium[0]:
                wordSpacing = '1px'
            elif wordSpacing == GeneralSizeEnum.large[0]:
                wordSpacing = '2px'
            elif wordSpacing == GeneralSizeEnum.xlarge[0]:
                wordSpacing = '3px'
            elif wordSpacing == GeneralSizeEnum.xxlarge[0]:
                wordSpacing = '4px'
            else:
                wordSpacing = None
        elif wordSpacing:
            wordSpacing = wordSpacing.valueAndUnit

        if wordSpacing:
            a.styles.add('word-spacing', wordSpacing, a.styleGroup)

        if isinstance(bold, bool):
            if bold:
                a.classes.add('sfml-b', a.styleGroup)
            else:
                a.styles.add('font-weight', 'normal', a.styleGroup)

        if isinstance(italic, bool):
            if italic:
                a.classes.add('sfml-i', a.styleGroup)
            else:
                a.styles.add('font-style', 'normal', a.styleGroup)

