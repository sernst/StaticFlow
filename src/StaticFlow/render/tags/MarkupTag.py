# MarkupTag.py
# (C)2012-2013
# Scott Ernst

import re
import inspect

from pyaid.web.mako.MakoRenderer import MakoRenderer
from pyaid.ArgsUtils import ArgsUtils
from pyaid.debug.Logger import Logger
from pyaid.reflection.Reflection import Reflection

from StaticFlow.StaticFlowEnvironment import StaticFlowEnvironment
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.error.MarkupTagError import MarkupTagError
from StaticFlow.render.error.MarkupAttributeError import MarkupAttributeError
from StaticFlow.render.attributes.AttributeData import AttributeData

#___________________________________________________________________________________________________ MarkupTag
class MarkupTag(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG      = ''

    _TAG_LIST                      = None
    _MARGIN_TOP_STYLE_ATTR_PATTERN = re.compile('margin-top:[^\'";]+')
    _STYLE_ATTR_PATTERN            = re.compile('style=(("[^"]*")|(\'[^\']*\'))')
    _TAG_INSERT_PATTERN            = re.compile('<[^>]+>')

#___________________________________________________________________________________________________ __init__
    def __init__(self, *args, **kwargs):
        """ Creates a new instance of MarkupTag.

            @@@param attributeSource:string
                If specified this will be used as the source attribute data for the tag. For
                parsed tags this will override the attribute data that was supplied in the actual
                tag definition text. However, in the procedural and/or independent cases where no
                attribute definition existed, this will take its place.
        """

        self._processor       = ArgsUtils.get('processor', None, kwargs, args, 0)
        self._block           = ArgsUtils.get('block', None, kwargs, args, 1)
        self._index           = ArgsUtils.get('index', 0, kwargs, args, 2)
        tagName               = ArgsUtils.get('tagName', None, kwargs, args, 3)
        self._procedural      = ArgsUtils.get('procedural', False, kwargs, args, 4)
        attributes            = ArgsUtils.get('attributes', None, kwargs, args, 5)
        self._independent     = ArgsUtils.get('independent', False, kwargs)
        self._attrData        = None
        self._attrsReady      = False
        self._voidTag         = ArgsUtils.get('void', None, kwargs)
        self._leafTag         = ArgsUtils.get('leaf', None, kwargs)
        self._isInsertsTag    = ArgsUtils.get('inserts', None, kwargs)
        self._passthruTag     = ArgsUtils.get('passthru', None, kwargs)
        self._renderOverride  = ArgsUtils.get('renderOverride', None, kwargs)
        self._renderTemplate  = ArgsUtils.get('renderTemplate', None, kwargs)
        self._replacementName = ArgsUtils.get('replacementName', None, kwargs)

        self._classMetadata  = {}
        self._errors         = []
        self._parent         = ArgsUtils.get('parent', None, kwargs)
        self._replacement    = ''
        self._offset         = 0

        self._name           = self.getClassAttr('TAG', '') if tagName is None else tagName.lower()

        if self._independent:
            self._log   = Logger(self)
            self._attrs = AttributeData(
                self,
                ArgsUtils.get('attributeSource', u'', kwargs),
                attributes=attributes)
        else:
            self._log   = self._processor.log
            start       = self._block.start + (0 if self._procedural else len(self.tagName) + 3)
            self._attrs = AttributeData(
                self,
                ArgsUtils.get('attributeSource', u'', kwargs) if self._procedural else
                    self._processor.source[start:self._block.end-1],
                attributes=attributes)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: apiLevel
    @property
    def apiLevel(self):
        return 2

#___________________________________________________________________________________________________ GS: primaryAttribute
    @property
    def primaryAttribute(self):
        return self.getClassAttr('PRIMARY_ATTR', None)

#___________________________________________________________________________________________________ GS: isProcedural
    @property
    def isProcedural(self):
        return self._procedural

#___________________________________________________________________________________________________ GS: block
    @property
    def block(self):
        return self._block
    @block.setter
    def block(self, value):
        self._block = value

#___________________________________________________________________________________________________ GS: index
    @property
    def index(self):
        return self._index

#___________________________________________________________________________________________________ GS: processor
    @property
    def processor(self):
        return self._processor

#___________________________________________________________________________________________________ GS: isBlockDisplay
    @property
    def isBlockDisplay(self):
        return self.getClassAttr('BLOCK_DISPLAY', False)

#___________________________________________________________________________________________________ GS: isBlockTag
    @property
    def isBlockTag(self):
        return False

#___________________________________________________________________________________________________ GS: isVoidTag
    @property
    def isVoidTag(self):
        """ Specifies whether or not the tag is a void tag. Void tags render as an empty string and
            are useful for conditional rendering and hierarchical data management."""

        if self._voidTag is None:
            return self.getClassAttr('VOID_TAG', False)

        return self._voidTag

#___________________________________________________________________________________________________ GS: isLeafTag
    @property
    def isLeafTag(self):

        if self._leafTag is None:
            return self.getClassAttr('LEAF_TAG', False)

        return self._leafTag

#___________________________________________________________________________________________________ GS: isPassthruTag
    @property
    def isPassthruTag(self):

        if self._passthruTag is None:
            return self.getClassAttr('PASSTHRU_TAG', False)

        return self._passthruTag

#___________________________________________________________________________________________________ GS: isInsertsTag
    @property
    def isInsertsTag(self):

        if self._isInsertsTag is None:
            return self.getClassAttr('INSERTS_TAG', True)

        return self._isInsertsTag

#___________________________________________________________________________________________________ GS: tagName
    @property
    def tagName(self):
        return self._name

#___________________________________________________________________________________________________ GS: replacement
    @property
    def replacement(self):
        return self._replacement

#___________________________________________________________________________________________________ GS: attrs
    @property
    def attrs(self):
        return self._attrs

#___________________________________________________________________________________________________ GS: renderOffset
    @property
    def renderOffset(self):
        return self._offset

#___________________________________________________________________________________________________ GS: aheadCapPolicy
    @property
    def aheadCapPolicy(self):
        return self.getAttrFromClass('AHEAD_CAP_POLICY')

#___________________________________________________________________________________________________ GS: backCapPolicy
    @property
    def backCapPolicy(self):
        return self.getAttrFromClass('BACK_CAP_POLICY')

#___________________________________________________________________________________________________ GS: parent
    @property
    def parent(self):
        return self._parent
    @parent.setter
    def parent(self, value):
        self._parent = value

#___________________________________________________________________________________________________ GS: renderTemplate
    @property
    def renderTemplate(self):
        if self._renderTemplate is None:
            self._renderTemplate = self.getClassAttr('TEMPLATE', '')
        return self._renderTemplate
    @renderTemplate.setter
    def renderTemplate(self, value):
        self._renderTemplate = value

#___________________________________________________________________________________________________ GS: log
    @property
    def log(self):
        return self._log

#___________________________________________________________________________________________________ GS: replacementName
    @property
    def replacementName(self):
        return self._replacementName

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        t = TagAttributesEnum

        out = t.THEME + t.ID + t.HTML_CLASS + t.HTML_STYLE + t.HTML_DATA + t.ACCENTED + t.CLEAR + \
              t.GROUP + t.HTML_ATTR
        if cls.getAttrFromClass('PRIMARY_ATTR', None):
            out += t.VALUE
        return out

#___________________________________________________________________________________________________ clone
    def clone(self, tree=True, replacements=None, **kwargs):
        if replacements and self.replacementName:
            if not isinstance(replacements, list):
                replacements = [replacements]

            for r in replacements:
                if r.replacementName == self.replacementName:
                    return r

        return self._cloneImpl(**kwargs)

#___________________________________________________________________________________________________ getNonPassthruRootTag
    def getNonPassthruRootTag(self):
        if self.isPassthruTag:
            return None

        return self

#___________________________________________________________________________________________________ confirmClosed
    def confirmClosed(self):
        return True

#___________________________________________________________________________________________________ useBackground
    def useBackground(self):
        self.attrs.classes.add('v-S-bck', self.attrs.styleGroup)

#___________________________________________________________________________________________________ addError
    def addError(self, value):
        self._errors.append(value)

#___________________________________________________________________________________________________ makeRenderAttributes
    def makeRenderAttributes(self):
        # Don't allow the tags _renderImpl to be called multiple times
        if self._attrsReady:
            return self._attrData

        try:
            self._attrData   = self._renderImpl()
        except Exception, err:
            MarkupTagError(
                tag=self,
                code=MarkupTagError.RENDER_FAILURE
            ).log()
            self._log.writeError([
                'Tag Render failure',
                'TAG' + str(self)
            ], err)
            return None

        self._attrsReady = True
        return self._attrData

#___________________________________________________________________________________________________ redefinitionTraversal
    def redefinitionTraversal(self, **kwargs):
        self._redefinitionTraversalImpl(**kwargs)
        return True

#___________________________________________________________________________________________________ redefinitionReversal
    def redefinitionReversal(self, **kwargs):
        self._redefinitionReversalImpl(**kwargs)
        return True

#___________________________________________________________________________________________________ connectivityTraversal
    def connectivityTraversal(self, **kwargs):
        self._addGroupRenderData()
        self._connectivityTraversalImpl(**kwargs)
        return True

#___________________________________________________________________________________________________ connectivityReversal
    def connectivityReversal(self, **kwargs):
        self._connectivityReversalImpl(**kwargs)
        return True

#___________________________________________________________________________________________________ preRender
    def preRender(self, **kwargs):
        self._preRenderImpl(**kwargs)
        return True

#___________________________________________________________________________________________________ render
    def render(self, **kwargs):
        insert = ArgsUtils.get('insert', True, kwargs)
        self.preRender(**kwargs)

        p = self._processor

        self._replacement = self._renderImplWrapper()
        if insert:
            self._offset = p.insertCharacters(
                self.start(),
                self.end(),
                self._replacement if self.isInsertsTag else u'',
                self.backCapPolicy,
                self.aheadCapPolicy)

        self.postRender(**kwargs)

        return self._replacement

#___________________________________________________________________________________________________ postRender
    def postRender(self, **kwargs):
        self._postRenderImpl(**kwargs)
        return True

#___________________________________________________________________________________________________ cleanupTraversal
    def cleanupTraversal(self, **kwargs):
        self._cleanupTraversalImpl(**kwargs)
        return True

#___________________________________________________________________________________________________ cleanupReversal
    def cleanupReversal(self, **kwargs):
        self._cleanupReversalImpl(**kwargs)
        return True

#___________________________________________________________________________________________________ addChild
    def addChild(self, tag):
        return False

#___________________________________________________________________________________________________ setCloseBlock
    def setCloseBlock(self, block):
        return False

#___________________________________________________________________________________________________ start
    def start(self, offset =0):
        try:
            return self._block.start + offset
        except Exception, err:
            return offset

#___________________________________________________________________________________________________ end
    def end(self, offset =0):
        try:
            return self._block.end + offset
        except Exception, err:
            return offset

#___________________________________________________________________________________________________ findContainingBlock
    def findContainingBlock(self, index):
        if self.contains(index):
            return self

        return None

#___________________________________________________________________________________________________ childrenContains
    def childrenContains(self, index):
        return None

#___________________________________________________________________________________________________ findChildrenByName
    def findChildrenByName(self, tagName, maxCount =0, recursive =False):
        return []

#___________________________________________________________________________________________________ contains
    def contains(self, index):
        return self.start() <= index < self.end()

#___________________________________________________________________________________________________ addResizerClass
    def addResizerClass(self):
        self.attrs.classes.add('v-gvml-resize')

#___________________________________________________________________________________________________ inOpenBlock
    def openBlockContains(self, index):
        if self.block.contains(index):
            return self

        return None

#___________________________________________________________________________________________________ getTagNameFromBlock
    @classmethod
    def getTagNameFromBlock(cls, processor, block):
        name  = ''
        start = block.start + 2
        ws    = [' ', '\n', '\t', ']']
        pp    = processor
        for i in range(0,24):
            if pp.source[start+i] in ws:
                break
            name += pp.source[start+i]

        return name.lower()

#___________________________________________________________________________________________________ createFromBlock
    @classmethod
    def createFromBlock(cls, processor, block, index):
        try:
            name = cls.getTagNameFromBlock(processor, block)
        except Exception, err:
            return None

        if MarkupTag._TAG_LIST is None:
            tags = dict()
            from StaticFlow.render.tags.TagDefinitions import TagDefinitions
            for tagDef in Reflection.getReflectionList(TagDefinitions):
                tags[tagDef.TAG] = tagDef
            MarkupTag._TAG_LIST = tags

        classImport = MarkupTag._TAG_LIST.get(name, None)
        if classImport is None:
            return None

        return classImport(processor, block, index, name)

#___________________________________________________________________________________________________ getClassAttr
    def getClassAttr(self, attr, defaultValue =None):

        # If that attr is already in the class metadata cache return the value
        if attr in self._classMetadata:
            return self._classMetadata[attr]

        out = self.__class__.getAttrFromClass(attr, defaultValue)
        self._classMetadata[attr] = out
        return out

#___________________________________________________________________________________________________ getAttrFromClass
    @classmethod
    def getAttrFromClass(cls, attr, defaultValue =None):

        # Search through class and its parent classes if necessary to find the attr value
        out = defaultValue
        if hasattr(cls, attr):
            out = getattr(cls, attr, defaultValue)
        else:
            bases = inspect.getmro(cls)
            for b in bases:
                if hasattr(b, attr):
                    out = getattr(b, attr, defaultValue)
                    break

                if isinstance(b, MarkupTag):
                    break

        return out

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return unicode(self.__str__())

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s [%s:%s]>' % (
            self.__class__.__name__, self.start(), self.end()
        )

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _redefinitionTraversalImpl
    def _redefinitionTraversalImpl(self, **kwargs):
        pass

#___________________________________________________________________________________________________ _redefinitionReversalImpl
    def _redefinitionReversalImpl(self, **kwargs):
        pass

#___________________________________________________________________________________________________ _connectivityTraversalImpl
    def _connectivityTraversalImpl(self, **kwargs):
        pass

#___________________________________________________________________________________________________ _connectivityReversalImpl
    def _connectivityReversalImpl(self, **kwargs):
        pass

#___________________________________________________________________________________________________ _preRenderImpl
    def _preRenderImpl(self, **kwargs):
        pass

#___________________________________________________________________________________________________ _postRenderImpl
    def _postRenderImpl(self, **kwargs):
        pass

#___________________________________________________________________________________________________ _cleanupTraversalImpl
    def _cleanupTraversalImpl(self, **kwargs):
        pass

#___________________________________________________________________________________________________ _cleanupReversalImpl
    def _cleanupReversalImpl(self, **kwargs):
        pass

#___________________________________________________________________________________________________ _renderFromTemplate
    def _renderFromTemplate(self, data):
        if self.isVoidTag:
            return u''

        if self._renderOverride is not None:
            return unicode(self._renderOverride)

        if not self.renderTemplate:
            return u''

        try:
            r = MakoRenderer(
                template=self.renderTemplate,
                rootPath=StaticFlowEnvironment.rootTemplatePath,
                data=data,
                logger=self._log
            )
            r.render(
                tag=self,
                data=self.attrs,
                pageData=self.processor.pageData,
                pageProcessor=self.processor.pageProcessor)
        except Exception, err:
            name = self.__class__.__name__
            self.log.writeError([
                u'MAKO RENDERING FAILURE [%s]:' % name,
                u'TEMPLATE: ' + unicode(self.renderTemplate),
                u'TAG: ' + unicode(self),
                u'BLOCK: ' + unicode(self.block),
                u'DATA: ' + unicode(self.attrs)
            ], err)
            return u''

        if not r.success:
            name = self.__class__.__name__
            self.log.write([
                u'MAKO RENDERING FAILURE [%s]:\n%s' % (name, r.errorMessage),
                u'TEMPLATE: ' + unicode(self.renderTemplate),
                u'TAG: ' + unicode(self),
                u'BLOCK: ' + unicode(self.block),
                u'DATA: ' + unicode(self.attrs)
            ])

        return r.dom

#___________________________________________________________________________________________________ _renderImplWrapper
    def _renderImplWrapper(self):
        self.makeRenderAttributes()
        if not self._independent and self._index == 0 and len(self._processor.result[:self.start()].strip()) == 0:
            self.attrs.styles.add('margin-top', '0')
        return self._renderFromTemplate(self._attrData)

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        return u''

#___________________________________________________________________________________________________ _addColorToGroup
    def _addColorToGroup(self, group =None, background =False, extract =False, defaultValue =None,
        forceAsStyle =False
    ):

        # if not forceAsStyle:
        #     colorClass = self.attrs.getAsColorClass(
        #         TagAttributesEnum.COLOR,
        #         background=background,
        #         defaultValue=None,
        #         allowFailure=True
        #     )
        #
        #     if colorClass:
        #         self.attrs.classes.add(colorClass, group)
        #         return True

        color = self.attrs.getAsColorValue(
            TagAttributesEnum.COLOR,
            defaultValue,
            extract=extract
        )

        if not color:
            return False

        prop = 'background-color' if background else 'color'
        self.attrs.styles.add(prop, color.web, group)

        return True

#___________________________________________________________________________________________________ _addGroupRenderData
    def _addGroupRenderData(self):
        from StaticFlow.render.tags.definitions.GroupTag import GroupTag
        if self.tagName == GroupTag.TAG:
            return

        groups, groupsKey = self.attrs.get(
            TagAttributesEnum.GROUP,
            None,
            returnKey=True
        )

        if groups is None:
            return

        if not isinstance(groups, list):
            groups = [groups]

        for g in groups:
            rd = self._processor.groups.get(g, None)
            if rd is None:
                MarkupAttributeError(
                    code='no-such-group',
                    tag=self,
                    attribute=groupsKey[0],
                    attributeData=groupsKey[1],
                    attributeGroup=TagAttributesEnum.GROUP,
                    rawValue=g
                ).log()
                continue

            self.attrs.addAuxiliaryRenderData(rd)

#___________________________________________________________________________________________________ _cloneImpl
    def _cloneImpl(self, **kwargs):
        block = self._block.clone()
        return self.__class__(
            index=self._processor.getNextTagIndex(),
            processor=self._processor,
            block=block,
            tagName=self.tagName,
            procedural=True,
            independent=ArgsUtils.get('independent', True, kwargs),
            attributes=self.attrs,
            void=self._voidTag,
            leaf=self._leafTag,
            passthru=self._passthruTag,
            renderOverride=self._renderOverride,
            renderTemplate=self._renderTemplate,
            replacementName=self._replacementName,
            **kwargs
        )
