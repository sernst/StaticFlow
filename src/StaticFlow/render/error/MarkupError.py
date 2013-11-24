# MarkupError.py
# (C)2012-2013
# Scott Ernst

from collections import namedtuple

import markupsafe

from pyaid.ArgsUtils import ArgsUtils
from pyaid.debug.Logger import Logger

#___________________________________________________________________________________________________ MarkupError
class MarkupError(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    ERROR_DEFINITION_NT = namedtuple('ERROR_DEFINITION_NT', ['code', 'label', 'message'])

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        """Creates a new instance of MarkupError."""

        self._thrown     = Logger.getFormattedStackTrace(2, 3)
        self._definition = ArgsUtils.get('errorDef', None, kwargs)
        self._tag        = ArgsUtils.get('tag', None, kwargs)
        self._block      = ArgsUtils.get('block', self._tag.block if self._tag else None, kwargs)
        self._processor  = ArgsUtils.get('processor', self._tag.processor if self._tag else None, kwargs)
        self._code       = ArgsUtils.get('code', self._definition.code, kwargs, allowNone=False)
        self.label       = ArgsUtils.get('label', self._definition.label, kwargs, allowNone=False)
        self.message     = ArgsUtils.get('message', self._definition.message, kwargs, allowNone=False)
        self._critical   = ArgsUtils.get('critical', False, kwargs)

        replacements = ArgsUtils.getAsList('replacements', kwargs)
        replacements.append([u'#TAG#', unicode(self._tag.tagName if self._tag else u'???')])

        for r in replacements:
            if self.message:
                self.message = self.message.replace(unicode(r[0]), unicode(r[1]))

            if self.label:
                self.label = self.label.replace(unicode(r[0]), unicode(r[1]))

        self._verbose   = ArgsUtils.get('verbose', False, kwargs)
        self._line      = None
        self._character = None
        self._source    = None
        self._logSource = None
        self._populateData()

#===================================================================================================
#                                                                                   G E T / S E T

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
        data = self.getLogData()
        if self._processor and self._processor.logger.trace:
            self._processor.logger.write(data)
        else:
            print data

#___________________________________________________________________________________________________ getHtmlLogDisplay
    def getHtmlLogDisplay(self):
        data = self.getLogData()
        out = [
            u'<div style="color:#FF6666;font-size:20px;">[RENDER ERROR]: %s</div>' % (data['label']),
            u'<div style="font-size:14px">',
            u'<div>%s</div>' % data['message'],
            u'</div><br />',
            u'<div style="font-size:14px;">On line <span style="font-weight:bold">#%s.%s</span>' % (
                data['location'][0],
                data['location'][1] ) ]

        if self._processor.filename:
            out[-1] += u' of <span style="font-weight:bold;">%s</span></div>' \
                % self._processor.filename

            if self._processor.filePath:
                out.append(
                    u'<div style="color:#666666;font-size:11px;">%s</div><br />'
                    % self._processor.filePath)
        else:
            out.append(u'</div><br />')

        if self._source:
            out.append(
                u'<div style="font-size:12px;font-color:#333333;">%s</div><br />' % self._source)

        out += self._getHtmlLogDisplay()

        out += [
            u'<ul style="color:#333333;">',
            u'<li>Code: %s</li>' % data['code'],
            u'<li>Type: %s</li>' % data['type'],
            u'<li>Tag: %s</li>' % data['tag'],
            u'<li>Block: %s</li>' % data['block'],
            u'</ul>',
            u'<div style="font-size:10px;color:#AAAAAA"><span style="font-weight:bold">Thrown At:</span>%s</div>' %
                self._thrown.replace(
                    '\n', u'<br />').replace(
                    '  ', '&nbsp;&nbsp;').replace(
                    '\t', '&nbsp;&nbsp;&nbsp;&nbsp;')]

        return u'\n'.join(out)

#___________________________________________________________________________________________________ getLogData
    def getLogData(self):
        logs = {
            'type':unicode(self.__class__.__name__),
            'code':unicode(self.code),
            'label':unicode(self.label),
            'location':(self.line, self.character),
            'block':str(self._block),
            'tag':str(self._tag),
            'message':unicode(self.message) }

        logs = dict(logs.items() + self._getLogData().items())
        logs['source'] = unicode(self._logSource)
        return logs

#___________________________________________________________________________________________________ log
    def log(self):
        """Doc..."""

        if not self._processor:
            print "No processor available to log the error. Error aborted."
            print self.getLogData()
            return

        if self._verbose:
            self._processor.logger.write(self.getLogData())
        self._processor.addRenderError(self)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getHtmlLogDisplay
    def _getHtmlLogDisplay(self):
        return []

#___________________________________________________________________________________________________ _getLogData
    def _getLogData(self):
        """Doc..."""
        return dict()

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
            self._processor.logger.writeError([
                u'Markupsafe escaping failure',
                u'Source: ' + s
            ], err)
            s = u'Unable to display source code...'
        self._logSource = s

        s = s.replace(u'#OPEN#', u'<span style="color:#FF3333;font-weight:bold;">') \
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
                    proc.logger.writeError('Previous line failure', err)
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

