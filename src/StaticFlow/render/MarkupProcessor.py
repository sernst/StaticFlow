# MarkupProcessor.py
# (C)2011-2013
# Scott Ernst

import re

from pyaid.ArgsUtils import ArgsUtils
from pyaid.string.StringUtils import StringUtils
from pyaid.text.BlockDefinition import BlockDefinition
from pyaid.text.BlockSyntaxEnum import BlockSyntaxEnum
from pyaid.text.TextAnalyzer import TextAnalyzer
from pyaid.web.DomUtils import DomUtils

from StaticFlow.render.error.MarkupGlobalError import MarkupGlobalError
from StaticFlow.render.error.MarkupTagError import MarkupTagError
from StaticFlow.render.tags.MarkupTag import MarkupTag
from StaticFlow.render.text.MarkupTextBlockUtils import MarkupTextBlockUtils

#___________________________________________________________________________________________________ MarkupProcessor
class MarkupProcessor(TextAnalyzer):
    """The MarkupProcessor class is responsible for parsing Vizme Markup Language (Markup) and
    converting it to HTML for display on the web."""

#===================================================================================================
#                                                                                       C L A S S

    DEFAULT_STYLE_SUFFIX = ''

    _WHITESPACE_KILLER_REGEX = re.compile('\s{2,}')

    _CONTINUE_LINE_PATTERN = re.compile('(->>|\\\\)[\s\t]*\n')

    _HTML_INSIDE_TAG_PATTERN = re.compile('(?P<tag><[^\s\t\n>/]+[^>]*>)')

    _HTML_PRE_TAG_WHITESPACE_PATTERN  = re.compile(
        '(?P<whitespace>[\s\t\n]+)(?P<tag><[^\n\t\s>]+[^>]*>)'
    )

    _HTML_POST_TAG_WHITESPACE_PATTERN = re.compile(
        '(?P<tag><[^\n\t\s>]+[^>]*>)(?P<whitespace>[\s\t\n]+)'
    )

    _STRIP_WHITESPACE_PATTERN = re.compile('(^[\s\t\n]+|[\s\t\n]+$)')

    _UNWANTED_NEWLINE_PATTERN = re.compile(
        '(?P<close>\[/#[A-Za-z0-9_#]+\])(?P<space>[\s\t\n]+)(?P<open>\[#[A-Za-z0-9_#]+)'
    )

    _STRIP_PATTERN = re.compile(
        '(^[\s\t\n]+)|(^[\n]*<br />[\n]*)|([\s\t\n]+$)|(^[\n]*<br />[\n]*$)'
    )

    _DIV_LINE_BREAK_PATTERN = re.compile(
        '(<br />[\s\t\n]*((?=<div)|(?=<script)))|(((?<=</div>)|(?<=</script>))[\s\t\n]*<br />)'
    )

#___________________________________________________________________________________________________ __init__
    def __init__(self, source, **kwargs):

        self.footerDom     = u''
        self.pageData      = ArgsUtils.get('pageData', None, kwargs)
        self.pageProcessor = ArgsUtils.get('pageProcessor', None, kwargs)

        debugData = ArgsUtils.extract('debugData', None, kwargs)
        blocks    = {
            'root':[
                MarkupTextBlockUtils.createMarkupCommentDef(BlockDefinition.BLOCKED),
                MarkupTextBlockUtils.createMarkupOpenDef('quote'),
                MarkupTextBlockUtils.createMarkupCloseDef(BlockDefinition.BLOCKED)
            ],
            'quote':[
                BlockDefinition.createQuoteDef(BlockDefinition.BLOCKED),
                BlockDefinition.createLiteralDef(BlockDefinition.BLOCKED)
            ]
        }

        self._renderErrors = []
        self._tagIndex     = -1

        super(MarkupProcessor, self).__init__(
            source,
            ArgsUtils.extract('debug', False, kwargs),
            blocks,
            debugData,
            stripSource=False,
            **kwargs)

        self._log.trace         = True
        self._result            = None
        self._anchors           = []
        self._tags              = []
        self._id                = StringUtils.getRandomString(8)
        self._css               = []
        self._js                = []
        self._radioArrays       = dict()
        self._patterns          = dict()
        self._groups            = dict()
        self._metadata          = ArgsUtils.getAsDict('metadata', kwargs)
        self._libraryIDs        = []
        self._autoTitle         = u''
        self._autoDescription   = u''
        self._allowModelCaching = False

        self.privateView = False

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: metadata
    @property
    def metadata(self):
        return self._metadata
    @metadata.setter
    def metadata(self, value):
        self._metadata = value

#___________________________________________________________________________________________________ GS: hasErrors
    @property
    def hasErrors(self):
        return len(self._renderErrors) > 0

#___________________________________________________________________________________________________ GS: renderErrors
    @property
    def renderErrors(self):
        return self._renderErrors

#___________________________________________________________________________________________________ GS: radioArrays
    @property
    def radioArrays(self):
        return self._radioArrays

#___________________________________________________________________________________________________ GS: groups
    @property
    def groups(self):
        return self._groups

#___________________________________________________________________________________________________ GS: patterns
    @property
    def patterns(self):
        return self._patterns

#___________________________________________________________________________________________________ GS: debug
    @property
    def debug(self):
        """Specifies whether or not the processor is running in debug mode."""
        return self._debug

#___________________________________________________________________________________________________ GS: result
    @property
    def result(self):
        """Processing results"""
        return self._result
    @result.setter
    def result(self, value):
        self._result = value

#___________________________________________________________________________________________________ GS: uid
    @property
    def uid(self):
        """ Identifier for this processor used in the uids of all tags. """
        return self._id

#___________________________________________________________________________________________________ GS: tags
    @property
    def tags(self):
        """ Returns list of top-level tags, which contain references to their children resulting
            in the render tree for the processed markup.

            @@@return list
        """

        return self._tags

#___________________________________________________________________________________________________ GS: cssStyles
    @property
    def cssStyles(self):
        if self._css:
            return u'<style>\n' + u'\n'.join(self._css) + u'\n</style>'
        return None

#___________________________________________________________________________________________________ GS: autoTitle
    @property
    def autoTitle(self):
        if self._autoTitle:
            return self._autoTitle

        return self._anchors[0]['lbl'] if self._anchors else u''
    @autoTitle.setter
    def autoTitle(self, value):
        self._autoTitle = value

#___________________________________________________________________________________________________ GS: autoDescription
    @property
    def autoDescription(self):
        if self._autoDescription:
            return self._autoDescription

        if not self._result:
            return u''

        source = self._result

        p      = re.compile('<script.*(?!</script>)', re.DOTALL)
        source = p.sub(u'', source)

        p      = re.compile('<pre.*(?!</pre>)', re.DOTALL)
        source = p.sub(u'', source)

        p      = re.compile('<[/A-Za-z]+[^>]+>')
        source = p.sub(u'\n', source)

        res = re.compile('[A-Za-z0-9.,?!\'" -:;\(\)&%$#@]{64,}').search(source)
        if not res or not res.group():
            return u''
        r = res.group()

        r = r[:2000].replace(u'\n',u' ')
        r = MarkupProcessor._WHITESPACE_KILLER_REGEX.sub(u' ', r)
        return StringUtils.htmlEscape(StringUtils.getCompleteFragment(r, 255, True))
    @autoDescription.setter
    def autoDescription(self, value):
        self._autoDescription = value

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ traceHierarchy
    def traceHierarchy(self, message, root =None):
        root = self._tags if not root else root
        s    = message + '\n'
        for t in root:
            s += MarkupProcessor._traceTagInHierarchy(t)

        return s

#___________________________________________________________________________________________________ addRenderError
    def addRenderError(self, error):
        self._renderErrors.append(error)

#___________________________________________________________________________________________________ addAnchor
    def addAnchor(self, anchorData):
        self._anchors.append(anchorData)

#___________________________________________________________________________________________________ getAnchorList
    def getAnchorList(self):
        """ Returns the list of anchor tags that were created during the conversion process. These
        are used to reference the anchors elsewhere in the page, e.g. if you want to create a
        navigation sidebar.

        @return list
            The list of anchors, each of which is an object containing the properties for the
            anchor. These include:
            [#ul]
                [#li][#b]id:[/#b] The 'unique' identifier for that anchor in the page.[/#li]
                [#li][#b]lbl:[/#b] The display label for that anchor.[/#li]
            [/#ul]
        """

        self.get()

        return self._anchors

#___________________________________________________________________________________________________ get
    def get(self, **kwargs):
        """ Converts the markup to HTML if not already done and then returns the converted HTML.

            @return string
                The HTML created by converting the markup.
        """

        if self._result:
            return self._result
        elif not self._raw:
            return u''

        self._parseArgs(**kwargs)

        try:
            self.trace('Beginning analysis...')
            self.analyze()
            return self._result
        except Exception, err:
            self._log.writeError('Markup Conversion Failure', err)
            MarkupGlobalError(processor=self).log()
            return self._result if self._result else u''

#___________________________________________________________________________________________________ getNextTagIndex
    def getNextTagIndex(self):
        self._tagIndex += 1
        return self._tagIndex

#___________________________________________________________________________________________________ addJSScript
    def addJSScript(self, script):
        self._js.append(script)

#___________________________________________________________________________________________________ addCSSStyles
    def addCSSStyles(self, styles):
        self._css.append(styles)

#___________________________________________________________________________________________________ trace
    def trace(self, message, data =None, error =None, showResult =False):
        if not self._debug:
            return

        if data or showResult:
            s = [message]
            if data and isinstance(data, dict):
                for n,v in data.iteritems():
                    s.append(n + u': ' + unicode(v))
            elif data:
                s.append(u'DATA: ' + unicode(data))

            if showResult:
                s.append(u'RESULT:\n' + unicode(self._result))
        else:
            s = message

        print u'\n' + 100*u'-'
        if error:
            self._log.writeError(s, error)
        else:
            self._log.write(s)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _traceTagInHierarchy
    @classmethod
    def _traceTagInHierarchy(cls, tag, level =0):
        s = u'\n' + (u'-'*2*level) + (u'> ' if level > 0 else u'') + str(tag)
        if tag.isBlockTag:
            for c in tag.children:
                s += cls._traceTagInHierarchy(c, level + 1)

        return s

#___________________________________________________________________________________________________ _addError
    def _addError(self, message):
        self.trace(u'RENDERING ERROR: ' + message)
        TextAnalyzer._addError(self, message)

#___________________________________________________________________________________________________ _parseArgs
    def _parseArgs(self, **kwargs):
        self.pageProcessor  = ArgsUtils.get('pageProcessor', self.pageProcessor, kwargs)
        self.pageData       = ArgsUtils.get('pageData', self.pageData, kwargs)
        self._debug         = ArgsUtils.get('debug', self._debug, kwargs)
        self._allowModelCaching = True

#___________________________________________________________________________________________________ _insertImpl
    def _insertImpl(self, start, end, value):
        self._result = self._result[:start] + value + self._result[end:]

#___________________________________________________________________________________________________ _executeTagAction
    def _executeTagActions(self, tags, action, errorLabel):
        for t in tags:
            try:
                getattr(t, action)()
            except Exception, err:
                self._log.writeError([errorLabel, 'Tag: ' + str(t)], err)
                MarkupTagError(tag=t).log()

#___________________________________________________________________________________________________ _createTags
    def _createTags(self):
        tags  = []
        for g in self._blocks:
            self.trace(
                'Processing block',
                {'Block':g, 'Source':self._result[g.start:min(g.end, g.start + 40)]}
            )

            #---------------------------------------------------------------------------------------
            # Markup Open Case:
            if g.blockType == MarkupTextBlockUtils.MARKUP_OPEN:
                self.trace('Creating tag', g)
                try:
                    t = MarkupTag.createFromBlock(self, g, self.getNextTagIndex())
                except Exception, err:
                    try:
                        tagName = MarkupTag.getTagNameFromBlock(self, g)
                    except Exception, err:
                        tagName = u'UNKNOWN'

                    self._log.writeError([
                        'Failed to create tag',
                        'Block: ' + str(g),
                        'Tag Name: ' + tagName], err)

                    MarkupGlobalError(
                        processor=self,
                        code=MarkupGlobalError.TAG_CREATION_FAILED,
                        block=g,
                        replacements=[[u'#TAG#', tagName]]).log()
                    continue

                if t is None:
                    MarkupGlobalError(
                        processor=self,
                        code=MarkupGlobalError.FICTIONAL_TAG,
                        block=g).log()
                    self._addError('Unrecognized tag: ' + str(g))
                    continue

                self.trace('Tag created', t)

                if len(tags) > 0 and tags[-1].addChild(t):
                    self.trace('Tag parent found', t.parent)
                    continue

                self.trace('No tag parent found')
                tags.append(t)

            #---------------------------------------------------------------------------------------
            # Markup Close Case:
            elif g.blockType == MarkupTextBlockUtils.MARKUP_CLOSE:
                matched = False
                for t in reversed(tags):
                    try:
                        if t.setCloseBlock(g):
                            matched = True

                            # For leaf tags closed, close all open children. Protects against
                            # unclosed tags from bleeding through.
                            if t.closeBlock and not t.renderChildren:
                                for c in t.children:
                                    if c.isBlockTag and not c.closeBlock:
                                        self.trace('Closing leaf child', {'child':c, 'tag':t})
                                        c.closeBlock = g
                            break
                    except Exception, err:
                        continue

                if not matched:
                    MarkupGlobalError(
                        processor=self,
                        code=MarkupGlobalError.UNMATCHED_CLOSE_TAG,
                        block=g
                    ).log()
                    self._addError('Unmatched block: ' + str(g))

        self.trace(self.traceHierarchy('Tag creation complete:', tags))

        for t in tags:
            t.confirmClosed()

        return tags

#___________________________________________________________________________________________________ _removeHTMLTagWhitespace
    def _removeHTMLTagWhitespace(self, source):
        preserveBlocks = DomUtils.getPreserveBlocks(source)

        res = MarkupProcessor._HTML_INSIDE_TAG_PATTERN.finditer(source)
        if res:
            for r in res:
                start   = r.start()
                end     = r.end()
                replace = r.group('tag').replace(u'\n', u' ')
                source  = source[:start] + replace + source[end:]

        res = MarkupProcessor._HTML_PRE_TAG_WHITESPACE_PATTERN.finditer(source)
        if res:
            for r in res:
                start = r.start()
                end   = r.end()

                tag = r.group('tag')
                preSource = source[:start]
                if StringUtils.begins(tag, (u'<span', u'<a')):
                    strippedPreSource = preSource.strip()

                    # Preserve lines between span tags
                    if StringUtils.ends(strippedPreSource, (u'</span>', u'</a>')):
                        continue

                    # Preserve lines between span tags and non-html entities like text
                    if not strippedPreSource.endswith(u'>'):
                        continue

                skip  = False
                for b in preserveBlocks:
                    if b.start <= start <= b.end or b.start <= end <= b.end:
                        skip = True
                        break
                if skip:
                    continue

                length  = len(r.group('whitespace'))
                replace = u' '*length + tag
                source  = preSource + replace + source[end:]

        res = MarkupProcessor._HTML_POST_TAG_WHITESPACE_PATTERN.finditer(source)
        if res:
            for r in res:
                start = r.start()
                end   = r.end()

                tag        = r.group('tag')
                postSource = source[end:]
                if tag in (u'</span>', u'</a>'):
                    strippedPostSource = postSource.strip()

                    # Preserve lines between span tags
                    if StringUtils.begins(strippedPostSource, (u'<span', u'<a')):
                        continue

                    # Preserve lines between span tags and non-html entities like text
                    if not strippedPostSource.startswith(u'<'):
                        continue

                skip  = False
                for b in preserveBlocks:
                    if b.start <= start <= b.end or b.start <= end <= b.end:
                        skip = True
                        break
                if skip:
                    continue

                length  = len(r.group('whitespace'))
                replace = tag + u' '*length
                source  = source[:start] + replace + postSource

        return source

#___________________________________________________________________________________________________ _modifyResult
    def _modifyResult(self, source):
        prepend = u''
        append = u''
        for n,v in self.radioArrays.iteritems():
            if v.isRemote:
                prepend += v.createControl()

        return prepend + source + append

#___________________________________________________________________________________________________ _postAnalyzeImpl
    def _postAnalyzeImpl(self):
        self.trace('Analysis complete. Beginning processing...')

        #-------------------------------------------------------------------------------------------
        # CLEANUP HTML WHITESPACE
        #       For html already in the page, either explicit or created by the preprocessor remove
        #       the newlines between tags to prevent them from being viewed as line breaks during
        #       Markup rendering.
        self._result = self._removeHTMLTagWhitespace(self._raw.replace(u'\r', u' '))
        self.trace('CLEANED -> preliminary HTML whitespace', showResult=True)

        tags = self._createTags()

        #-------------------------------------------------------------------------------------------
        # REMOVE UNWANTED LINE BREAKS
        # Newlines that occur between close and open Markup tags should be removed.
        res = MarkupProcessor._STRIP_WHITESPACE_PATTERN.finditer(self._result)
        if res:
            for r in res:
                start        = r.start()
                end          = r.end()
                length       = end - start
                self._result = self._result[:start] + u' '*length + self._result[end:]

        res = MarkupProcessor._CONTINUE_LINE_PATTERN.finditer(self._result)
        if res:
            for r in res:
                start   = r.start()
                end     = r.end()
                length  = end - start
                replace = u' '*length
                self._result = self._result[:start] + replace + self._result[end:]

        res = MarkupProcessor._UNWANTED_NEWLINE_PATTERN.finditer(self._result)
        if res:
            for r in res:
                start   = r.start()
                end     = r.end()

                # Skip line breaks inside of leaf tags.
                skip     = False
                startTag = None
                endTag   = None
                for t in tags:
                    if not startTag:
                        c = t.findContainingBlock(start)
                        if c and c.isLeafTag:
                            skip = True
                            break
                        startTag = c

                    if not endTag:
                        endTag = t.findContainingBlock(end)

                    if startTag and endTag:
                        break

                if skip:
                    continue

                # Skip tags that are not display:block or voids
                skip = (startTag and not (startTag.isBlockDisplay or startTag.isVoidTag)) or \
                       (endTag and not (endTag.isBlockDisplay or endTag.isVoidTag))
                if skip:
                    continue

                replace = r.group('close') + r.group('space').replace(u'\n', u' ') + r.group('open')
                self._result = self._result[:start] + replace + self._result[end:]

        self.trace('Line breaks cleaned up; Starting Tag rendering...')

        #-------------------------------------------------------------------------------------------
        # RENDER RESULT
        for b in self._blocks:
            if b.blockType == BlockSyntaxEnum.COMMENT:
                start = b.start
                while start - 1 > 0 and self._result[start-1] in [u'\r', u'\n', u'\t']:
                    start -= 1

                end = b.end
                while end < len(self._result) and self._result[end] in [u'\r', u'\n', u'\t']:
                    end += 1

                length = end - start
                if length > 0:
                    self._result = self._result[:start] + u' '*length + self._result[end:]

        #-------------------------------------------------------------------------------------------
        # EXECUTE THE MULTI-STAGE RENDERING PROCESS
        self._executeTagActions(tags, 'redefinitionTraversal', 'Redefinition Traversal Failure')
        self._executeTagActions(tags, 'redefinitionReversal', 'Redefinition Reversal Failure')

        self._executeTagActions(tags, 'connectivityTraversal', 'Connectivity Traversal Failure')
        self._executeTagActions(tags, 'connectivityReversal', 'Connectivity Reversal Failure')

        self.trace(self.traceHierarchy('Global pre-render complete:', tags))
        self._executeTagActions(tags, 'render', 'Render Failure')

        self._executeTagActions(tags, 'cleanupTraversal', 'Cleanup Traversal Failure')
        self._executeTagActions(tags, 'cleanupReversal', 'Cleanup Render Failure')

        self.trace('RENDERED RESULT -> Markup converted to HTML', showResult=True)

        #-------------------------------------------------------------------------------------------
        # POST-PROCESSING HTML WHITESPACE CLEANUP
        self._result = self._removeHTMLTagWhitespace(self._result.replace(u'\r', u' '))
        self.trace('CLEANED -> post HTML whitespace', showResult=True)

        #-------------------------------------------------------------------------------------------
        # STRIP MARKUP
        res    = MarkupProcessor._STRIP_PATTERN.finditer(self._result)
        offset = 0
        for r in res:
            s       = r.start() + offset
            e       = r.end() + offset
            offset += self.insertCharacters(s, e, u'')
        self.trace('STRIPPED -> markup', showResult=True)

        #-------------------------------------------------------------------------------------------
        # HANDLE NEWLINES NOT IN TAGS
        offset         = 0
        tagIndex       = 0
        preserveBlocks = DomUtils.getPreserveBlocks(self._result)
        while True:
            index = self._result.find('\n', offset)

            if index == -1:
                break

            # Ignore line breaks inside preserved tags
            skip = False
            for b in preserveBlocks:
                if b.start <= index <= b.end:
                    offset = b.end + 1
                    skip   = True
                    break
            if skip:
                continue

            while tagIndex < len(tags):
                if index > tags[tagIndex].end():
                    tagIndex += 1
                    continue
                break

            if tagIndex < len(tags) and tags[tagIndex].contains(index):
                offset    = tags[tagIndex].end()
                tagIndex += 1
                continue

            offset = index + self.insertCharacters(index, index+1, u'<br />')
        self.trace('ADDED breaks to newlines not in tags', showResult=True)

        #-------------------------------------------------------------------------------------------
        # REMOVE BR DIV COMBOS
        res    = MarkupProcessor._DIV_LINE_BREAK_PATTERN.finditer(self._result)
        offset = 0
        for r in res:
            s       = r.start() + offset
            e       = r.end() + offset
            offset += self.insertCharacters(s, e, u'')

        self._result = self._result.replace(u'[*', u'[').replace(u'*]', u']')
        self._tags   = tags

        #-------------------------------------------------------------------------------------------
        # FINAL MODIFICATIONS TO THE RENDERED DOM
        self._result = self._modifyResult(self._result)

        #-------------------------------------------------------------------------------------------
        # CLEANUP WHITE SPACE
        self._result = DomUtils.minifyDom(self._result)

        self.trace('Post processing complete.')
