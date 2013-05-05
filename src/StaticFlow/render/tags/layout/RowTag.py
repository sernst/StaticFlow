# RowTag.py
# (C)2012
# Scott Ernst

import math

from StaticFlow.render.enum.GeneralSizeEnum import GeneralSizeEnum
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.box.BoxTag import BoxTag

#___________________________________________________________________________________________________ RowTag
class RowTag(BoxTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG          = 'row'
    TEMPLATE     = 'markup/box/default.mako'

    _COLUMN_UNIT_WIDTH = 64

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        t = TagAttributesEnum
        return BoxTag.getAttributeList() + t.VERTICAL_ALIGN + t.SPACING + t.SAME_HEIGHT + \
            t.RAGGED + t.DEFAULT_REACH + t.MAX_COLUMNS + t.MIN_COLUMNS + t.SIZE

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _connectivityReversalImpl
    def _connectivityReversalImpl(self):
        a            = self.attrs
        columns      = []
        totalReach   = 0.0

        defaultReach = a.getAsEnumerated(
            TagAttributesEnum.DEFAULT_REACH + TagAttributesEnum.SIZE,
            GeneralSizeEnum,
            None,
            allowFailure=True
        )

        if not defaultReach:
            defaultReach = a.getAsUnit(
                TagAttributesEnum.DEFAULT_REACH,
                None,
                allowFailure=True
            )

            if not defaultReach:
                defaultReach = 'm'

        for c in self.children:
            c = c.getNonPassthruRootTag()
            if c is None or not c.isBlockDisplay:
                continue

            mr = None
            r  = c.attrs.getAsEnumerated(
                TagAttributesEnum.REACH,
                GeneralSizeEnum,
                None,
                allowFailure=True
            )

            if r == 'none':
                r = defaultReach
            elif not r:
                r = c.attrs.getAsUnit(
                    TagAttributesEnum.REACH,
                    None,
                    allowFailure=True
                )

                if not r:
                    r = defaultReach

            if isinstance(r, basestring):
                if r == 'xxs':
                    r  = 0.25
                    mr = 1
                elif r == 'xs':
                    r  = 0.5
                    mr = 2
                elif r == 's':
                    r  = 0.75
                    mr = 3
                elif r == 'm':
                    r  = 1.0
                    mr = 4
                elif r == 'l':
                    r  = 1.5
                    mr = 5
                elif r == 'xl':
                    r  = 2.0
                    mr = 6
                elif r == 'xxl':
                    r  = 3.0
                    mr = 7
            else:
                r  = float(r.value)
                mr = int(round(4*r))

            totalReach += r
            columns.append([c, r, mr if mr else int(4*r)])

        if len(columns) == 2:
            columns[0][0].attrs.classes.add('v-gvml-rowChildLeft')
            columns[1][0].attrs.classes.add('v-gvml-rowChildRight')
        else:
            for c in columns:
                c[0].attrs.classes.add('v-gvml-rowChild')

        for c in columns:
            r = 0.01*math.floor(100*c[1]/totalReach)
            c[0].attrs.settings.add('rowReach', r)
            c[0].attrs.settings.add('rowMinW', RowTag._COLUMN_UNIT_WIDTH*c[2])

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a = self.attrs
        sameHeight = a.getAsBool(
            TagAttributesEnum.SAME_HEIGHT,
            False,
            kwargs
        )

        maxColumns = a.getAsInt(
            TagAttributesEnum.MAX_COLUMNS,
            0,
            kwargs
        )

        minColumns = a.getAsInt(
            TagAttributesEnum.MIN_COLUMNS,
            1,
            kwargs
        )

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
        a.settings.add('maxCols', maxColumns)
        a.settings.add('minCols', min(max(minColumns, 1), maxColumns))
        a.settings.add('hAll', sameHeight)

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
        BoxTag._renderImpl(self, paddingDef=GeneralSizeEnum.none[0], **kwargs)
