# AttributeUtils.py
# (C)2012-2013
# Scott Ernst

import re

from pyaid.reflection.Reflection import Reflection

from StaticFlow.render.enum.GeneralSizeEnum import GeneralSizeEnum
from StaticFlow.render.attributes.UnitAttribute import UnitAttribute

#___________________________________________________________________________________________________ AttributeUtils
class AttributeUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _BEND_FINDER = re.compile('[+-]+$')

#___________________________________________________________________________________________________ _getValueAndBendCount
    @classmethod
    def getValueAndBendCount(cls, value):
        if not isinstance(value, basestring):
            return value, 0

        res = cls._BEND_FINDER.search(value)
        if res:
            cBend = 0
            bends = res.group()
            for i in range(len(bends)):
                cBend += 1 if bends[i:i+1] == '+' else -1
            return value[:-len(bends)], max(-3, min(3, cBend))
        else:
            return value, 0

#___________________________________________________________________________________________________ bendValue
    @classmethod
    def bendValue(cls, value, bendCount, previousValue, nextValue, asInt =False):
        if not bendCount:
            return value

        v = float(value)
        if bendCount > 0:
            return v + float(bendCount)/4.0*(float(nextValue) - v)

        result = v - float(abs(bendCount))/4.0*(v - float(previousValue))

        if asInt:
            return int(round(result))

        return result

#___________________________________________________________________________________________________ _getAsTShirtEnum
    @classmethod
    def getAsTShirtEnum(cls, value, defaultEnum =u'none'):
        value = value.lower().replace(u' ', u'')
        for enum in Reflection.getReflectionList(GeneralSizeEnum):
            if value in enum[1]:
                return value

        return defaultEnum

#___________________________________________________________________________________________________ parseSizeEnumValues
    @classmethod
    def parseSizeEnumValues(cls, source, values, minValue =None, maxValue =None, noneValue =None,
                            asInt =False):
        if source is None:
            return None

        source, bends = AttributeUtils.getValueAndBendCount(source)
        source = source.lower().replace(u' ', u'')

        if minValue is None:
            minValue = max(0.0, float(values[0]) - (float(values[1]) - float(values[0])))

        if maxValue is None:
            maxValue = float(values[-1]) + (float(values[-1]) - float(values[-2]))

        if source in GeneralSizeEnum.xxsmall[1]:
            p = cls.bendValue(
                values[0], bends, minValue, values[1], asInt=asInt
            )
        elif source in GeneralSizeEnum.xsmall[1]:
            p = cls.bendValue(
                values[1], bends, values[0], values[2], asInt=asInt
            )
        elif source in GeneralSizeEnum.small[1]:
            p = cls.bendValue(
                values[2], bends, values[1], values[3], asInt=asInt
            )
        elif source in GeneralSizeEnum.medium[1]:
            p = cls.bendValue(
                values[3], bends, values[2], values[4], asInt=asInt
            )
        elif source in GeneralSizeEnum.large[1]:
            p = cls.bendValue(
                values[4], bends, values[3], values[5], asInt=asInt
            )
        elif source in GeneralSizeEnum.xlarge[1]:
            p = cls.bendValue(
                values[5], bends, values[4], values[6], asInt=asInt
            )
        elif source in GeneralSizeEnum.xxlarge[1]:
            p = cls.bendValue(
                values[6], bends, values[5], maxValue
            )
        elif source in GeneralSizeEnum.none[1]:
            if bends > 0:
                p = cls.bendValue(
                    minValue, bends, minValue, values[0])
            else:
                p = noneValue
        elif source:
            p = UnitAttribute.createIfValid(source, unitType=(int if asInt else float))
        else:
            p = None

        return p

