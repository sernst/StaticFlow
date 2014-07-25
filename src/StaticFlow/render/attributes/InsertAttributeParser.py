# InsertAttributeParser.py
# (C)2014
# Scott Ernst

from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.error.MarkupAttributeError import MarkupAttributeError
from StaticFlow.render.error.MarkupTagError import MarkupTagError

#___________________________________________________________________________________________________ InsertAttributeParser
class InsertAttributeParser(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________
    @classmethod
    def parseText(cls, attrs):
        TAE = TagAttributesEnum
        out = u''
        source, textKey = attrs.get(TAE.TEXT, returnKey=True)

        if source is not None:
            try:
                if isinstance(source, basestring):
                    subPath = source
                    section = None
                else:
                    subPath = source[0]
                    section = source[1]
            except Exception, err:
                attrs.tag.log.writeError(u'Failed to parse text attribute', err)
                MarkupAttributeError(
                    tag=attrs.tag,
                    errorDef=MarkupTagError.ERROR_DEFINITION_NT(
                        u'invalid-text-value',
                        u'Invalid Paragraph Source Text',
                        u'The text attribute value is invalid.'),
                    attribute=textKey[0],
                    attributeData=textKey[1],
                    attributeGroup=TAE.TEXT,
                    rawValue=source).log()
                return
        else:
            subPath = None
            section = None

        subPath, subPathKey = attrs.get(
            TAE.TEXT_PATH + TAE.PATH,
            defaultValue=subPath,
            returnKey=True)

        section, sectionKey = attrs.get(
            TAE.TEXT_SECTION + TAE.SECTION,
            defaultValue=section,
            returnKey=True)

        if source is None and subPath is None and section is None:
            return

        if attrs.processor.page.loadTextInsert(subPath=subPath) is None:
            MarkupAttributeError(
                tag=attrs.tag,
                errorDef=MarkupTagError.ERROR_DEFINITION_NT(
                    u'invalid-text-path',
                    u'Invalid Paragraph Text Path',
                    u'The text path attribute value is invalid.'),
                attribute=textKey[0] if source else subPathKey[0],
                attributeData=textKey[1] if source else subPathKey[1],
                attributeGroup=TAE.TEXT if source else (TAE.TEXT_PATH + TAE.PATH),
                rawValue=source).log()

        try:
            out = attrs.processor.page.getTextInsert(
                subPath=subPath,
                section=section,
                throwMissingError=True)
        except Exception, err:
            attrs.log.writeError(u'Failed to parse paragraph text attribute', err)
            MarkupAttributeError(
                tag=attrs.tag,
                errorDef=MarkupTagError.ERROR_DEFINITION_NT(
                    u'invalid-text-section',
                    u'Invalid Paragraph Text Section',
                    u'The text section attribute value is invalid.'),
                attribute=textKey[0] if source else sectionKey[0],
                attributeData=textKey[1] if source else sectionKey[1],
                attributeGroup=TAE.TEXT if source else (TAE.TEXT_SECTION + TAE.SECTION),
                rawValue=source).log()
            return

        return out

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _internalMethod
    def _internalMethod(self):
        """Doc..."""
        pass
