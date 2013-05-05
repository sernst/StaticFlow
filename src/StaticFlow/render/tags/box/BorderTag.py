# BorderTag.py
# (C)2012-2013
# Scott Ernst

import re

from pyaid.list.ListUtils import ListUtils

from StaticFlow.render.enum.GeneralSizeEnum import GeneralSizeEnum
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.box.BoxTag import BoxTag

#___________________________________________________________________________________________________ BorderTag
class BorderTag(BoxTag):
    """A VizmeML tag that encloses its contents within a stylized border."""

#===================================================================================================
#                                                                                       C L A S S

    TAG           = 'border'
    BLOCK_DISPLAY = True
    PRIMARY_ATTR  = TagAttributesEnum.EDGES[0]

    _ALLOW_MERGE_OPEN_RE  = re.compile('^[\s\t\n]*\[#')
    _ALLOW_MERGE_CLOSE_RE = re.compile('\[[A-Za-z0-9_]\][\s\t\n]$')

#___________________________________________________________________________________________________ __init__
    def __init__(self, *args, **kwargs):
        BoxTag.__init__(self, *args, **kwargs)
        self._mergedToChild = False

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: mergedToChild
    @property
    def mergedToChild(self):
        return self._mergedToChild

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        t = TagAttributesEnum
        return BoxTag.getAttributeList() + t.MERGE + t.LINE_TYPE + t.EDGES + t.COLOR + \
               t.LINE_WIDTH + t.TYPE

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _connectivityReversalImpl
    def _connectivityReversalImpl(self):
        # If the border tag is wrapping a single block tag then apply the border to the element to
        # save on wrapping the border in an element of its own.
        cs    = self.children
        merge = not self.attrs.explicitAccent and \
                self.attrs.getAsBool(TagAttributesEnum.MERGE, True) and \
                len(cs) == 1 and cs[0].isBlockDisplay

        if merge:
            merge = not self._processor.result[self.bodyStart():cs[0].start()].strip()
            if merge:
                merge = not self._processor.result[cs[0].end():self.bodyEnd()].strip()

        if merge:
            self._populateBorder(cs[0])
            cs[0].attrs.join(self.attrs)
            self.renderTemplate = 'shared/vml/empty.mako'
            self._mergedToChild = True
            BoxTag._renderImpl(self, skipBackground=True, paddingDef=GeneralSizeEnum.none[0])

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        if self._mergedToChild:
            return

        self._populateBorder(self)
        BoxTag._renderImpl(self, paddingDef=GeneralSizeEnum.none[0], **kwargs)

#___________________________________________________________________________________________________ _populateBorder
    def _populateBorder(self, target):
        src = self.attrs
        a = target.attrs

        lineType  = src.getAsKeyword(
            TagAttributesEnum.TYPE + TagAttributesEnum.LINE_TYPE,
            u'solid'
        )

        edgeTypes = src.getAsKeyword(
            TagAttributesEnum.EDGES,
            u'all'
        )

        color = src.getAsColorMixer(
            TagAttributesEnum.COLOR,
            None,
            extract=True
        )

        lineWidth = src.getAsInt(
            TagAttributesEnum.LINE_WIDTH,
            None,
            allowFailure=True
        )

        if lineWidth is None:
            lineWidthEnum = src.getAsEnumerated(
                TagAttributesEnum.LINE_WIDTH,
                GeneralSizeEnum,
                GeneralSizeEnum.xxsmall
            )
            if lineWidthEnum == GeneralSizeEnum.xxsmall[0]:
                lineWidth = 1
            elif lineWidthEnum == GeneralSizeEnum.xsmall[0]:
                lineWidth = 2
            elif lineWidthEnum == GeneralSizeEnum.small[0]:
                lineWidth = 3
            elif lineWidthEnum == GeneralSizeEnum.medium[0]:
                lineWidth = 4
            elif  lineWidthEnum == GeneralSizeEnum.large[0]:
                lineWidth = 5
            elif  lineWidthEnum == GeneralSizeEnum.xlarge[0]:
                lineWidth = 6
            elif lineWidthEnum == GeneralSizeEnum.xxlarge[0]:
                lineWidth = 7
            else:
                lineWidth = 1

        #-------------------------------------------------------------------------------------------
        # COLOR: If no color is present use the border color for the current VizmeML style
        if color is None:
            try:
                color = a.backColors.borderColor
            except Exception, err:
                pass
        color = 'currentColor' if color is None else color.web

        #-------------------------------------------------------------------------------------------
        # FIND EDGES
        edges = [0, 0, 0, 0]
        if isinstance(edgeTypes, basestring) and edgeTypes.find('none') == -1:
            if edgeTypes.find('all') != -1:
                edges = [1, 1, 1, 1]
            else:
                if edgeTypes.find('left') != -1:
                    edges[-1] = 1
                if edgeTypes.find('right') != -1:
                    edges[1] = 1
                if edgeTypes.find('top') != -1:
                    edges[0] = 1
                if edgeTypes.find('bottom') != -1:
                    edges[2] = 1

                if not sum(edges):
                    if edgeTypes.find('l') != -1:
                        edges[-1] = 1
                    if edgeTypes.find('r') != -1:
                        edges[1] = 1
                    if edgeTypes.find('t') != -1:
                        edges[0] = 1
                    if edgeTypes.find('b') != -1:
                        edges[2] = 1

        elif isinstance(edgeTypes, list):
            if 'all' in edgeTypes:
                edges = [1, 1, 1, 1]
            else:
                if ListUtils.contains(edgeTypes, ['l', 'left']):
                    edges[-1] = 1
                if ListUtils.contains(edgeTypes, ['r', 'right']):
                    edges[1] = 1
                if ListUtils.contains(edgeTypes, ['t', 'top']):
                    edges[0] = 1
                if ListUtils.contains(edgeTypes, ['b', 'bottom']):
                    edges[2] = 1

        #-------------------------------------------------------------------------------------------
        # ADD EDGE STYLES
        borderName  = 'border#REP#'
        borderStyle = '%spx %s %s' % (str(lineWidth), lineType, color)
        if sum(edges) == 4:
            a.styles.add(borderName.replace('#REP#', ''), borderStyle, a.styleGroup)
        else:
            if edges[0]:
                a.styles.add(borderName.replace('#REP#', '-top'), borderStyle, a.styleGroup)
            if edges[1]:
                a.styles.add(borderName.replace('#REP#', '-right'), borderStyle, a.styleGroup)
            if edges[2]:
                a.styles.add(borderName.replace('#REP#', '-bottom'), borderStyle, a.styleGroup)
            if edges[3]:
                a.styles.add(borderName.replace('#REP#', '-left'), borderStyle, a.styleGroup)
