# MarkupTextBlockUtils.py
# (C)2013
# Scott Ernst

import re

from pyaid.text.BlockDefinition import BlockDefinition
from pyaid.text.BlockSyntaxEnum import BlockSyntaxEnum
from pyaid.text.MatchLookDefinition import MatchLookDefinition

#___________________________________________________________________________________________________ MarkupTextBlockUtils
class MarkupTextBlockUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    MARKUP_OPEN  = 'markup_open'

    MARKUP_CLOSE = 'markup_close'

    MARKUP_ATTR  = 'markup_attr'

#___________________________________________________________________________________________________ createMarkupCommentDef
    @classmethod
    def createMarkupCommentDef(cls, findState =None):
        return BlockDefinition(
            'MARKUP_COMMENT', '[##]', BlockSyntaxEnum.COMMENT, '[/##]', findState=findState
        )

#___________________________________________________________________________________________________ createMarkupOpenDef
    @classmethod
    def createMarkupOpenDef(cls, findState =None):
        return BlockDefinition(
            'MARKUP_OPEN', '[#', cls.MARKUP_OPEN, ']',
            matchReqs=MatchLookDefinition('[^A-Za-z_\]]+', lookAhead=True),
            terminatorReqs=MatchLookDefinition('\*'),
            findState=findState
        )

#___________________________________________________________________________________________________ createMarkupOpenDef
    @classmethod
    def createMarkupCloseDef(cls, findState =None):
        return BlockDefinition(
            'MARKUP_CLOSE', '[/#', cls.MARKUP_CLOSE, ']',
            matchReqs=MatchLookDefinition('[^A-Za-z_\]]+', lookAhead=True),
            terminatorReqs=MatchLookDefinition('\*'),
            findState=findState
        )

#___________________________________________________________________________________________________ createMarkupOpenDef
    @classmethod
    def createMarkupAttributeDef(cls, findState =None):
        return BlockDefinition(
            'MARKUP_ATTR',
            re.compile('(^|[\s\t\n]+)'),
            cls.MARKUP_ATTR,
            re.compile('($|[\s\t\n]+)'),
            matchReqs=MatchLookDefinition(',', True),
            terminatorReqs=MatchLookDefinition(',', True),
            findState=findState,
            chainBlocks=True,
            closeAtEnd=True
        )
