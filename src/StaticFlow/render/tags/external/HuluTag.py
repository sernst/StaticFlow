# HuluTag.py
# (C)2012
# Eric D. Wills and Scott Ernst

import re

from StaticFlow.render.enum.AspectRatioEnum import AspectRatioEnum
from StaticFlow.render.dom.OEmbedRequest import OEmbedRequest
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.error.MarkupAttributeError import MarkupAttributeError
from StaticFlow.render.error.MarkupTagError import MarkupTagError
from StaticFlow.render.tags.MarkupTag import MarkupTag

#___________________________________________________________________________________________________ HuluTag
class HuluTag(MarkupTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'hulu'
    TEMPLATE       = 'markup/external/hulu.mako'
    BLOCK_DISPLAY  = True
    PRIMARY_ATTR   = TagAttributesEnum.URL[0]

    _OEMBED       = {'url':'http://www.hulu.com/api/oembed.json'}
    _URL_RE       = re.compile('http://www\.hulu\.com/embed/(?P<code>[^"?]+)')
    _DEFAULT_CODE = u'jFY7Fwz02N3gSJip5OhIxw'

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        t = TagAttributesEnum
        return (MarkupTag.getAttributeList() + t.URL + t.START + t.STOP + t.THUMB + t.ASPECT_RATIO)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        """ All VML tags must override the _renderImpl() method, which handles all of the attribute
            parsing and state modification before the actual rendering of the Mako template. This
            method does not return anything, it is meant to modify the tag state.
        """

        a      = self.attrs
        url    = a.get(TagAttributesEnum.URL, None, kwargs)
        aspect = a.getAsEnumerated(
            TagAttributesEnum.ASPECT_RATIO,
            AspectRatioEnum,
            None,
            kwargs,
            allowFailure=True
        )

        if not aspect:
            aspect = a.getAsFloat(TagAttributesEnum.ASPECT_RATIO, None)

        if url:
            try:
                result = OEmbedRequest.get(url, self._OEMBED)
                if self._processor.debug:
                    self._log.write(u'Hulu oEmbed result: ' + unicode(result))

                if not aspect:
                    width  = result.get('width', None)
                    height = result.get('height', None)
                    if width and height:
                        try:
                            aspect = float(width)/float(height + 20.0)
                        except ValueError:
                            pass

                res = HuluTag._URL_RE.search(result.get('embed_url', ''))

                code = res.group('code')

                start, startKeyData = a.get(TagAttributesEnum.START, None, kwargs, returnKey=True)
                if start:
                    try:
                        start = int(start)
                    except Exception, err:
                        start = 0

                        MarkupAttributeError(tag=self, code='invalid-frame-number',
                                          attribute=startKeyData[0], attributeData=startKeyData[1],
                                          attributeGroup=TagAttributesEnum.START, rawValue=start).log()

                stop, stopKeyData = a.get(TagAttributesEnum.STOP, None, kwargs, returnKey=True)
                if stop:
                    try:
                        stop = int(stop)
                    except Exception, err:
                        stop = 0

                        MarkupAttributeError(tag=self, code='invalid-frame-number',
                                          attribute=stopKeyData[0], attributeData=stopKeyData[1],
                                          attributeGroup=TagAttributesEnum.STOP, rawValue=stop).log()


                thumb, thumbKeyData = a.get(TagAttributesEnum.THUMB, None, kwargs, returnKey=True)
                if thumb:
                    try:
                        thumb = int(thumb)
                    except Exception, err:
                        thumn = 0

                        MarkupAttributeError(tag=self, code='invalid-frame-number',
                                          attribute=thumbKeyData[0], attributeData=thumbKeyData[1],
                                          attributeGroup=TagAttributesEnum.THUMB, rawValue=thumb).log()

                if thumb is not None:
                    if start is None:
                        start = 0
                    if stop is None:
                        stop = thumb
                elif stop is not None:
                    if start is None:
                        start = 0

                if start is not None:
                    code += u'/' + unicode(start)
                if stop is not None:
                    code += u'/' + unicode(stop)
                if thumb is not None:
                    code += u'/' + unicode(thumb)

                a.render['code'] = code

            except Exception, err:
                if self._processor.debug:
                    self._log.writeError(u'Hulu oEmbed error', err)

                a.render['code'] = u''
        else:
            a.render['code'] = HuluTag._DEFAULT_CODE

            if self._processor.privateView:
                MarkupTagError(tag=self, code='missing-url-attribute').log()

        a.addTagClasses('player', 'player')

        if not aspect:
            aspect = AspectRatioEnum.WIDESCREEN[0]

        a.settings.add('aspect', aspect if aspect else AspectRatioEnum.WIDESCREEN[0], 'player')

        a.classes.add('v-vmlAspect', 'player')

        a.styles.add('width','100%', 'player')

        a.render['isSecure'] = self._processor.isSecure
