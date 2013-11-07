# MetaDataTag.py
# (C)2013
# Scott Ernst

from pyaid.text.InsertCapPolicy import InsertCapPolicy

from StaticFlow.render.tags.MarkupTag import MarkupTag

#___________________________________________________________________________________________________ MetaDataTag
class MetaDataTag(MarkupTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG           = 'metadata'
    BLOCK_DISPLAY = True
    VOID_TAG      = True

    BACK_CAP_POLICY = InsertCapPolicy(
        InsertCapPolicy.BACK_TYPE, removeExp=InsertCapPolicy.NEWLINE_BACK)

    AHEAD_CAP_POLICY = InsertCapPolicy(
        InsertCapPolicy.AHEAD_TYPE, removeExp=InsertCapPolicy.NEWLINE_AHEAD)

#___________________________________________________________________________________________________ __init__
    def __init__(self, *args, **kwargs):
        MarkupTag.__init__(self, *args, **kwargs)
        self._processor.metadata = dict(
            self._processor.metadata.items() + self.attrs.attributeDict.items())

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        return None
