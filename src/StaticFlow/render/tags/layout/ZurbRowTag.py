# ZurbRowTag.py
# (C)2012-2013
# Scott Ernst

from StaticFlow.render.enum.GeneralSizeEnum import GeneralSizeEnum
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.box.BoxTag import BoxTag

#___________________________________________________________________________________________________ ZurbRowTag
class ZurbRowTag(BoxTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG          = 'zurbrow'
    TEMPLATE     = 'markup/box/default.mako'

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        t = TagAttributesEnum
        return BoxTag.getAttributeList() + t.TYPE

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a = self.attrs

        a.classes.add('row')
        rowType, rowTypeKey = a.get(TagAttributesEnum.TYPE, returnKey=True)
        if rowType is not None:
            rowType = rowType.lower()
            if rowType in ['f', 'full']:
                a.classes.add('fullWidth')
            elif rowType in ['l', 'large']:
                a.classes.add('largeWidth')

        BoxTag._renderImpl(self, paddingDef=GeneralSizeEnum.none[0], **kwargs)

