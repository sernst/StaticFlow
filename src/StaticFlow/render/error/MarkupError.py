# MarkupError.py
# (C)2012-2013
# Scott Ernst

import markupsafe

from pyaid.ArgsUtils import ArgsUtils

#___________________________________________________________________________________________________ MarkupError
class MarkupError(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, defaultCode, **kwargs):
        """Creates a new instance of MarkupError."""

        self._code = ArgsUtils.get('code', defaultCode, kwargs)
        if not self._code:
            self._code = defaultCode

        self._tag        = ArgsUtils.get('tag', None, kwargs)
        self._block      = ArgsUtils.get('block', self._tag.block if self._tag else None, kwargs)
        self._processor  = ArgsUtils.get('processor', self._tag.processor if self._tag else None, kwargs)
        self._label      = ArgsUtils.get('label', None, kwargs)
        self._message    = ArgsUtils.get('message', None, kwargs)
        self._critical   = ArgsUtils.get('critical', False, kwargs)
        self._quotedInfo = ArgsUtils.get('quotedInfo', None, kwargs)

        replacements    = ArgsUtils.get('replacements', [], kwargs)
        replacements.append([u'#TAG#', unicode(self._tag.tagName if self._tag else u'???')])


        self._label     = ArgsUtils.get('label', 'Unknown Error', kwargs)
        self._message   = ArgsUtils.get('message', 'This error is a mystery!', kwargs)

        for r in replacements:
            if self._message:
                self._message = self._message.replace(unicode(r[0]), unicode(r[1]))

            if self._label:
                self._label = self._label.replace(unicode(r[0]), unicode(r[1]))

        self._verbose   = ArgsUtils.get('verbose', False, kwargs)
        self._line      = None
        self._character = None
        self._source    = None
        self._logSource = None
        self._populateData()

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: quotedInfo
    @property
    def quotedInfo(self):
        return self._quotedInfo.strip() if self._quotedInfo else None

#___________________________________________________________________________________________________ GS: critical
    @property
    def critical(self):
        return self._critical

#___________________________________________________________________________________________________ GS: code
    @property
    def code(self):
        return self._code
    @code.setter
    def code(self, value):
        self._code = value

#___________________________________________________________________________________________________ GS: label
    @property
    def label(self):
        return self._label
    @label.setter
    def label(self, value):
        self._label = value

#___________________________________________________________________________________________________ GS: message
    @property
    def message(self):
        return self._message
    @message.setter
    def message(self, value):
        self._message = value

#___________________________________________________________________________________________________ GS: line
    @property
    def line(self):
        return self._line if self._line else 0

#___________________________________________________________________________________________________ GS: character
    @property
    def character(self):
        return self._character if self._character else 0

#___________________________________________________________________________________________________ GS: tag
    @property
    def tag(self):
        return self._tag

#___________________________________________________________________________________________________ GS: tag
    @property
    def processor(self):
        return self._processor

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ echo
    def echo(self):
        if self._processor and self._processor.log.trace:
            self._processor.log.write(self.getLogData())
        else:
            print self.getLogData()

#___________________________________________________________________________________________________ getLogData
    def getLogData(self):
        logs = [
            unicode(self.__class__.__name__),
            u'Code: ' + unicode(self.code),
            u'Label: ' + unicode(self.label),
            u'Location: %s.%s' % (unicode(self.line), unicode(self.character)),
            u'Block: ' + unicode(self._block),
            u'Tag: ' + unicode(self._tag),
            u'Info: ' + unicode((u'\n' + unicode(self.quotedInfo)) if self.quotedInfo else None)
        ] + self._getLogData()
        logs.append(u'Source: ' + unicode(self._logSource))
        return logs

#___________________________________________________________________________________________________ log
    def log(self):
        """Doc..."""

        if not self._processor:
            print "No processor available to log the error. Error aborted."
            return

        if self._verbose:
            self._processor.log.write(self.getLogData())
        self._processor.addRenderError(self)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getLogData
    def _getLogData(self):
        """Doc..."""
        return []

#___________________________________________________________________________________________________ _getErrorDOMData
    def _getErrorDOMData(self, data):
        return data

#___________________________________________________________________________________________________ _populateData
    def _populateData(self):
        pass

#___________________________________________________________________________________________________ _createLineDisplay
    def _createLineDisplay(self, position, lastLineIndex, line, character, startSplit, endSplit):
        proc          = self._processor
        nextLineIndex = proc.source[position:].find('\n')
        if nextLineIndex == -1:
            nextLineIndex = None
        else:
            nextLineIndex += position

        s = proc.source[lastLineIndex+1:nextLineIndex]
        s = s[:startSplit] + u'#OPEN#' + s[startSplit:endSplit] + u'#CLOSE#' + s[endSplit:]

        lines = self._createPreviousLines(line, lastLineIndex) + [[unicode(line + 1), s]] + \
                self._createNextLines(line, nextLineIndex)

        lineNumberLength = 0
        for l in lines:
            lineNumberLength = max(lineNumberLength, len(l[0]))

        out = []
        for i in range(0,len(lines)):
            l        = lines[i]
            out.append(unicode(l[0]).rjust(lineNumberLength) + u'  ' + unicode(l[1]).strip(u'\n'))
        s = u'#BR#'.join(out)

        if not isinstance(s, unicode):
            s = unicode(s)

        try:
            s = unicode(markupsafe.escape(s))
        except Exception, err:
            self._processor.log.writeError([
                u'Markupsafe escaping failure',
                u'Source: ' + s
            ], err)
            s = u'Unable to display source code...'
        self._logSource = s

        s = s.replace(u'#OPEN#', u'<span class="v-vmldebug-errorHighlight">') \
             .replace(u'#CLOSE#', u'</span>') \
             .replace(u'#BR#', u'<br />')

        self._character = character + 1
        self._line      = line + 1
        self._source    = s

#___________________________________________________________________________________________________ _createPreviousLines
    def _createPreviousLines(self, line, endIndex, count =2):
        out  = []
        proc = self._processor

        while len(out) < count:
            previousLine = None
            if line > 1:
                try:
                    index        = max(0, proc.source[:endIndex].rindex(u'\n'))
                    previousLine = proc.source[index+1:endIndex]
                    endIndex     = index
                except Exception, err:
                    proc.log.writeError('Previous line failure', err)
                    return out
            elif line == 1:
                previousLine = proc.source[:endIndex]
            else:
                return out

            out.insert(0, [unicode(line), previousLine])
            line -= 1

        return out

#___________________________________________________________________________________________________ _createNextLines
    def _createNextLines(self, line, startIndex, count =2):
        out  = []
        proc = self._processor

        while startIndex and len(out) < count:
            nextLine = None
            if startIndex < len(proc.source):
                try:
                    index      = proc.source[startIndex+1:].index(u'\n') + startIndex + 1
                    nextLine   = proc.source[startIndex+1:index]
                    startIndex = index
                except Exception, err:
                    nextLine   = proc.source[startIndex:].rstrip()
                    startIndex = None
            else:
                return out

            line += 1
            out.append([unicode(line + 1), nextLine])

        return out

