# MarkupTagError.py
# (C)2012-2013
# Scott Ernst

from pyaid.ArgsUtils import ArgsUtils

from StaticFlow.render.error.MarkupError import MarkupError

#___________________________________________________________________________________________________ MarkupTagError
class MarkupTagError(MarkupError):

#===================================================================================================
#                                                                                       C L A S S

    READ_FAILURE    = 'tag-read-failure'
    UNCLOSED_TAG    = 'unclosed-tag'
    CORRUPT_ATTRS   = 'corrupt-attributes'
    RENDER_FAILURE  = 'render-failure'
    PREMATURE_CLOSE = 'incorrect-close-order'

    _DEFAULT_CODE   = 'tag-read-failure'

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        """Creates a new instance of MarkupTagError."""

        self._errorAtEnd = ArgsUtils.extract('errorAtEnd', False, kwargs)

        MarkupError.__init__(self, defaultCode=MarkupTagError._DEFAULT_CODE, **kwargs)

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
