# MarkupTagError.py
# (C)2012-2013
# Scott Ernst

from pyaid.ArgsUtils import ArgsUtils

from StaticFlow.render.error.MarkupError import MarkupError

#___________________________________________________________________________________________________ MarkupTagError
class MarkupTagError(MarkupError):

#===================================================================================================
#                                                                                       C L A S S

    MISSING_URL = MarkupError.ERROR_DEFINITION_NT(
        u'missing-url-attribute',
        u'Missing URL Attribute',
        u'No URL attribute was specified in the "#TAG#" tag.')

    READ_FAILURE = MarkupError.ERROR_DEFINITION_NT(
        u'tag-read-failure',
        u'Invalid Tag "#TAG"',
        u'Unable to read the "#TAG#" tag.')

    UNCLOSED_TAG = MarkupError.ERROR_DEFINITION_NT(
        u'unclosed-tag',
        u'Unclosed #TAG# Tag',
        u'The "#TAG#" tag has no closed pair.')

    CORRUPT_ATTRS = MarkupError.ERROR_DEFINITION_NT(
        u'corrupt-attributes',
        u'Corrupt Attributes',
        u'One or more attributes of the "#TAG#" tag are invalid.')

    RENDER_FAILURE = MarkupError.ERROR_DEFINITION_NT(
        u'render-failure',
        u'Read Failure',
        u'Unable to read the "#TAG#" tag.')

    PREMATURE_CLOSE = MarkupError.ERROR_DEFINITION_NT(
        u'incorrect-close-order',
        u'Tags out of Order',
        u'The #TAG# has been closed in the incorrect order.')

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        """Creates a new instance of MarkupTagError."""

        self._errorAtEnd = ArgsUtils.extract('errorAtEnd', False, kwargs)

        ArgsUtils.addIfMissing('errorDef', self.READ_FAILURE, kwargs, True)
        MarkupError.__init__(self, **kwargs)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getErrorDOMData
    def _getErrorDOMData(self, data):
        data['errorType'] = u'Tag Syntax Error'
        return data

#___________________________________________________________________________________________________ _populateData
    def _populateData(self):
        """Doc..."""

        if not self._tag:
            return

        proc  = self._tag.processor
        if self._errorAtEnd and self._tag.closeBlock:
            block = self._tag.closeBlock
        else:
            block = self._tag.block

        if not block:
            return

        # Determine the character location
        position = block.originalStart
        line     = proc.source[:position].count('\n')

        if line > 0:
            lastLineIndex = proc.source[:position].rindex('\n')
            character     = len(proc.source[lastLineIndex+1:position])
        else:
            lastLineIndex = -1
            character     = len(proc.source[:position])

        startSplit = character
        endSplit   = character + (block.originalEnd - block.originalStart)

        self._createLineDisplay(position, lastLineIndex, line, character, startSplit, endSplit)
