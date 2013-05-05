# HeaderTag.py
# (C)2012-2013
# Scott Ernst

from pyaid.text.InsertCapPolicy import InsertCapPolicy
from StaticFlow.render.enum.GeneralSizeEnum import GeneralSizeEnum
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.MarkupBlockTag import MarkupBlockTag

#___________________________________________________________________________________________________ HeaderTag
class HeaderTag(MarkupBlockTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'header'
    TEMPLATE       = 'markup/divBase.mako'
    BLOCK_DISPLAY  = True
    LEAF_TAG       = True
    STRIP_POLICY   = MarkupBlockTag.STRIP_ALL
    NEWLINE_POLICY = MarkupBlockTag.REMOVE_NEWLINES
    PRIMARY_ATTR   = TagAttributesEnum.LEVEL[0]

    _BACK_CAP = InsertCapPolicy(
        InsertCapPolicy.BACK_TYPE, addExp=InsertCapPolicy.NEWLINE_BACK, addReplace=u'<br />'
    )

    _AHEAD_CAP = InsertCapPolicy(
        InsertCapPolicy.AHEAD_TYPE, removeExp=InsertCapPolicy.NEWLINE_AHEAD
    )

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: apiLevel
    @property
    def apiLevel(self):
        return 0

#___________________________________________________________________________________________________ GS: aheadCapPolicy
    @property
    def aheadCapPolicy(self):
        return HeaderTag._AHEAD_CAP

#___________________________________________________________________________________________________ GS: backCapPolicy
    @property
    def backCapPolicy(self):
        return HeaderTag._BACK_CAP

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        t = TagAttributesEnum
        return MarkupBlockTag.getAttributeList() + t.LEVEL + t.COLOR + t.SPACING

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a = self.attrs

        level = a.getAsInt(
            TagAttributesEnum.LEVEL,
            1
        )

        spacer = a.getAsEnumerated(
            TagAttributesEnum.SPACING,
            GeneralSizeEnum,
            None,
            allowFailure=True
        )

        if not self._addColorToGroup(a.styleGroup):
            a.classes.add('v-S-hgh', a.styleGroup)

        if not spacer:
            spacer = a.getAsUnit(TagAttributesEnum.SPACING, defaultUnit='em')

            if spacer:
                spacer = spacer.valueAndUnit
            elif self.parent and self.parent.children.index(self) == 0:
                spacer = None
            elif self in self._processor.tags and not self._processor.tags.index(self):
                spacer = None
            else:
                spacer = '1.0em'

        else:
            if spacer == GeneralSizeEnum.xxsmall[0]:
                spacer = '0.25em'
            elif spacer == GeneralSizeEnum.xsmall[0]:
                spacer = '0.5em'
            elif spacer == GeneralSizeEnum.small[0]:
                spacer = '0.75em'
            elif spacer == GeneralSizeEnum.medium[0]:
                spacer = '1.0em'
            elif spacer == GeneralSizeEnum.large[0]:
                spacer = '1.25em'
            elif spacer == GeneralSizeEnum.xlarge[0]:
                spacer = '1.5em'
            elif spacer == GeneralSizeEnum.xxlarge[0]:
                spacer = '2.0em'
            else:
                spacer = None

        if spacer:
            a.styles.add('margin-top', spacer, a.styleGroup)

        if level == 1:
            size = '2.0em'
        elif level == 2:
            size = '1.8em'
        elif level == 3:
            size = '1.6em'
        elif level == 4:
            size = '1.4em'
        else:
            size = '1.2em'

        a.styles.add('font-size', size, a.styleGroup)
        a.vdata.add('jid', a.id.get(), a.styleGroup)

        self._processor.addAnchor({'id':a.id.get(), 'lbl':a.content, 'lvl':level})


