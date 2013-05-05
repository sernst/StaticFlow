# GroupTag.py
# (C)2012-2013
# Scott Ernst

from pyaid.text.InsertCapPolicy import InsertCapPolicy

from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.error.MarkupTagError import MarkupTagError
from StaticFlow.render.tags.MarkupTag import MarkupTag

#___________________________________________________________________________________________________ GroupTag
class GroupTag(MarkupTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG           = 'line'
    PRIMARY_ATTR  = TagAttributesEnum.GROUP[0]
    BLOCK_DISPLAY = True
    VOID_TAG      = True

    BACK_CAP_POLICY = InsertCapPolicy(
        InsertCapPolicy.BACK_TYPE, removeExp=InsertCapPolicy.NEWLINE_BACK
    )

    AHEAD_CAP_POLICY = InsertCapPolicy(
        InsertCapPolicy.AHEAD_TYPE, removeExp=InsertCapPolicy.NEWLINE_AHEAD
    )

#___________________________________________________________________________________________________ __init__
    def __init__(self, *args, **kwargs):
        MarkupTag.__init__(self, *args, **kwargs)

        a = self.attrs

        groupName = a.get(
            TagAttributesEnum.GROUP,
            None
        )

        if groupName is None:
            MarkupTagError(tag=self).log() #TODO
            return

        self._processor.groups[groupName] = a

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: apiLevel
    @property
    def apiLevel(self):
        return 0

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        return None
