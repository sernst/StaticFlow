# VimeoTag.py
# (C)2012-2013
# Eric D. Wills and Scott Ernst

import re

from StaticFlow.render.enum.AspectRatioEnum import AspectRatioEnum
from StaticFlow.render.dom.OEmbedRequest import OEmbedRequest
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.error.MarkupTagError import MarkupTagError
from StaticFlow.render.tags.MarkupTag import MarkupTag

#___________________________________________________________________________________________________ VimeoTag
class VimeoTag(MarkupTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'vimeo'
    TEMPLATE       = 'markup/external/vimeo.mako'
    BLOCK_DISPLAY  = True
    PRIMARY_ATTR   = TagAttributesEnum.URL[0]

    _OEMBED       = {'url':'http://vimeo.com/api/oembed.json'}
    _URL_RE       = re.compile('src="http://player\.vimeo\.com/video/(?P<code>[^"?]+)')
    _DEFAULT_CODE = u'47337258'

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        t = TagAttributesEnum
        return MarkupTag.getAttributeList() + t.URL + t.AUTO_PLAY + t.COLOR + t.ASPECT_RATIO

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        """ All VML tags must override the _renderImpl() method, which handles all of the attribute
            parsing and state modification before the actual rendering of the Mako template. This
            method does not return anything, it is meant to modify the tag state.
        """

        a     = self.attrs
        url   = a.get(TagAttributesEnum.URL, None, kwargs)
        play  = a.getAsBool(TagAttributesEnum.AUTO_PLAY, False, kwargs)
        color = a.getAsColorMixer(TagAttributesEnum.COLOR, None)
        if not color:
            if a.focalColors.baseColor.lightness > a.backColors.baseColor.lightness:
                color = a.focalColors.baseColor.bareHex
            else:
                color = a.backColors.baseColor.bareHex
        else:
            color = color.bareHex

        aspect = a.getAsEnumerated(TagAttributesEnum.ASPECT_RATIO, AspectRatioEnum, None,
                                   kwargs, allowFailure=True)
        if not aspect:
            aspect = a.getAsFloat(TagAttributesEnum.ASPECT_RATIO, None)

        if url:
            try:
                result = OEmbedRequest.get(url, self._OEMBED)
                if self._processor.debug:
                    self._log.write(u'Vimeo oEmbed result: ' + unicode(result))

                if not aspect:
                    width  = result.get('width', None)
                    height = result.get('height', None)
                    if width and height:
                        try:
                            aspect = float(width)/float(height + 20.0)
                        except ValueError:
                            pass

                res = VimeoTag._URL_RE.search(result.get('html', ''))

                a.render['code'] = res.group('code')
            except Exception, err:
                if self._processor.debug:
                    self._log.writeError(u'Vimeo oEmbed error', err)

                a.render['code'] = u''
        else:
            a.render['code'] = VimeoTag._DEFAULT_CODE

            if self._processor.privateView:
                MarkupTagError(tag=self, code='missing-url-attribute').log()

        a.render['autoplay'] = u'1' if play else u'0'
        a.render['color']    = unicode(color)

        a.addTagClasses('player', 'player')

        if not aspect:
            aspect = AspectRatioEnum.WIDESCREEN[0]

        a.settings.add('aspect', aspect if aspect else AspectRatioEnum.WIDESCREEN[0], 'player')

        a.classes.add('v-vmlAspect', 'player')

        a.styles.add('width','100%', 'player')
