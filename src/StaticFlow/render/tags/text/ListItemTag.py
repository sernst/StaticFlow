# ListItemTag.py
# (C)2012
# Scott Ernst

from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.error.MarkupTagError import MarkupTagError
from StaticFlow.render.tags.MarkupBlockTag import MarkupBlockTag

#___________________________________________________________________________________________________ ListItemTag
class ListItemTag(MarkupBlockTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'item'
    TEMPLATE       = 'markup/list/listItemBase.mako'
    BLOCK_DISPLAY  = True
    STRIP_POLICY   = MarkupBlockTag.STRIP_ALL
    NEWLINE_POLICY = MarkupBlockTag.BREAK_ON_NEWLINES

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: listParent
    @property
    def listParent(self):
        parent = self.parent
        while parent:
            if parent.tagName == 'list':
                return parent
            parent = parent.parent

        return None

#___________________________________________________________________________________________________ GS: apiLevel
    @property
    def apiLevel(self):
        return 0

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        t = TagAttributesEnum
        return MarkupBlockTag.getAttributeList() + t.COLOR

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _connectivityReversalImpl
    def _connectivityReversalImpl(self):
        p          = self._processor

        listParent = self.listParent
        if not listParent and not isinstance(self.parent, ListItemTag):
            MarkupTagError(
                tag=self,
                errorDef=MarkupTagError.ERROR_DEFINITION_NT(
                    u'orphaned-list-item',
                    u'Orphaned List Item',
                    u'List item tag appears outside of a list.') ).log()

        subLists   = []
        openList   = []
        lastItem   = None
        for t in self._children:
            if t.tagName == self.tagName:
                if lastItem is None:
                    openList.append(t)
                    lastItem = t
                elif len(p.result[lastItem.end():t.start()].strip()) == 0:
                    openList.append(t)
                    lastItem = t
                else:
                    subLists.append(openList)
                    openList = [t]
                    lastItem = t
            elif openList:
                subLists.append(openList)
                openList = []
                lastItem = None

        if openList:
            subLists.append(openList)

        if not subLists:
            return


        from StaticFlow.render.tags.text.ListTag import ListTag
        if isinstance(self.parent, ListTag):
            isOrdered  = self.parent.isOrdered
            attributes = {
                'type':[self.parent.attrs.getAsKeyword(TagAttributesEnum.TYPE, 'bullet'), None] }
        else:
            isOrdered  = False
            attributes = None

        offset = 1
        for group in subLists:
            if isOrdered and offset > 1:
                attributes['start'] = [str(offset), None]

            b = group[0].block
            b = p.createBlock(b.start, b.start, self.block.blockDef)
            l = ListTag(self._processor, b, len(self._processor.tags), procedural=True,
                        attributes=attributes)

            b = group[-1].closeBlock
            b = p.createBlock(b.end, b.end, self.closeBlock.blockDef)
            l.setCloseBlock(b)

            self.addChildBefore(l, group[0])
            for t in group:
                self.removeChild(t)
                l.addChild(t)
            offset += len(group)

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a = self.attrs
        self._addColorToGroup(a.styleGroup)
