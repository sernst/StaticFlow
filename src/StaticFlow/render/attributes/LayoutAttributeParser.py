# LayoutAttributeParser.py
# (C)2012-2013
# Scott Ernst

from pyaid.ArgsUtils import ArgsUtils
from pyaid.color.ColorValue import ColorValue
from pyaid.reflection.Reflection import Reflection

from StaticFlow.render.enum.GeneralSizeEnum import GeneralSizeEnum
from StaticFlow.render.enum.LineTypesEnum import LineTypesEnum
from StaticFlow.render.attributes.AttributeUtils import AttributeUtils
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.attributes.UnitAttribute import UnitAttribute
from StaticFlow.render.error.MarkupAttributeError import MarkupAttributeError

#___________________________________________________________________________________________________ LayoutAttributeParser
class LayoutAttributeParser(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _PAD_VALUES = [0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

#___________________________________________________________________________________________________ parsePadding
    @classmethod
    def parsePadding(cls, attrs, apply =False, overrides =None, extract = False, group =None,
                     allowFailure =False, defaultValue =None):
        pad, keyData = attrs.get(
            TagAttributesEnum.PADDING,
            defaultValue=ArgsUtils.get('paddingDef', defaultValue, overrides),
            overrides=overrides,
            extract=extract,
            returnKey=True
        )

        if not pad:
            return None

        try:
            if isinstance(pad, basestring):
                pad = pad.lower().replace(u' ', '')
                out = AttributeUtils.parseSizeEnumValues(
                    source=pad,
                    values=cls._PAD_VALUES,
                    minValue=0.0,
                    maxValue=5.0
                )

                if isinstance(out, UnitAttribute):
                    out.setDefaultUnit(u'em')
                    out = out.valueAndUnit
                elif out:
                    out = unicode(out) + u'em'
            else:
                out = []
                for p in pad:
                    pout = AttributeUtils.parseSizeEnumValues(
                        source=p,
                        values=cls._PAD_VALUES,
                        minValue=0.0,
                        maxValue=5.0
                    )

                    if pout:
                        if isinstance(pout, UnitAttribute):
                            pout.setDefaultUnit(u'em')
                            pout = out.valueAndUnit
                        elif pout:
                            pout = unicode(pout) + u'em'
                        out.append(pout)

                out = u' '.join(out)
        except Exception, err:
            if not allowFailure:
                MarkupAttributeError(
                    tag=attrs.tag,
                    errorDef=MarkupAttributeError.BAD_ATTRIBUTE_VALUE,
                    attribute=keyData[0] if keyData else TagAttributesEnum.PADDING[0],
                    attributeData=keyData[1] if keyData else None,
                    attributeGroup=TagAttributesEnum.PADDING,
                    rawValue=pad
                ).log()
            return None

        if out and apply:
            attrs.styles.add('padding', out, attrs.styleGroup if not group else group)

        return out

#___________________________________________________________________________________________________ parseAlignment
    @classmethod
    def parseAlignment(cls, attrs, apply =False, overrides =None, extract =False, group =None):
        align = attrs.getAsKeyword(
            TagAttributesEnum.ALIGNMENT,
            ArgsUtils.get('alignDef', None, overrides),
            overrides)

        if align in ['right', 'r']:
            out = u'right'
        elif align in ['center', 'c']:
            out = u'center'
        elif align in ['left', 'l']:
            out = u'left'
        else:
            out = None

        if apply and out:
            attrs.styles.add('text-align', out, group)

        if extract:
            attrs.remove(TagAttributesEnum.ALIGNMENT)

        return out

#___________________________________________________________________________________________________ parseScale
    @classmethod
    def parseScale(cls, attrs, apply =False, overrides =None, extract =False, useSizeKeys =False,
                   group =None):
        """Doc..."""

        if useSizeKeys:
            keys = TagAttributesEnum.SCALE +  TagAttributesEnum.SIZE
        else:
            keys = TagAttributesEnum.SCALE

        size = attrs.get(keys, None, overrides)

        if size:
            size, bends = AttributeUtils.getValueAndBendCount(size)

            if size.isdigit():
                size = unicode(size) + u'em'
            else:
                sizeUnit = UnitAttribute.createIfValid(size, defaultUnit='em')
                if sizeUnit:
                    size = unicode(sizeUnit.valueAndUnit)
                    attrs.styles.add('font-size', size)
                else:
                    size = AttributeUtils.getAsTShirtEnum(size)
                    if size == GeneralSizeEnum.xxsmall[0]:
                        size = unicode(AttributeUtils.bendValue(0.6, bends, 0.2, 0.8)) + u'em'
                    elif size == GeneralSizeEnum.xsmall[0]:
                        size = unicode(AttributeUtils.bendValue(0.8, bends, 0.6, 1.0)) + u'em'
                    elif size == GeneralSizeEnum.small[0]:
                        size = unicode(AttributeUtils.bendValue(1.0, bends, 0.8, 1.2)) + u'em'
                    elif size == GeneralSizeEnum.medium[0]:
                        size = unicode(AttributeUtils.bendValue(1.2, bends, 1.0, 1.5)) + u'em'
                    elif size == GeneralSizeEnum.large[0]:
                        size = unicode(AttributeUtils.bendValue(1.5, bends, 1.2, 1.8)) + u'em'
                    elif size == GeneralSizeEnum.xlarge[0]:
                        size = unicode(AttributeUtils.bendValue(1.8, bends, 1.5, 2.2)) + u'em'
                    elif size == GeneralSizeEnum.xxlarge[0]:
                        size = unicode(AttributeUtils.bendValue(2.2, bends, 1.8, 3.0)) + u'em'
                    else:
                        size = None

            if size and apply:
                attrs.styles.add('font-size', size, group)

        if extract:
            attrs.remove(keys)

        return size

#___________________________________________________________________________________________________ parseBorder
    @classmethod
    def parseBorder(cls, attrs, apply =False, overrides =None, extract =False, group =None,
                    defaultColor =None):
        keys = TagAttributesEnum.BORDER

        borderColor = None
        borderSize  = None
        borderStyle = None

        useBorder = attrs.getAsBool(keys, None, overrides, True)
        if useBorder is None:
            border = attrs.get(keys, None, overrides)
            if not border:
                useBorder = False
            else:
                useBorder = True

                if not isinstance(border, list):
                    border = [border]

                for item in border:
                    if borderSize is None:
                        unitItem = UnitAttribute.createIfValid(item, 'px')
                        if unitItem:
                            borderSize = unitItem.valueAndUnit
                            continue

                    if borderStyle is None:
                        found =False
                        for lineType in Reflection.getReflectionList(LineTypesEnum):
                            if item in lineType[1]:
                                borderStyle = lineType[0]
                                found       = True
                                break
                        if found:
                            continue

                    if borderColor is None:
                        color = attrs.convertToColorValue(item, None)
                        if color:
                            borderColor = color

        if extract:
            attrs.remove(keys)

        if not useBorder:
            return None

        if borderColor is None:
            if defaultColor is None:
                borderColor = attrs.backColors.borderColor.web
            elif isinstance(defaultColor, ColorValue):
                borderColor = defaultColor.web
            else:
                borderColor = defaultColor
        else:
            borderColor = borderColor.web

        border = u' '.join([
            borderSize if borderSize else '1px',
            borderStyle if borderStyle else 'solid',
            borderColor
        ])

        if apply:
            attrs.styles.add('border', border, group)

        return border

