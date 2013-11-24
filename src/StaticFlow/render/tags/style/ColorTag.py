# ColorTag.py
# (C)2012
# Scott Ernst

from pyaid.color.ColorValue import ColorValue
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.tags.MarkupBlockTag import MarkupBlockTag
from pyaid.string.StringUtils import StringUtils

#___________________________________________________________________________________________________ ColorTag
class ColorTag(MarkupBlockTag):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TAG            = 'color'
    TEMPLATE       = 'markup/spanBase.mako'
    STRIP_POLICY   = MarkupBlockTag.STRIP_NEWLINES
    NEWLINE_POLICY = MarkupBlockTag.BREAK_ON_NEWLINES
    PRIMARY_ATTR   = TagAttributesEnum.NAME[0]

    _COLOR_PROPS = [
        'hex', 'rgb', 'rgb_one', 'rgbone', 'hsl', 'hslone', 'hsl_one', 'hsv', 'hsvone', 'hsv_one'
    ]
    _RGB_KEYS    = ['r','g','b']
    _HSL_KEYS    = ['h','s','l']
    _HSV_KEYS    = ['h','s','v']

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
        return MarkupBlockTag.getAttributeList() + t.NAME+ t.COLOR + ColorTag._COLOR_PROPS

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _renderImpl
    def _renderImpl(self, **kwargs):
        a   = self.attrs
        raw = a.getAsKeyword(TagAttributesEnum.NAME + TagAttributesEnum.COLOR, None)
        if raw:
            c = raw.rstrip('+-')
        else:
            c = raw

        if c in ['hgh', 'high', 'highlight']:
            vclass = 'v-S-hgh'
        elif c in ['lnk', 'link']:
            vclass = 'v-S-lnk'
        elif c in ['sft', 'soft']:
            vclass = 'v-S-sft'
        elif c in ['btn', 'button']:
            vclass = 'v-S-fbn'
        elif c in ['fcl', 'focal']:
            vclass = 'v-S-fcl'
        elif c in ['bck', 'back', 'background']:
            vclass = 'v-S-bckfront'
        elif c in ['dod', 'dodge']:
            vclass = 'v-S-dodfront'
        elif c in ['brn', 'burn']:
            vclass = 'v-S-brnfront'
        elif c in ['bor', 'border']:
            vclass = 'v-S-borfront'
        elif c in ['bbtn', 'backbutton', 'buttonback']:
            vclass = 'v-S-bbnfront'
        elif c is not None:
            vclass = None
            if self._setColor(ColorValue(raw)):
                return
        else:
            vclass = None

        if vclass is not None:
            bendCount = ColorValue.getBendCount(raw)
            if bendCount == 0:
                bendSuffix = ''
            else:
                bendSuffix = ('-d' if bendCount < 0 else '-u') + str(abs(bendCount))

            a.classes.add(vclass + bendSuffix, a.styleGroup)
            return

        props = ColorTag._COLOR_PROPS
        for p in props:
            c = a.get(p, None)
            if c is None:
                continue

            try:
                if self._setColor(c, p):
                    return
            except Exception, err:
                self._processor.logger.writeError('ColorTag: %s | %s -> %s' % (p, str(c), str(type(c))), err)
                a.logAttributeError(p, c) #TODO: This no longer works.

#___________________________________________________________________________________________________ _setColor
    def _setColor(self, color, colorMode =None):
        if color is None:
            return False

        if isinstance(color, list):
            normalized = colorMode.endswith('one')
            if colorMode.startswith('rgb'):
                keys = ColorTag._RGB_KEYS
            elif colorMode.startswith('hsl'):
                keys = ColorTag._HSL_KEYS
            elif colorMode.startswith('hsv'):
                keys = ColorTag._HSV_KEYS
            else:
                keys = ColorTag._RGB_KEYS

            c     = {}
            norms = True
            for i in range(len(color)):
                raw        = color[i]
                value      = float(raw.rstrip('+-'))
                c[keys[i]] = value

                if not normalized:
                    norms = norms and (raw.find('.') != -1 and value <= 1.0)

            c = ColorValue(c, normalized or norms)

            if StringUtils.ends(color[-1], ['+', '-']):
                c.bend(color[-1])
        else:
            c = color

        self.attrs.styles.add(
            'color', c.web if isinstance(c, ColorValue) else unicode(c), self.attrs.styleGroup
        )
        return True

