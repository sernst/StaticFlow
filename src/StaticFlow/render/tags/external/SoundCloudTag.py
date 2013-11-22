# SoundCloudTag.py
# (C)2012
# Eric D. Wills and Scott Ernst

import re

from StaticFlow.render.enum.AspectRatioEnum import AspectRatioEnum
from StaticFlow.render.dom.OEmbedRequest import OEmbedRequest
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.error.MarkupTagError import MarkupTagError
from StaticFlow.render.tags.MarkupTag import MarkupTag

#___________________________________________________________________________________________________ SoundCloudTag
class SoundCloudTag(MarkupTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'soundcloud'
    TEMPLATE       = 'markup/external/soundCloud.mako'
    BLOCK_DISPLAY  = True
    PRIMARY_ATTR   = TagAttributesEnum.URL[0]

    _OEMBED           = {'url':'http://soundcloud.com/oembed'}
    _URL_TRACKS_RE    = re.compile('url=http%3A%2F%2Fapi\.soundcloud\.com' +
                                   '%2Ftracks%2F(?P<code>[^"&]+)')
    _URL_PLAYLISTS_RE = re.compile('url=http%3A%2F%2Fapi\.soundcloud\.com' +
                                   '%2Fplaylists%2F(?P<code>[^"&]+)')
    _DEFAULT_CODE     = u'55954068'

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        t = TagAttributesEnum
        return (MarkupTag.getAttributeList() + t.URL + t.AUTO_PLAY + t.ARTWORK + t.COMMENTS +
                t.COLOR + t.ASPECT_RATIO)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        """ All VML tags must override the _renderImpl() method, which handles all of the attribute
            parsing and state modification before the actual rendering of the Mako template. This
            method does not return anything, it is meant to modify the tag state.
        """

        a        = self.attrs
        url      = a.get(TagAttributesEnum.URL, None, kwargs)
        play     = a.getAsBool(TagAttributesEnum.AUTO_PLAY, False, kwargs)
        artwork  = a.getAsBool(TagAttributesEnum.ARTWORK, True, kwargs)
        comments = a.getAsBool(TagAttributesEnum.COMMENTS, True, kwargs)
        color    = a.getAsColorMixer(TagAttributesEnum.COLOR, None)
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
                    self._log.write(u'SoundCloud oEmbed result: ' + unicode(result))

                if not aspect:
                    width  = result.get('width', None)
                    height = result.get('height', None)
                    if width and height:
                        try:
                            aspect = float(width)/float(height + 20.0)
                        except ValueError:
                            pass

                res  = SoundCloudTag._URL_TRACKS_RE.search(result.get('html', ''))
                type = u'tracks'
                if not res:
                    res  = SoundCloudTag._URL_PLAYLISTS_RE.search(result.get('html', ''))
                    type = u'playlists'

                    a.render['code'] = res.group('code')
                    a.render['type'] = type
            except Exception, err:
                if self._processor.debug:
                    self._log.writeError(u'SoundCloud oEmbed error', err)

                a.render['code'] = u''
                a.render['type'] = u'playlists'
        else:
            a.render['code'] = SoundCloudTag._DEFAULT_CODE
            a.render['type'] = u'tracks'

            if self._processor.privateView:
                MarkupTagError(tag=self, errorDef=MarkupTagError.MISSING_URL).log()

        a.render['autoplay'] = u'true' if play else u'false'
        a.render['artwork']  = u'true' if artwork else u'false'
        a.render['comments'] = u'true' if comments else u'false'
        a.render['color']    = unicode(color)

        a.addTagClasses('player', 'player')

        if not aspect:
            aspect = AspectRatioEnum.WIDESCREEN[0]

        a.settings.add('aspect', aspect if aspect else AspectRatioEnum.WIDESCREEN[0], 'player')

        a.classes.add('v-vmlAspect', 'player')

        a.styles.add('width','100%', 'player')
