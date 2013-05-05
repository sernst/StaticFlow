# LinkTag.py
# (C)2012-2013
# Scott Ernst

import re

from StaticFlow.render.attributes.LayoutAttributeParser import LayoutAttributeParser
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.MarkupBlockTag import MarkupBlockTag

#___________________________________________________________________________________________________ LinkTag
class LinkTag(MarkupBlockTag):
    """VizmeML tag class for creating hyperlinks in web pages."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'link'
    TEMPLATE       = 'shared/vml/anchorBase.mako'
    STRIP_POLICY   = MarkupBlockTag.STRIP_ALL
    NEWLINE_POLICY = MarkupBlockTag.REMOVE_NEWLINES
    PRIMARY_ATTR   = TagAttributesEnum.TO[0]

    _ILLEGAL_CHAR_RE = re.compile('[^A-Za-z0-9_]+')

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
        t = TagAttributesEnum
        return MarkupBlockTag.getAttributeList() + t.TO + t.WINDOW_TARGET + t.COLOR + t.URL + \
               t.AJAX + t.SCALE

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a = self.attrs

        LayoutAttributeParser.parseScale(a, True)

        url = a.getAsURL(
            TagAttributesEnum.TO + TagAttributesEnum.URL,
            None
        )

        target = a.getAsKeyword(
            TagAttributesEnum.WINDOW_TARGET,
            None
        )

        self._addColorToGroup(a.styleGroup)

        if target == 'new':
            target = '_blank'
        elif target in ['me', 'self', 'this']:
            target = '_self'
        else:
            target = a.get(TagAttributesEnum.WINDOW_TARGET)

        if url is None:
            ajax = a.get(
                TagAttributesEnum.AJAX + TagAttributesEnum.API,
                None
            )
            if ajax:
                url = 'javascript:void(0)'
                a.settings.add('link', ajax)
            else:
                return
        else:
            ajax = None

        a.attrs.add('href', url)
        a.classes.add(['v-S-lnk-h', 'v-hoverLink'], a.styleGroup)

        if ajax and target:
            # This should link to the target location where the AJAX result should be returned.
            a.settings.add('linkTarget', target)
        elif target:
            a.attrs.add('target', target, a.styleGroup)

        if not a.content:
            a.content = unicode(ajax if ajax else url)
