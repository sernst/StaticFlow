# YouTubeTag.py
# (C)2012-2013
# Scott Ernst

import re

from StaticFlow.render.enum.AspectRatioEnum import AspectRatioEnum
from StaticFlow.render.dom.OEmbedRequest import OEmbedRequest
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.error.MarkupTagError import MarkupTagError
from StaticFlow.render.tags.MarkupTag import MarkupTag

#___________________________________________________________________________________________________ YouTubeTag
class YouTubeTag(MarkupTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    # The tag identifier, i.e. [#youtube]
    TAG            = 'youtube'

    # The Mako template used to render the tag. This path is relative to the root path
    # /vizme/templates/mako/.
    TEMPLATE       = 'markup/external/youTube.mako'

    # Specifies whether the tag should be rendered like a <div> tag when True or like a <span> tag
    # when False. Use False only for tags that should be inline with text.
    BLOCK_DISPLAY  = True

    # This is the attribute for the tag that can be specified without defining the property. In the
    # YouTubeTag case, this is the 'url' property meaning that:
    #   [#youtube url:http://www.youtube.com/video/5j3hgdo2]
    # can also be specified as:
    #   [#youtube http://www.youtube.com/video/5j3hgdo2]
    # omitting the url: attribute prefix. Not all tags have a primary attribute, in which case this
    # can be set to None or omitted.
    PRIMARY_ATTR   = TagAttributesEnum.URL[0]

    _OEMBED = {'url':'http://www.youtube.com/oembed'}

    # This is the regex used to extract the video code from the oembed result.
    _URL_RE       = re.compile('src="http://www\.youtube\.com/embed/(?P<code>[^"?]+)')
    _DEFAULT_CODE = u'L1s_PybOuY0'

    #===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        t = TagAttributesEnum
        return MarkupTag.getAttributeList() + t.URL + t.AUTO_PLAY + t.START + t.TIME + t.ASPECT_RATIO

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        """ All VML tags must override the _renderImpl() method, which handles all of the attribute
            parsing and state modification before the actual rendering of the Mako template. This
            method does not return anything, it is meant to modify the tag state.
        """

        # As mentioned, the a property is my convention for self.attrs, which is an instance of
        # vmi.web.vml.render.AttributeData.
        a = self.attrs

        # The parsed VML attributes for a tag are accessed through the AttributeData class using the
        # various get*() methods. In this case I use a.get(), which returns the raw string value for
        # given attributes. As you can see the first argument is a list of possible attribute names.
        # To make VizmeML as flexible as possible, we support in many case multiple names for an
        # attribute. A good example of this is the TagAttributeEnum.URL case, which allows url
        # properties to be specified as url:... or href:... or src:..., which are the three possible
        # values used in html. Multiple attribute names also allow for long and short versions of
        # names and the user can decide which to use. Here the START and TIME attribute names are
        # combined, which means the start time can be specified as start:..., begin:..., or time:...
        # The second argument in this method is the default value to return if the property was not
        # specified. Finally, kwargs is passed in as an override. This is optional, but I've started
        # doing it by default because it makes refactoring easier. The kwargs acts as an override,
        # meaning if start, begin, or time is specified in kwargs, that value will be used instead
        # of accessing the attribute directly. This is quite useful when you want to modify the
        # value of an attribute from a subclass but let the parent class still handle the result.
        start = a.get(TagAttributesEnum.START + TagAttributesEnum.TIME, None, kwargs)

        # Getting the url in the same, raw fashion as the start property.
        url = a.get(TagAttributesEnum.URL, None, kwargs)

        # Here play is a boolean value so getAsBool is used instead of get, which converts the value
        # from a string into a boolean where 'true', 'yes', 'on', and '1' all equate to True and
        # anything else is False.
        play = a.getAsBool(TagAttributesEnum.AUTO_PLAY, False, kwargs)

        # Get as enumerated returns an enumerated result based on the enumeration class specified as
        # the second argument. The third argument then becomes the default value to return if the
        # value is not specified OR the value specified doesn't match any of the values in the
        # enumeration class. If you look at the AspectRatioEnum class you will see entries like:
        #       WIDESCREEN  = [1.7778, ['wide', 'widescreen', 'sixteen-nine']]
        # where the first element of the list is the enumerated value and the second element is a
        # list of possible values the user can specify that equate to the given enumeration entry.
        # In this case, if the user specifies:
        #   [#youtube aspect:widescreen ...]
        #   [#youtube aspect:wide ...]
        # the getAsEnumerated method would return 1.7778. However, if the user specified:
        #   [#youtube aspect:foo ...]
        # None would be returned because foo isn't specified in any of the enumeration values within
        # the class and the default value is set to None.
        #
        # Another key point here is the use of the allowFailure argument. When True it means an
        # invalid value will fail silently instead of logging as an error. This error logging will
        # be presented to the user during page previews once we get it implemented. The reason for
        # allowing silent failure in this case (which is the most common use of it) is that the
        # aspect ratio can be specified either as an enumerated value, or directly as a float. So
        # if this enumerated access fails, it means the value is likely a float. We don't want to
        # log the error, instead we want to try to access the attribute as a float instead as is
        # done below.
        aspect = a.getAsEnumerated(TagAttributesEnum.ASPECT_RATIO, AspectRatioEnum, None,
                                   kwargs, allowFailure=True)

        # Here if the aspect ratio is None the aspect ratio should be accessed as a float value.
        # Now this case doesn't allow failure since it is the last attempt to access the attribute.
        # If the attribute get fails this time, the failure should be logged because the attribute
        # was specified incorrectly. NOTE: failures only occur if the property was specified but
        # could not be typecast/converted into the format specified by the get method. No failure
        # occurs if the property just wasn't specified.
        if not aspect:
            aspect = a.getAsFloat(TagAttributesEnum.ASPECT_RATIO, None)

        # Finally we've got all of the attributes we need for the tag. I try to put these all first
        # because it makes it easier to maintain and reference. Now we have to modify the states
        # according to the given properties.

        if url:
            try:
                result = OEmbedRequest.get(url, self._OEMBED)
                if self._processor.debug:
                    self._log.write(u'YouTube oEmbed result: ' + unicode(result))

                if not aspect:
                    width  = result.get('width', None)
                    height = result.get('height', None)
                    if width and height:
                        try:
                            aspect = float(width)/float(height + 20.0)
                        except ValueError:
                            pass

                res = YouTubeTag._URL_RE.search(result.get('html', ''))

                a.render['code'] = res.group('code')
            except Exception, err:
                if self._processor.debug:
                    self._log.writeError(u'YouTube oEmbed error', err)

                a.render['code'] = u''
        else:
            a.render['code'] = YouTubeTag._DEFAULT_CODE

            if self._processor.privateView:
                MarkupTagError(tag=self, code='missing-url-attribute').log()

        # a.render is a dict for storing arbitrary render data keys and values that will be used
        # by the mako template.
        a.render['autohide'] = u'2'
        a.render['autoplay'] = u'1' if play else u'0'

        if start:
            if start.find(':') != -1:
                s = start.strip().split(':')
                try:
                    start = unicode(60*int(s[0]) + int(s[-1]))
                except ValueError:
                    start = 0

            a.render['start'] = u'&start=' + unicode(start)
        else:
            a.render['start'] = u''

        # All VizmeML tags have associated tag classes to distinguish them in the page. The
        # universal format is v-gvml-[TAGNAME], which is applied to the outermost DOM element. It is
        # however, also nice to add tag classes to other DOM elements within the rendered DOM. Here
        # I'm adding v-gvml-youtube-player to the 'player' group of render data. This allows the
        # client to access a particular portion of the DOM reliably.
        a.addTagClasses('player', 'player')

        # DOMRenderData, which is the base class for AttributeData, is made up of a bunch of
        # DOMOrganizer classes (and subclasses). A DOMOrganizer maintains a list of property
        # values for the various groups of render data. The a.settings is an organizer that let's
        # you specify key/value pairs for various groups. Here the 'aspect' property is set on the
        # 'player' group. When the Mako template is rendered, all a.settings for a particular group
        # are rendered as a JSON-encoded string to the data-v-sets DOM attribute.
        if not aspect:
            aspect = AspectRatioEnum.WIDESCREEN[0]

        a.settings.add('aspect', aspect if aspect else AspectRatioEnum.WIDESCREEN[0], 'player')

        # The a.classes is a list, organizer, where you specify the value to add to the list for
        # specific group.
        a.classes.add('v-vmlAspect', 'player')

        # a.styles is another dict-like DOM group organizer, with key value pairs being assigned
        # to a particular group.
        a.styles.add('width','100%', 'player')

