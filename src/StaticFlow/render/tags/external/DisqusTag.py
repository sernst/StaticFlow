# DisqusTag.py
# (C)2012-2013
# Scott Ernst

from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.MarkupTag import MarkupTag

#___________________________________________________________________________________________________ DisqusTag
class DisqusTag(MarkupTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    # The tag identifier, i.e. [#youtube]
    TAG            = 'disqus'

    # The Mako template used to render the tag. This path is relative to the root path
    # /vizme/templates/mako/.
    TEMPLATE       = 'markup/external/disqus.mako'

    # Specifies whether the tag should be rendered like a <div> tag when True or like a <span> tag
    # when False. Use False only for tags that should be inline with text.
    BLOCK_DISPLAY  = True

    # This is the attribute for the tag that can be specified without defining the property. In the
    # DisqusTag case, this is the 'url' property meaning that:
    #   [#youtube url:http://www.youtube.com/video/5j3hgdo2]
    # can also be specified as:
    #   [#youtube http://www.youtube.com/video/5j3hgdo2]
    # omitting the url: attribute prefix. Not all tags have a primary attribute, in which case this
    # can be set to None or omitted.
    PRIMARY_ATTR   = None

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        t = TagAttributesEnum
        return MarkupTag.getAttributeList()

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


