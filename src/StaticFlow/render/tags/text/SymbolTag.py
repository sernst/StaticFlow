# SymbolTag.py
# (C)2012
# Scott Ernst

from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.MarkupTag import MarkupTag

#___________________________________________________________________________________________________ SymbolTag
class SymbolTag(MarkupTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG           = 'symbol'
    TEMPLATE      = 'markup/spanBase.mako'
    BLOCK_DISPLAY = False
    PRIMARY_ATTR  = TagAttributesEnum.VALUE[0]

    SYMBOLS = [
        ['&cent;', 'cent', 'cents'],
        ['&pound;', 'pound'],
        ['&curren;', 'currency'],
        ['&yen;', 'yen'],
        ['&brvbar;', 'brokenbar','brokebar'],
        ['&sect;', 'section'],
        ['&copy;', 'copy', 'copyright', '(c)', 'c'],
        ['&laquo;', 'leftdoublearrow'],
        ['&reg;', 'register', 'registermark', '(r)', 'r'],
        ['&deg;', 'degree'],
        ['&plusmn;', 'plusminus'],
        ['&sup2;', 'squared'],
        ['&sup3;', 'cubed'],
        ['&micro;', 'micro'],
        ['&para;', 'paragraph'],
        ['&middot;', 'dot'],
        ['&raquo;', 'rightdoublearrow'],
        ['&frac14;', 'quarter'],
        ['&frac12;', 'half'],
        ['&frac34;', 'threequarter', 'threequarters'],
        ['&times;', 'times', 'multiply', 'multiplication'],
        ['&#8240', 'perthousand', 'perk'],
        ['&#8364;', 'euro', 'euros'],
        ['&#8482;', 'trademark', 'tm'],
        ['&infin;', 'infinity'],
        ['&ang;', 'angle'],
        ['&ne;', 'notequal', 'unequal'],
        ['&bull;', 'bullet'],
        ['&dagger;', 'dagger'],
        ['&Dagger;', 'doubledagger']
    ]

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        t = TagAttributesEnum
        return MarkupTag.getAttributeList() + t.SYMBOL + t.COLOR

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a = self.attrs

        value = a.getAsKeyword(
            TagAttributesEnum.VALUE + TagAttributesEnum.SYMBOL,
            None,
            kwargs
        )

        self._addColorToGroup(a.styleGroup)

        for s in SymbolTag.SYMBOLS:
            if value in s[1:]:
                a.content = s[0]
                break
