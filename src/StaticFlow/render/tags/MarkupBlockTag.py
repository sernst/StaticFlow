# MarkupBlockTag.py
# (C)2012-2013
# Scott Ernst

import re

from pyaid.ArgsUtils import ArgsUtils
from pyaid.list.ListUtils import ListUtils
from pyaid.text.InsertCapPolicy import InsertCapPolicy

from StaticFlow.render.error.MarkupTagError import MarkupTagError
from StaticFlow.render.tags.MarkupTag import MarkupTag

#___________________________________________________________________________________________________ MarkupBlockTag
class MarkupBlockTag(MarkupTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG = ''

    REMOVE_NEWLINES   = 'remove'
    BREAK_ON_NEWLINES = 'break'

    STRIP_ALL         = 'all'
    STRIP_NEWLINES    = 'newlines'

    _STRIP_ALL_PATTERN      = re.compile('(^[\s\t\n]+)|([\s\t\n]+$)')
    _STRIP_NEWLINES_PATTERN = re.compile('(^[\n]+)|([\n]+$)')

    _AHEAD_CAP = InsertCapPolicy(
        InsertCapPolicy.AHEAD_TYPE,
        removeExp=InsertCapPolicy.NEWLINE_NO_TAG_AHEAD
    )

#___________________________________________________________________________________________________ __init__
    def __init__(self, *args, **kwargs):
        """Creates a new instance of ClassTemplate."""
        self._closeBlock = ArgsUtils.get('closeBlock', None, kwargs)
        self._children   = []
        MarkupTag.__init__(self, *args, **kwargs)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: isBlockTag
    @property
    def isBlockTag(self):
        return True

#___________________________________________________________________________________________________ GS: closeBlock
    @property
    def closeBlock(self):
        return self._closeBlock

#___________________________________________________________________________________________________ GS: renderChildren
    @property
    def renderChildren(self):
        return not self.isLeafTag and not self.isVoidTag

#___________________________________________________________________________________________________ GS: aheadCapPolicy
    @property
    def aheadCapPolicy(self):
        return MarkupBlockTag._AHEAD_CAP if self.isBlockDisplay else None

#___________________________________________________________________________________________________ GS: closeBlock
    @property
    def closeBlock(self):
        return self._closeBlock
    @closeBlock.setter
    def closeBlock(self, value):
        self._closeBlock = value

#___________________________________________________________________________________________________ GS: replacement
    @property
    def replacement(self):
        return '' if self._closeBlock is None else self._replacement

#___________________________________________________________________________________________________ GS: endTagString
    @property
    def endTagString(self):
        return '' if self._procedural else '[/#' + self._name + ']'

#___________________________________________________________________________________________________ GS: children
    @property
    def children(self):
        return self._children

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        return MarkupTag.getAttributeList()

#___________________________________________________________________________________________________ clone
    def clone(self, tree=True, replacements=None, **kwargs):
        ct = MarkupTag.clone(self, tree, replacements)
        if replacements:
            if isinstance(replacements, list):
                cloned = ct not in replacements
            else:
                cloned = ct != replacements
        else:
            cloned = True

        if cloned:
            if self._closeBlock:
                block = self._closeBlock.clone()
                self._processor.insertBlock(block, afterBlock=self._closeBlock)
            else:
                block = None
            ct.closeBlock = block

        if not tree:
            return ct

        for c in self._children:
            ctChild = c.clone(tree=tree, replacements=replacements, **kwargs)
            ct.addChild(ctChild)

        return ct

#___________________________________________________________________________________________________ getNonPassthruRootTag
    def getNonPassthruRootTag(self):
        if not self.renderChildren:
            return MarkupTag.getNonPassthruRootTag(self)

        if self.isPassthruTag:
            for c in self._children:
                t = c.getNonPassthruRootTag()
                if t:
                    return t
        else:
            return self

        return None

#___________________________________________________________________________________________________ openBlockContains
    def openBlockContains(self, index):
        if not self.isLeafTag:
            for c in self._children:
                out = c.inOpenBlock(index)
                if out:
                    return out

        MarkupTag.openBlockContains(self, index)

#___________________________________________________________________________________________________ confirmClosed
    def confirmClosed(self):
        childEnd = -1
        for c in self._children:
            if c.confirmClosed():
                childEnd = max(childEnd, c.end())

        if self.closeBlock is None:
            MarkupTagError(tag=self, code=MarkupTagError.UNCLOSED_TAG).log()
            return False

        if self.end() < childEnd:
            MarkupTagError(tag=self, code=MarkupTagError.PREMATURE_CLOSE, errorAtEnd=True).log()

        return True

#___________________________________________________________________________________________________ redefinitionTraversal
    def redefinitionTraversal(self, **kwargs):
        self._redefinitionTraversalImpl(**kwargs)

        if not self.renderChildren:
            return True

        for c in self._children:
            c.redefinitionTraversal(**kwargs)

        return True

#___________________________________________________________________________________________________ redefinitionReversal
    def redefinitionReversal(self, **kwargs):
        if self.renderChildren:
            for c in self._children:
                c.redefinitionReversal(**kwargs)

        self._redefinitionReversalImpl(**kwargs)
        return True

#___________________________________________________________________________________________________ connectivityTraversal
    def connectivityTraversal(self, **kwargs):
        self._addGroupRenderData()
        self._connectivityTraversalImpl(**kwargs)

        if not self.renderChildren:
            return True

        for c in self._children:
            c.connectivityTraversal(**kwargs)

        return True

#___________________________________________________________________________________________________ connectivityReversal
    def connectivityReversal(self, **kwargs):
        if self.renderChildren:
            for c in self._children:
                c.connectivityReversal(**kwargs)

        self._connectivityReversalImpl(**kwargs)
        return True

#___________________________________________________________________________________________________ render
    def render(self, **kwargs):
        insert = ArgsUtils.get('insert', True, kwargs)
        self.preRender(**kwargs)

        if self.renderChildren:
            for c in self._children:
                try:
                    c.render(**kwargs)
                except Exception, err:
                    MarkupTagError(tag=c).log()
                    self._log.writeError([
                        'Tag Render Failure',
                        'Tag: ' + str(c)
                    ], err)

        if self._closeBlock:
            self._replacement = self._renderImplWrapper()
        else:
            self._replacement = self._unclosedRenderImpl()

        p = self._processor

        if insert:
            self._offset = p.insertCharacters(
                self.start(),
                self.end(),
                self._replacement,
                self.backCapPolicy,
                self.aheadCapPolicy
            )

        self.postRender(**kwargs)

        return self._replacement

#___________________________________________________________________________________________________ cleanupTraversal
    def cleanupTraversal(self, **kwargs):
        self._cleanupTraversalImpl(**kwargs)

        if not self.renderChildren:
            return True

        for c in self._children:
            c.cleanupTraversal(**kwargs)

        return True

#___________________________________________________________________________________________________ cleanupReversal
    def cleanupReversal(self, **kwargs):
        if self.renderChildren:
            for c in self._children:
                c.cleanupReversal(**kwargs)

        self._cleanupReversalImpl(**kwargs)
        return True

#___________________________________________________________________________________________________ end
    def end(self, offset =0):
        end = self._block.end if self._closeBlock is None else self._closeBlock.end
        return end + offset

#___________________________________________________________________________________________________ bodyStart
    def bodyStart(self, offset =0):
        return self._block.end + offset

#___________________________________________________________________________________________________ bodyEnd
    def bodyEnd(self, offset =0):
        return self.end() + offset - (0 if self._procedural else len(self.endTagString))

#___________________________________________________________________________________________________ findContainingBlock
    def findContainingBlock(self, index):
        c = None if self.isLeafTag else self.childrenContains(index)
        if c is None:
            if self.contains(index):
                return self
        else:
            return c

        return None

#___________________________________________________________________________________________________ childrenContains
    def childrenContains(self, index):
        if self.isLeafTag:
            return None

        for c in self._children:
            cc = c.childrenContains(index)
            if cc:
                return cc
            elif c.contains(index):
                return c

        return None

#___________________________________________________________________________________________________ findChildrenByName
    def findChildrenByName(self, tagName, maxCount =0, recursive =False):
        if not self.children:
            return []

        select = []
        for c in self.children:
            if c.getAttrFromClass('TAG').lower() == tagName.lower():
                select.append(c)

            if recursive:
                select += c.findChildrenByName(tagName, recursive=recursive)

            if maxCount and len(select) >= maxCount:
                return select[:maxCount]

        return select

#___________________________________________________________________________________________________ addChild
    def addChild(self, tag):
        for c in self._children:
            if c.addChild(tag):
                return True

        if tag.start >= self.start() and (self._closeBlock is None or tag.end() <= self.end()):
            self._children.append(tag)
            tag.parent = self
            return True

        return False

#___________________________________________________________________________________________________ addChildAt
    def addChildAt(self, tag, index =0):
        index = ListUtils.getAbsoluteIndex(index, self._children)
        try:
            currentIndex = self._children.index(tag)
            if currentIndex < index:
                self._children.remove(tag)
                self._children.insert(index, tag)
            elif currentIndex > index:
                self._children.insert(index, tag)
                self._children.remove(tag)
            tag.parent = self
            return True
        except Exception, err:
            pass

        self._children.insert(index, tag)
        tag.parent = self
        return True

#___________________________________________________________________________________________________ addChildBefore
    def addChildBefore(self, tag, child):
        try:
            return self.addChildAt(tag, self._children.index(child))
        except Exception, err:
            pass

        return self.addChildAt(tag, -1)

#___________________________________________________________________________________________________ removeChild
    def removeChild(self, tag):
        try:
            self._children.remove(tag)
            return tag
        except Exception, err:
            return None

#___________________________________________________________________________________________________ setCloseBlock
    def setCloseBlock(self, block):
        if self._procedural:
            self._closeBlock = block
            return True

        for c in reversed(self._children):
            if c.setCloseBlock(block):
                return True

        blockStr = self.endTagString
        start    = block.start
        end      = start + len(blockStr)
        if self._closeBlock is None \
           and self._processor.source[start:end].lower() == blockStr:
            self._closeBlock = block
            return True

        return False

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImplWrapper
    def _renderImplWrapper(self):
        self.attrs.content = self._getBodyImpl()
        return MarkupTag._renderImplWrapper(self)

#___________________________________________________________________________________________________ _unclosedRenderImpl
    def _unclosedRenderImpl(self):
        return ''

#___________________________________________________________________________________________________ _getBodyImpl
    def _getBodyImpl(self):
        return self._getBody()

#___________________________________________________________________________________________________ _getBody
    def _getBody(self, stripPolicy =None, newlinePolicy =None):
        p      = self._processor
        reps   = []
        offset = 0

        if self._independent:
            body = u''
            for c in self._children:
                body += c.replacement
        else:
            body = p.result[self.bodyStart():self.bodyEnd()]

        if stripPolicy is None:
            stripPolicy = self.getClassAttr('STRIP_POLICY', None)

        if newlinePolicy is None:
            newlinePolicy = self.getClassAttr('NEWLINE_POLICY', None)

        #-------------------------------------------------------------------------------------------
        # HANDLE BODY STRIP POLICY
        if stripPolicy:
            if stripPolicy == MarkupBlockTag.STRIP_ALL:
                pattern = MarkupBlockTag._STRIP_ALL_PATTERN
            else:
                pattern = MarkupBlockTag._STRIP_NEWLINES_PATTERN

            res = pattern.finditer(body)
            if res:
                for r in res:
                    s       = r.start() + offset
                    e       = r.end() + offset
                    body    = body[:s] + body[e:]
                    offset -= e - s
                    reps.append((s, e - s))

        if self._independent:
            return body

        #-------------------------------------------------------------------------------------------
        # HANDLE BODY NEWLINES
        if newlinePolicy:
            if newlinePolicy == MarkupBlockTag.BREAK_ON_NEWLINES:
                rep = u'<br />'
            else:
                rep = u' '

            start  = self.bodyStart()
            offset = 0
            index  = 0
            repLen = len(rep)
            while True:
                index = body.find(u'\n', index)
                if index == -1:
                    break

                globalIndex = index + start - offset
                for r in reps:
                    if r[0] <= index - offset:
                        globalIndex += r[1]

                c = self.childrenContains(globalIndex)
                if c is None:
                    body    = body[:index] + rep + body[index+1:]
                    index  += repLen
                    offset += repLen - 1
                else:
                    newIndex = c.end() - start + offset
                    for r in reps:
                        if r[0] <= newIndex:
                            newIndex += r[1]
                    index = max(index + 1, newIndex)

        return body



