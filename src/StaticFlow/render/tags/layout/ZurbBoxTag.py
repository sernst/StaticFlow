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
        return BoxTag.getAttributeList() + t.SMALL + t.SIZE + t.CENTER + t.TYPE + t.PUSH + t.PULL \
            + t.OFFSET

#___________________________________________________________________________________________________ addZurbColumnClasses
    @classmethod
    def addZurbColumnClasses(cls, attrs, target =None, **kwargs):
        a = attrs

        pull = 0
        push = 0
        offset = a.getAsInt(TagAttributesEnum.OFFSET)
        if offset is None:
            push = a.getAsInt(TagAttributesEnum.PUSH, 0)
            pull = a.getAsInt(TagAttributesEnum.PULL, 0)
        elif offset > 0:
            push = offset
        elif offset < 0:
            pull = abs(offset)

        if pull > 0:
            a.classes.add('pull-' + str(pull))
        if push > 0:
            a.classes.add('push-' + str(push))

        isCentered = a.getAsBool(
            TagAttributesEnum.CENTER,
            False,
            kwargs)

        sizeType = a.get(TagAttributesEnum.TYPE, u'L')
        try:
            sizeType = sizeType.upper()[0]
        except Exception, err:
            sizeType = u'L'

        prefix = {'L':'large', 'M':'medium', 'S':'small'}[sizeType]

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


