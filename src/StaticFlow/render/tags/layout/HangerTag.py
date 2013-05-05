# HangerTag.py
# (C)2012
# Scott Ernst

from StaticFlow.render.enum.GeneralSizeEnum import GeneralSizeEnum
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.box.BoxTag import BoxTag

#___________________________________________________________________________________________________ HangerTag
class HangerTag(BoxTag):
    """A VizmeML tag that encloses its contents within a stylized border."""

#===================================================================================================
#                                                                                       C L A S S

    TAG           = 'hanger'
    TEMPLATE      = 'vml/layout/hanger.mako'
    BLOCK_DISPLAY = True
    PRIMARY_ATTR  = TagAttributesEnum.SIDE[0]

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        t = TagAttributesEnum
        return BoxTag.getAttributeList() + t.ROW_REACH + t.SIDE + t.EDGES + t.ON + t.REACH

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        BoxTag._renderImpl(self, **kwargs)
        a = self.attrs

        # If the hanger tag is a row child tag its hanging attributes should be ignored and it
        # should be rendered as a normal box tag.
        if a.settings.getKey('rowReach'):
            a.render['hangerActive'] = False
            return
        else:
            a.render['hangerActive'] = True

        side = a.getAsKeyword(
            TagAttributesEnum.SIDE + TagAttributesEnum.EDGES + TagAttributesEnum.ON,
            'left',
            kwargs
        )

        r = a.getAsEnumerated(
            TagAttributesEnum.REACH,
            GeneralSizeEnum,
            GeneralSizeEnum.xsmall,
            kwargs
        )

        if side in ['left', 'lft', 'l']:
            a.classes.add('v-gvml-hangerLeft')
        else:
            a.classes.add('v-gvml-hangerRight')

        if r == 'xxs':
            r = 0.125
        elif r == 'xs':
            r = 0.25
        elif r == 's':
            r = 0.33
        elif r == 'm':
            r = 0.5
        elif r == 'l':
            r = 0.66
        elif r == 'xl':
            r = 0.75
        elif r == 'xxl':
            r = 1.0
        else:
            r = None

        if r is not None:
            a.settings.add('hangerReach', r)

        # Populate the attributes and settings for the resizer tag that triggers resize handling
        # on the hanger.
        a.addTagClasses('sizer', 'resizer')
        a.vdata.add('target', a.id.get(), 'resizer')

        self.addResizerClass()
