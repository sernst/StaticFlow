# MarkupAttributeError.py
# (C)2012-2013
# Scott Ernst

from pyaid.ArgsUtils import ArgsUtils

from StaticFlow.render.error.MarkupError import MarkupError

#___________________________________________________________________________________________________ MarkupAttributeError
class MarkupAttributeError(MarkupError):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    MISSING_ATTRIBUTE = MarkupError.ERROR_DEFINITION_NT(
        u'missing-attribute',
        u'Missing "#ATTR#" Attribute',
        u'The "#ATTR#" was not found in the "#TAG#" tag.')

    INVALID_ATTRIBUTE = MarkupError.ERROR_DEFINITION_NT(
        u'invalid-attribute',
        u'Invalid "#ATTR#" Attribute',
        u'The "#ATTR#" attribute in the "#TAG#" tag is unrecognized.')

    BAD_ATTRIBUTE_VALUE = MarkupError.ERROR_DEFINITION_NT(
        u'bad-attribute-value',
        u'Bad Attribute Value',
        u'Unable to read the value "#VAL#" of the "#ATTR#" attribute in the "#TAG#" tag.')

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        """Creates a new instance of MarkupAttributeError."""

        self._attribute         = ArgsUtils.get('attribute', None, kwargs)
        self._attrGroup         = ArgsUtils.get('attributeGroup', None, kwargs)
        self._rawValue          = ArgsUtils.get('rawValue', None, kwargs)
        self._value             = ArgsUtils.get('value', self._rawValue, kwargs)
        self._attrData          = ArgsUtils.get('attributeData', None, kwargs)
        self._attributeSource   = None

        replacements = ArgsUtils.getAsList('replacements', kwargs)
        replacements.append(
            [u'#ATTR#', unicode(self.attribute if self.attribute else u'???')])
        replacements.append(
            [u'#VAL#', unicode(self.value if self.value else u'???')])
        kwargs['replacements'] = replacements

        ArgsUtils.addIfMissing('errorDef', self.INVALID_ATTRIBUTE, kwargs, True)
        MarkupError.__init__(self, **kwargs)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: value
    @property
    def value(self):
        return self._value

#___________________________________________________________________________________________________ GS: rawValue
    @property
    def rawValue(self):
        return self._rawValue if self._rawValue else self._value

#___________________________________________________________________________________________________ GS: attribute
    @property
    def attribute(self):
        return self._attribute

#___________________________________________________________________________________________________ GS: attributeGroup
    @property
    def attributeGroup(self):
        return self._attrGroup

#___________________________________________________________________________________________________ GS: attributeSource
    @property
    def attributeSource(self):
        return self._attributeSource

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getLogData
    def _getLogData(self):
        """Doc..."""
        return {'attribute':unicode(self.attributeSource)}

#___________________________________________________________________________________________________ _getErrorDOMData
    def _getErrorDOMData(self, data):
        data['errorType'] = u'Attribute Syntax Error'
        return data

#___________________________________________________________________________________________________ _populateData
    def _populateData(self):
        """Doc..."""

        if not self._tag or not self._tag.block:
            return

        proc  = self._tag.processor
        block = self._tag.block
        index = 0

        if self._attrData:
            # Index offset due to the opening of the tag, i.e. '[#tagName '
            tagOffset  = 0 if self._tag.isProcedural else len(self._tag.tagName) + 3

            # Index offset due to the location of the attribute in the tag
            attrOffset = self._attrData['start']
        else:
            tagOffset  = 0
            attrOffset = 0

        # Determine the character location
        position = block.originalStart + tagOffset + attrOffset
        line     = proc.source[:position].count('\n')

        if line > 0:
            lastLineIndex = proc.source[:position].rindex('\n')
            character     = len(proc.source[lastLineIndex+1:position])
        else:
            lastLineIndex = -1
            character     = len(proc.source[:position])

        startSplit = character

        if self._attrData:
            self._attributeSource = self._attrData['data']
            endSplit              = character + len(self._attrData['data'])
        else:
            endSplit = character + (block.originalEnd - block.originalStart)

        self._createLineDisplay(position, lastLineIndex, line, character, startSplit, endSplit)

