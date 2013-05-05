# MarkupGlobalError.py
# (C)2012-2013
# Scott Ernst

from StaticFlow.render.error.MarkupError import MarkupError

#___________________________________________________________________________________________________ MarkupGlobalError
class MarkupGlobalError(MarkupError):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    READ_FAILURE        = 'read-failure'
    FICTIONAL_TAG       = 'fictional-tag'
    UNMATCHED_CLOSE_TAG = 'unmatched-close-tag'
    TAG_CREATION_FAILED = 'tag-create-failure'

    _DEFAULT_CODE       = 'read-failure'

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        MarkupError.__init__(self, defaultCode=MarkupGlobalError._DEFAULT_CODE, **kwargs)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getErrorDOMData
    def _getErrorDOMData(self, data):
        data['errorType'] = u'Global Syntax Error'
        return data

#___________________________________________________________________________________________________ _populateData
    def _populateData(self):
        """Doc..."""

        if not self._block:
            return

        proc  = self._processor
        block = self._block

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


