# ZurbBoxTag.py
# (C)2012-2013
# Scott Ernst

from StaticFlow.render.enum.GeneralSizeEnum import GeneralSizeEnum
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.box.BoxTag import BoxTag

#___________________________________________________________________________________________________ ZurbBoxTag
class ZurbBoxTag(BoxTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG          = 'zurbbox'
    TEMPLATE     = 'markup/box/default.mako'
    PRIMARY_ATTR = TagAttributesEnum.SIZE

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        t = TagAttributesEnum
        return BoxTag.getAttributeList() + t.SMALL + t.SIZE + t.CENTER

#___________________________________________________________________________________________________ addZurbColumnClasses
    @classmethod
    def addZurbColumnClasses(cls, attrs, target =None, **kwargs):
        a = attrs
        isCentered = a.getAsBool(
            TagAttributesEnum.CENTER,
            False,
            kwargs)

        isLarge = not a.getAsBool(
            TagAttributesEnum.SMALL,
            False,
            kwargs)

        prefix = 'large' if isLarge else 'small'

        size = a.getAsInt(
            TagAttributesEnum.SIZE,
            12,
            kwargs)

        a.classes.add(prefix + '-' + str(size), target)
        if isCentered:
            a.classes.add(prefix + '-centered', target)
        a.classes.add('columns', target)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a = self.attrs
        self.addZurbColumnClasses(a, **kwargs)
        BoxTag._renderImpl(self, paddingDef=GeneralSizeEnum.none[0], **kwargs)


