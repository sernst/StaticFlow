# ImageTag.py
# (C)2012-2013
# Scott Ernst

from pyaid.string.StringUtils import StringUtils

from StaticFlow.components.LocalImage import LocalImage
from StaticFlow.render.enum.AlignmentEnum import AlignmentEnum
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.error.MarkupAttributeError import MarkupAttributeError
from StaticFlow.render.tags.MarkupTag import MarkupTag

#___________________________________________________________________________________________________ ImageTag
class ImageTag(MarkupTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG             = 'image'
    TEMPLATE        = 'markup/image/imageBase.mako'
    PRIMARY_ATTR = TagAttributesEnum.URL[0]

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: isBlockDisplay
    @property
    def isBlockDisplay(self):
        return not self.attrs.getAsBool(TagAttributesEnum.INLINE, False)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getAttributeList
    @classmethod
    def getAttributeList(cls):
        t = TagAttributesEnum
        return MarkupTag.getAttributeList() + t.ALIGNMENT + t.WIDTH + t.HEIGHT + t.URL + t.INLINE

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a = self.attrs

        align = a.getAsEnumerated(
            TagAttributesEnum.ALIGNMENT,
            AlignmentEnum,
            AlignmentEnum.CENTER)

        wide = a.getAsUnit(
            TagAttributesEnum.WIDTH,
            0,
            defaultUnit='px',
            unitType=int)

        tall = a.getAsUnit(
            TagAttributesEnum.HEIGHT,
            0,
            defaultUnit='px',
            unitType=int)

        url, urlKeyData = a.get(
            TagAttributesEnum.URL,
            None,
            returnKey=True)

        if not url:
            MarkupAttributeError(
                tag=self,
                errorDef=MarkupAttributeError.ERROR_DEFINITION_NT(
                    u'no-image-specified',
                    u'No Image Specified',
                    u'Missing image URL or path definition attribute.'),
                attribute=urlKeyData[0],
                attributeData=urlKeyData[1],
                attributeGroup=TagAttributesEnum.URL).log()

        #--- LOCAL IMAGE SIZE
        #       For local images, try to get the size from the image file if it exists
        if not StringUtils.begins(url, [u'http', u'//']):
            img = LocalImage(self.processor.page, url)
            if img.exists:
                wide.value = img.width
                tall.value = img.height

        w = wide.value if wide.value > 0 else 640
        h = tall.value if tall.value > 0 else 360

        #--- HTML ATTRIBUTES ---#
        a.styles.add({'max-width':unicode(w) + 'px', 'max-height':unicode(h) + 'px'}, 'imageBox')
        a.data.add({'width':unicode(wide), 'height':unicode(tall)})
        a.data.add('src', url, 'image')
        a.classes.add('sfml-lazyImage', 'image')
        a.classes.add('sfml-imageBox', 'imageBox')

        if a.getAsBool(TagAttributesEnum.INLINE, False, kwargs, True):
            a.styles.add({'display':'inline-block'}, 'imageBox')

        #--- HORIZONTAL ALIGNMENT
        #       Set the alignment of the image within the box, which defaults sto center.
        if align == 'r':
            a.styles.add({
                    'text-align':'right',
                    'margin:':'auto 0 auto auto'},
                'imageBox')
        elif align == 'l':
            a.styles.add({
                    'text-align':'left',
                    'margin':'auto auto 0 auto'},
                'imageBox')
        else:
            a.styles.add({
                    'text-align':'center',
                    'margin':'auto'},
                'imageBox')
