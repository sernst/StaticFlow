# TwitterTag.py
# (C)2012
# Scott Ernst

import string

from StaticFlow.render.enum.GeneralSizeEnum import GeneralSizeEnum
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.MarkupTag import MarkupTag
from pyaid.json.JSON import JSON
from pyaid.string.StringUtils import StringUtils

#___________________________________________________________________________________________________ TwitterTag
class TwitterTag(MarkupTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'twitter'
    TEMPLATE       = 'markup/external/twitter.mako'
    BLOCK_DISPLAY  = True
    PRIMARY_ATTR   = TagAttributesEnum.SEARCH[0]

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        t = TagAttributesEnum
        return MarkupTag.getAttributeList() + t.SEARCH + t.HEIGHT + t.COUNT + t.START + t.STOP + \
               t.IGNORE + t.TITLE + t.SUBTITLE + t.COUNT + t.SCROLL + t.TIME + t.LOOP

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        if self._processor.globalVars:
            self._processor.globalVars.includeTwitterWidgetAPI = True

        a         = self.attrs
        q         = a.get(TagAttributesEnum.SEARCH, '@vizme', kwargs)
        start     = a.get(TagAttributesEnum.START, None, kwargs)
        stop      = a.get(TagAttributesEnum.STOP, None, kwargs)
        skips     = a.get(TagAttributesEnum.IGNORE, None, kwargs)
        height    = a.getAsEnumerated(TagAttributesEnum.HEIGHT, GeneralSizeEnum, GeneralSizeEnum.medium)
        title     = a.get(TagAttributesEnum.TITLE, '', kwargs)
        subtitle  = a.get(TagAttributesEnum.SUBTITLE, '', kwargs)
        count     = a.get(TagAttributesEnum.COUNT + TagAttributesEnum.TWEETS, 10, kwargs)
        scrollbar = a.getAsBool(TagAttributesEnum.SCROLL, count > 5, kwargs)
        interval  = a.getAsInt(TagAttributesEnum.TIME, 5, kwargs)
        loop      = a.getAsBool(TagAttributesEnum.LOOP, interval > 0, kwargs)

        if not isinstance(q, list):
            q = [q]
        user = len(q) == 1 and q[0].startswith('@') and not StringUtils.contains(q[0], [' ', ','])
        q = u' OR '.join(q)

        if height in ['none', 'm']:
            height = 300
        elif height == 'xxs':
            height = 100
        elif height == 'xs':
            height = 175
        elif height == 's':
            height = 250
        elif height == 'l':
            height = 375
        elif height == 'xl':
            height = 450
        elif height == 'xxl':
            height = 525
        else:
            height = 300

        if skips:
            user = False
            q += u' ' + (u'-' + skips if isinstance(skips, basestring) else u' -'.join(skips))

        if start or stop:
            user = False
            if start:
                q += u' since:' + start

            if stop:
                q += u' until:' + stop


        data = {
            'id':a.id.get(),
            'version':2,
            'width':'auto',
            'height':height,
            'interval':1000*interval,
            'theme': {
                'shell': {
                    'background': a.backColors.baseColor.web,
                    'color': a.focalColors.highlightColor.web
                },

                'tweets': {
                    'background': a.backColors.baseColor.web,
                    'color': a.focalColors.baseColor.web,
                    'links': a.focalColors.linkColor.web
                }
            },
            'features': {
                'scrollbar':scrollbar,
                'loop':loop,
                'live':interval > 0,
                'behavior':  u'all' if user else u'default'
            },

            'type': 'profile' if user else 'search'
        }

        if user:
            a.render['setUser'] = u'.setUser("' + q + u'")'
            data['rpp']         = count
        else:
            a.render['setUser'] = u''
            data['search']      = q
            data['title']       = subtitle.capitalize() if subtitle else string.capwords(q)
            data['subject']     = title.capitalize() if title else string.capwords(q.split(' ')[0])

        a.render['twitterData'] = JSON.asString(data).replace("'", "\\'")

#___________________________________________________________________________________________________ _renderImpl
    def _getAsBooleanString(self, test):
        return u'true' if test else u'false'
