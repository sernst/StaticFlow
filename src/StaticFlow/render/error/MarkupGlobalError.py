# MarkupGlobalError.py
# (C)2012-2013
# Scott Ernst

from pyaid.ArgsUtils import ArgsUtils

from StaticFlow.render.error.MarkupError import MarkupError

#___________________________________________________________________________________________________ MarkupGlobalError
class MarkupGlobalError(MarkupError):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    READ_FAILURE = MarkupError.ERROR_DEFINITION_NT(
        u'read-failure',
        u'Render Read Failure',
        u'Unable to read the markup.')

    FICTIONAL_TAG = MarkupError.ERROR_DEFINITION_NT(
        u'fictional-tag',
        u'Fictional Tag',
        u'Unknown tag.')

    UNMATCHED_CLOSE_TAG = MarkupError.ERROR_DEFINITION_NT(
        u'unmatched-close-tag',
        u'Missing Closed Tag',
        u'Unmatched closing tag.')

    TAG_CREATION_FAILED = MarkupError.ERROR_DEFINITION_NT(
        u'tag-create-failure',
        u'Tag Creation Failed',
        u'Unable to create the tag with the specified attributes.')

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        ArgsUtils.addIfMissing('errorDef', self.READ_FAILURE, kwargs, True)
        MarkupError.__init__(self, **kwargs)

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


