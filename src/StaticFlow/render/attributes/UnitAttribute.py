# UnitAttribute.py
# (C)2012-2013
# Scott Ernst

import re

#___________________________________________________________________________________________________ UnitAttribute
class UnitAttribute(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _VALUE_UNIT_PATTERN = re.compile('^(?P<value>-?[0-9\.]+)(?P<unit>[A-Za-z%]*)')
    _UNIT_PATTERN  = re.compile('[^0-9\.-]+$')
    _VALUE_PATTERN = re.compile('^[0-9\.-]+')

#___________________________________________________________________________________________________ __init__
    def __init__(self, value, unit =None, defaultUnit =None, unitType =None):
        """Creates a new instance of UnitAttribute."""

        # Parse the value and unit if the source is a string
        if isinstance(value, basestring):
            if unit is None:
                res = UnitAttribute._UNIT_PATTERN.search(value)
                if res:
                    unit = unicode(res.group())
                else:
                    unit = None

            value = UnitAttribute._VALUE_PATTERN.match(value).group()

        # Force value to conform to specified or default numeric unit
        self._value   = float(value) if unitType is None else unitType(value)
        self._srcUnit = unit

        self._defaultUnit = defaultUnit
        self._unit        = unit
        self._updateUnit(unit, defaultUnit)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: valueAndUnit
    @property
    def valueAndUnit(self):
        return str(self.value) + str(self.unit)

#___________________________________________________________________________________________________ GS: value
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, value):
        self._value = value

#___________________________________________________________________________________________________ GS: unit
    @property
    def unit(self):
        return self._unit
    @unit.setter
    def unit(self, value):
        self._unit = value

#___________________________________________________________________________________________________ GS: isPixels
    @property
    def isPixels(self):
        return self.unit == u'px'

#___________________________________________________________________________________________________ GS: isDecimal
    @property
    def isDecimal(self):
        return self.unit == u'' and int(self.value) != self.value

#___________________________________________________________________________________________________ GS: isEm
    @property
    def isEm(self):
        return self.unit == u'em'

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ setDefaultUnit
    def setDefaultUnit(self, defaultUnit):
        self._defaultUnit = defaultUnit
        self._updateUnit(self._unit, self._defaultUnit)

#___________________________________________________________________________________________________ isValid
    @classmethod
    def isValid(cls, value):
        return cls._VALUE_UNIT_PATTERN.match(value) is not None

#___________________________________________________________________________________________________ createIfValid
    @classmethod
    def createIfValid(cls, value, unit =None, defaultUnit =None, unitType =None):
        res = cls._VALUE_UNIT_PATTERN.match(value)
        if res is None:
            return None

        try:
            num = float(res.group('value'))
        except Exception, err:
            return None

        try:
            unit = res.group('unit')
            if not unit:
                unit = defaultUnit
        except Exception, err:
            return None

        return UnitAttribute(num, unit, defaultUnit, unitType)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _updateUnit
    def _updateUnit(self, unit, defaultUnit):
        if unit in [u'lines', u'line', u'ln']:
            self._unit = u'em'
        elif unit == u'%':
            self._value = float(self._value)/100.0
            self._unit  = u''
        elif unit is None:
            self._unit = defaultUnit if defaultUnit else u''
        else:
            self._unit = unit

        if unit == u'px':
            self._value = int(self._value)

#___________________________________________________________________________________________________ __str__
    def __repr__(self):
        return '<UnitAttribute | %s>' % str(self)

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        """Doc..."""
        return str(self.value) + str(self.unit)

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        """Doc..."""
        return unicode(self.value) + unicode(self.unit)


