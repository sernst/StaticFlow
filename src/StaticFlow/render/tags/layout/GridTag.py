# GridTag.py
# (C)2012
# Scott Ernst

from StaticFlow.render.enum.GeneralSizeEnum import GeneralSizeEnum
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.box.BoxTag import BoxTag

#___________________________________________________________________________________________________ GridTag
class GridTag(BoxTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG          = 'grid'
    TEMPLATE     = 'markup/box/default.mako'

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        t = TagAttributesEnum
        return BoxTag.getAttributeList() + t.VERTICAL_ALIGN + t.SPACING + t.SAME_HEIGHT + \
            t.RAGGED + t.DEFAULT_REACH + t.MAX_COLUMNS + t.SIZE

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _connectivityReversalImpl
    def _connectivityReversalImpl(self):
        for c in self.children:
            if c.isPassthruTag:
                if c.children:
                    c = c.children[0]
                else:
                    continue

            c.attrs.classes.add('v-gvml-gridChild')

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a = self.attrs

        align = a.getAsKeyword(
            TagAttributesEnum.VERTICAL_ALIGN,
            'grow',
            kwargs
        )

        gapSize = a.getAsEnumerated(
            TagAttributesEnum.SPACING,
            GeneralSizeEnum,
            GeneralSizeEnum.medium,
            kwargs
        )

        sameHeight  = a.getAsBool(
            TagAttributesEnum.SAME_HEIGHT,
            True,
            kwargs
        )

        ragged = a.getAsBool(
            TagAttributesEnum.RAGGED,
            False,
            kwargs
        )

        size = a.getAsEnumerated(
            TagAttributesEnum.SIZE + TagAttributesEnum.DEFAULT_REACH,
            GeneralSizeEnum,
            None,
            kwargs
        )

        maxColumns = a.getAsInt(
            TagAttributesEnum.MAX_COLUMNS,
            len(self.children),
            kwargs
        )

        a.settings.add('maxCols', maxColumns)
        a.settings.add('rag', ragged)
        a.settings.add('hAll', sameHeight)

        if not size:
            size = a.getAsUnit(
                TagAttributesEnum.SIZE + TagAttributesEnum.DEFAULT_REACH,
                125,
                'px',
                unitType=int
            )
            a.settings.add('size', size.value)
        else:
            if size == 'xxs':
                size = 50
            elif size == 'xs':
                size = 125
            elif size == 's':
                size = 200
            elif size == 'm':
                size = 250
            elif size == 'l':
                size = 325
            elif size == 'xl':
                size = 425
            elif size == 'xxl':
                size = 500
            else:
                size = 125
            a.settings.add('size', size)

        if gapSize == 'xxs':
            gap = 1
        elif gapSize == 'xs':
            gap = 4
        elif gapSize == 's':
            gap = 8
        elif gapSize == 'm':
            gap = 16
        elif gapSize == 'l':
            gap = 32
        elif gapSize == 'xl':
            gap = 64
        elif gapSize == 'xxl':
            gap = 128
        else:
            gap = 0
        a.settings.add('gap', gap)

        if align in ['grow', 'fill']:
            align = 'fill'
        elif align in ['top']:
            align = 'top'
        elif align in ['middle', 'center']:
            align = 'middle'
        elif align in ['bottom', 'baseline']:
            align = 'bottom'
        else:
            align = None

        if align:
            a.settings.add('rowAlign', align)

        self.addResizerClass()
        BoxTag._renderImpl(self, paddingDef=GeneralSizeEnum.none[0], align='auto', **kwargs)

