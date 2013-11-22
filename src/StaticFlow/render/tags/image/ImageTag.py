# ImageTag.py
# (C)2012-2013
# Scott Ernst

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
        return MarkupTag.getAttributeList() + t.ALIGNMENT + t.INLINE + t.WIDTH + t.HEIGHT + t.URL \
            + t.LINKED + t.FIXED + t.TARGET + t.WINDOW_TARGET + t.SHRINK + t.DIRECT \
            + t.MAX_HEIGHT + t.MAX_WIDE

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
            640,
            defaultUnit='px',
            unitType=int)

        tall = a.getAsUnit(
            TagAttributesEnum.HEIGHT,
            360,
            defaultUnit='px',
            unitType=int)

        url, urlKeyData = a.get(
            TagAttributesEnum.URL,
            None,
            returnKey=True)

        link = a.getAsBool(
            TagAttributesEnum.LINKED,
            None,
            allowFailure=True)

        target = a.getAsKeyword(
            TagAttributesEnum.TARGET + TagAttributesEnum.WINDOW_TARGET,
            None)

        fixed = a.getAsBool(
            TagAttributesEnum.FIXED,
            False)

        if link is None:
            link = a.getAsURL(TagAttributesEnum.LINKED, None)

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

        w = wide.value
        h = tall.value

        if fixed:
            a.styles.add({'width':unicode(w) + 'px', 'height':unicode(h) + 'px'})
            a.settings.add('fixed', 1)
        else:
            a.styles.add({'max-width':unicode(w) + 'px', 'max-height':unicode(h) + 'px'}, 'imageBox')
            a.data.add({'width':unicode(wide), 'height':unicode(tall)})

        a.data.add('src', url, 'image')
        a.classes.add('sfml-lazyImage', 'image')
        a.classes.add('sfml-imageBox', 'imageBox')

        if target is None:
            target = '_blank'
        elif target == 'new':
            target = '_blank'
        elif target in ['me', 'self', 'this']:
            target = '_self'
        else:
            target = a.get(TagAttributesEnum.WINDOW_TARGET + TagAttributesEnum.TARGET)

        if link:
            out = link if isinstance(link, basestring) else url
            if target != '_self':
                out = target + '|' + out

            a.vdata.add('clkr', out)
            a.addTagClasses('link')
            a.classes.add('v-transLink')

        if not self.isBlockDisplay:
            a.addTagClasses('inline')

        #-------------------------------------------------------------------------------------------
        # ALIGNMENT
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
