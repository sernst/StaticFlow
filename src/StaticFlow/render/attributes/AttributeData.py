# AttributeData.py
# (C)2012-2013
# Scott Ernst

import re
from collections import namedtuple

from pyaid.color.ColorValue import ColorValue
from pyaid.ArgsUtils import ArgsUtils
from pyaid.list.ListUtils import ListUtils
from pyaid.reflection.Reflection import Reflection
from pyaid.text.BlockDefinition import BlockDefinition
from pyaid.text.BlockSyntaxEnum import BlockSyntaxEnum
from pyaid.text.TextAnalyzer import TextAnalyzer

from StaticFlow.render.dom.DomRenderData import DomRenderData
from StaticFlow.render.enum.GeneralSizeEnum import GeneralSizeEnum
from StaticFlow.render.enum.TagAttributesEnum import TagAttributesEnum
from StaticFlow.render.error.MarkupAttributeError import MarkupAttributeError
from StaticFlow.render.error.MarkupTagError import MarkupTagError
from StaticFlow.render.attributes.UnitAttribute import UnitAttribute

#___________________________________________________________________________________________________ NullPasser
NullPasser = namedtuple('NullPasser', 'id')

#___________________________________________________________________________________________________ ErrorPasser
ErrorPasser = namedtuple('ErrorPasser', 'name')

#___________________________________________________________________________________________________ AttributeData
class AttributeData(DomRenderData):
    """Handles the attribute and data properties and state for rendering VizmeML tags."""

#===================================================================================================
#                                                                                       C L A S S

    GLOBAL_CLASS_PREFIX = 'v-gvml'

    _PARSE_BLOCKS = [
        BlockDefinition.createQuoteDef(BlockDefinition.BLOCKED),
        BlockDefinition.createLiteralDef(BlockDefinition.BLOCKED),
        BlockDefinition.createVizmeMLAttributeDef()
    ]

    _LIST_BLOCKS = [
        BlockDefinition.createQuoteDef(BlockDefinition.BLOCKED),
        BlockDefinition.createLiteralDef(BlockDefinition.BLOCKED, True),
        BlockDefinition.createCommaDelimitedListDef(None, True, True)
    ]

    _PRIMARY_ATTR_QUOTED_RE = re.compile('(^|[^,:\s\t\n])[\s\t\n]*$')

    _ILLEGAL_ID_CHARS_RE  = re.compile('[^@A-Za-z0-9_~]+')
    _REMOVE_WHITESPACE_RE = re.compile('[\s\t\n]+')

    _TRUE_BOOLEANS  = ['true', 't', 'on', '1', 'yes', 'y']
    _FALSE_BOOLEANS = ['false', 'f', 'off', '0', 'no', 'n']

    _INVALID_theme_CHARS = re.compile('[^A-Za-z0-9_]+')
    _COMMA_LIST_CLEANUP  = re.compile('[\s\t\n]*,[\s\t\n]*')

    _ROOT_THEME_PREFIX   = 'v-STYLE-'
    _THEME_PREFIX        = 'v-S-'
    _GSTYLE_PREFIX       = 'v-SG-'
    _BORDER_THEME_PREFIX = 'v-SB-'

#___________________________________________________________________________________________________ __init__
    def __init__(self, tag, source, **kwargs):
        """Creates a new instance of VMLAttributes and parses the specified attribute source in
        preparation for rendering the VizmeML tag DOM.

        @@@param tag:MarkupTag
            The tag that owns this render data.

        @@@param processor:VMLProcessor
            The VizmeML processor that is managing the rendering process.

        @@@param source:string
            The raw attribute string to be parsed into attributes for rendering.
        """

        DomRenderData.__init__(self, **kwargs)
        self._tag                             = tag
        self._processor                       = tag.processor
        self._source                          = source
        self._themeChanged                    = False
        self._auxiliaryRenderData            = None
        self._auxiliaryRenderDataExtractions = None

        try:
            self._props = self._parse()
        except Exception, err:
            MarkupTagError(
                tag=tag,
                code=MarkupTagError.CORRUPT_ATTRS
            ).log()
            if CONFIG.VERBOSE:
                tag.log.writeError([
                    'VML ATTRIBUTE PARSE FAILURE',
                    'raw: ' + str(source),
                    'tag: ' + str(tag)
                ], err)
            return

        # Get the primary attribute if one has been assigned
        self._primaryAttribute = tag.getClassAttr('PRIMARY_ATTR', None)
        if isinstance(self._primaryAttribute, list):
            self._primaryAttribute = self._primaryAttribute[0]

        additionalProps = ArgsUtils.get('attributes', None, kwargs)
        if additionalProps:
            self._props = dict(self._props.items() + additionalProps.items())

        #-------------------------------------------------------------------------------------------
        # ATTRIBUTE ERROR CHECKING
        allowedAttrs = self._tag.__class__.getAttributeList()
        if allowedAttrs is not None:
            if self._primaryAttribute:
                allowedAttrs = allowedAttrs + ['value']
            for k in self._props.keys():
                if not k in allowedAttrs:
                    val, keyData = self.get([k], returnKey=True)
                    self.logAttributeError(
                        keyData=keyData,
                        keyGroup=None,
                        rawValue=val,
                        code=MarkupAttributeError.INVALID_ATTRIBUTE,
                    )

        self.id.add(self.get(TagAttributesEnum.ID, self.uid).replace(' ', ''))
        self.classes.add(self.get(TagAttributesEnum.HTML_CLASS, None))

        htmlAttrs = self.get(TagAttributesEnum.HTML_ATTR, None)
        if htmlAttrs:
            if not isinstance(htmlAttrs, list):
                htmlAttrs = [htmlAttrs]
            for attr in htmlAttrs:
                parts = attr.split('=')
                if len(parts) == 1:
                    self.attrs.add(parts[0], '1')
                else:
                    self.attrs.add(parts[0], parts[1])

        css, keyData = self.get(TagAttributesEnum.HTML_STYLE, returnKey=True)
        if css:
            if isinstance(css, basestring):
                css = [css.split(':')]
            else:
                index = 0
                while index < len(css):
                    css[index] = css[index].split(':')
                    index += 1

            for c in css:
                if len(c) == 1:
                    MarkupAttributeError(
                        keyData=keyData,
                        keyGroup=TagAttributesEnum.HTML_STYLE,
                        rawValue=css,
                        code=MarkupAttributeError.BAD_ATTRIBUTE_VALUE
                    ).log()
                    continue
                elif len(c) > 2:
                    c = [c[0], u''.join(c[1:])]

                self.styles.add(c[0], c[1], self.styleGroup)

        data = dict()
        raw  = self.get(TagAttributesEnum.HTML_DATA, [])
        if raw:
            if not isinstance(raw, list):
                raw = [raw]
            for r in raw:
                r = r.split('=', 1)
                if len(r) == 1:
                    data[r[0]] = u'1'
                else:
                    data[r[0]] = r[1]
        self.data.add(data)

        # Adds the default tag classes to the root class list
        self.addTagClasses()

        #-------------------------------------------------------------------------------------------
        # THEME: If theme is specified, lookup the theme and return its class
        themeValue, themeKeyData = self.get(TagAttributesEnum.THEME, None, returnKey=True)
        if themeValue:
            self._theme = self._processor.profile.getTheme(themeValue)
            # Handles both success and failure cases.
            if self._theme:
                self._themeChanged = True
                self.classes.add(AttributeData._ROOT_THEME_PREFIX + self._theme.id)
                self.themeID.add(u'@' + self._theme.id)
            else:
                self._themeChanged = False
                self.logAttributeError(
                    keyData=themeKeyData,
                    keyGroup=TagAttributesEnum.THEME,
                    rawValue=themeValue,
                    code='no-such-theme'
                )
        else:
            self._themeChanged = False
            self._theme        = None

        #-------------------------------------------------------------------------------------------
        # ACCENT THEME: If theme or accent is specified make the appropriate change. If no accent is
        #               specified, search through tag parents to find the last accent change and
        #               inherit that value. If no inherited value is found, likely because of no
        #               parent the default False is applied.
        accent = self.getAsBool(TagAttributesEnum.ACCENTED, None)
        if isinstance(accent, bool):
            self._explicitAccent = True
            self._themeChanged   = True
            self._accented       = accent
            self.classes.add(u'v-STY-ACCENT' if self._accented else u'v-STY-NORMAL')
        else:
            self._explicitAccent = False
            self._accented       = None
            if self.themeChanged:
                self.classes.add(u'v-STY-ACCENT' if self._accented else u'v-STY-NORMAL')

        # If the theme was changed add a styleInner class to control to resizing of the child
        if self._themeChanged:
            self._classes.add('v-gvml-styleInner', self.styleGroup)

        #-------------------------------------------------------------------------------------------
        # CLEAR FLOATS
        clear = self.getAsBool(TagAttributesEnum.CLEAR, None, allowFailure=True)
        if not clear:
            clear = self.getAsKeyword(TagAttributesEnum.CLEAR, None)
        if clear:
            if clear == 'left':
                self.styles.add('clear', 'left')
            elif clear == 'right':
                self.styles.add('clear', 'right')
            else:
                self.styles.add('clear', 'both')

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: tag
    @property
    def tag(self):
        return self._tag

#___________________________________________________________________________________________________ GS: explicitAccent
    @property
    def explicitAccent(self):
        return self._explicitAccent

#___________________________________________________________________________________________________ GS: accented
    @property
    def accented(self):
        """Specifies whether or not the tag should be rendered in an accented or non-accented
        state. If the accent value is not set explicitly as a tag attribute this value is inherited
        from its parents.

        @@@returns bool
        """
        if self._accented is None:
            # Search through parent tags for an explicit accent and if one exists inherit the
            # accented state from that parent.
            parent = self._tag.parent
            while parent:
                if parent.attrs.explicitAccent:
                    self._accented = parent.attrs.accented
                    break
                parent = parent.parent

        return self._accented

#___________________________________________________________________________________________________ GS: primaryAttribute
    @property
    def primaryAttribute(self):
        """Returns the primary attribute for the tag, i.e. the attribute that can be specified
        without naming it within the tag. If no primary attribute exists for a tag this value will
        be None.

        @@@returns string
        """
        return self._primaryAttribute

#___________________________________________________________________________________________________ GS: theme
    @property
    def theme(self):
        """The VizmeML theme to use in rendering this tag. If the theme is not set explicitly as a
        tag attribute, the theme will be inherited from the tag's parents all the way up to the
        default theme specified by the VMLProcessor.

        @@@returns Web_theme
        """
        if self._theme:
            return self._theme

        parent = self._tag.parent
        theme  = None
        while parent and not theme:
            theme  = parent.attrs.theme
            parent = parent.parent

        if theme is None:
            return self._processor.theme

        return theme

#___________________________________________________________________________________________________ GS: backColors
    @property
    def backColors(self):
        """The background color bundle to use in rendering the tag. It will be either the background
        color bundle or the fill color bundle depending on the tag's accent property.

        @@@returns Web_ScenicColorBundle
        """
        return self.theme.fillColorBundle if self.accented else self.theme.backColorBundle

#___________________________________________________________________________________________________ GS: focalColors
    @property
    def focalColors(self):
        """The focal color bundle to use in rendering the tag. It will be either the front color
        bundle or the accent color bundle depending on the tag's accent property.

        @@@returns Web_FocalColorBundle
        """
        return self.theme.accentColorBundle if self.accented else self.theme.frontColorBundle

#___________________________________________________________________________________________________ GS: styleGroup
    @property
    def styleGroup(self):
        """Returns the root group name on which to apply styles depending on whether or not the
        theme was changed on the tag. The root group name is None.

        @@@returns string
        """
        return 'styled' if self.themeChanged else None

#___________________________________________________________________________________________________ GS: themeChanged
    @property
    def themeChanged(self):
        """Specifies whether or not the theme was changed explicitly by the VizmeML tag definition
        either by changing to a different theme or switching between accent and normal theme mode.
        When such an event occurs, the DOM for the tag must be rendered differently to handle the
        CSS class hierarchy for the change.

        @@@returns bool
        """
        return self._themeChanged

#___________________________________________________________________________________________________ GS: uid
    @property
    def uid(self):
        """ Returns the formatted unique identifier for the tag. Every VizmeML tag is given a
        unique identifier in the converted HTML to allow for navigational access. The format
        is [COMMON_PREFIX]-[label]-[index].  The uid is ignored if an htmlid is specified
        explicitly in the tag definition.

        @@@return string
        """
        return self._processor.uid + u'-' + self._tag.tagName + u'-' + unicode(self._tag.index)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ items
    def items(self):
        """Behaves like dict.items(), returning a list of property tuples."""
        return self._props.items()

#___________________________________________________________________________________________________ disableAuxiliaryKey
    def disableAuxiliaryKey(self, keys):
        if self._auxiliaryRenderDataExtractions is None:
            self._auxiliaryRenderDataExtractions = []

        if not isinstance(keys, list):
            keys = [keys]

        for k in keys:
            if not k in self._auxiliaryRenderDataExtractions:
                self._auxiliaryRenderDataExtractions.append(k)

        return True

#___________________________________________________________________________________________________ addAuxiliaryRenderData
    def addAuxiliaryRenderData(self, renderData, join=True):
        """ Adds an auxiliary AttributeData instance that behaves as a secondary access point for
            attribute access and, if specified, will also join this AttributeData instance
            properties.
        """

        if self._auxiliaryRenderData is None:
            self._auxiliaryRenderData            = [renderData]

            if self._auxiliaryRenderDataExtractions is None:
                self._auxiliaryRenderDataExtractions = []
            self._auxiliaryRenderDataExtractions += TagAttributesEnum.GROUP
        else:
            if renderData in self._auxiliaryRenderData:
                return False

            self._auxiliaryRenderData.insert(0, renderData)

        if join:
            self.join(renderData)

        return True

#___________________________________________________________________________________________________ logAttributeError
    def logAttributeError(self, keyData, keyGroup, rawValue, value =None, message =None, code =None,
                          critical =False):
        """Logs an attribute failure with the tag in which the error failed.

        @@@param attributeName:string
            The name of the attribute that caused the error.

        @@@param badValue:mixed
            The value that was returned and caused the failure.
        """

        if isinstance(keyData, list):
            keyName       = keyData[0]
            attributeData = keyData[1]
        elif isinstance(keyData, basestring):
            keyName       = keyData
            attributeData = None
        else:
            keyName       = None
            attributeData = None

        v = MarkupAttributeError(
            tag=self._tag,
            message=message,
            code=code,
            attribute=keyName,
            attributeGroup=keyGroup,
            attributeData=attributeData,
            value=value,
            rawValue=rawValue,
            critical=critical
        ).log()

#___________________________________________________________________________________________________ addTagClasses
    def addTagClasses(self, suffix ='', group =None):
        """Adds the contextual tag CSS classes to the list of render CSS classes.

        @@@param suffix:string -default=''
            If a suffix is specified it will be appended onto the classes when added. This is
            useful for creating additional contextual classes based on a tag's state. It is also
            used to create subclasses on sub-elements of the tag.

        @@@param group:string -default=None
            Specifies the group on which to add the class. If no group is specified the class will
            be added to the root class list and therefore rendered to the root DOM element of the
            tag.
        """

        self._classes.add([self._getGlobalClass(suffix)], group)

#___________________________________________________________________________________________________ set
    def set(self, keys, value, defaultKey =None):
        """Sets the value of the specified tag attribute. All possible tag keys are passed to make
        sure that existing values are overwritten instead of causing data duplication.

        @@@param keys:string,list
            A single or list of keys for which the attribute should be set. If one of those keys
            is found the value will overwrite the existing value. Otherwise, the attribute will
            be created for subsequent access.

        @@@param value:mixed
            The value to assign to the attribute.

        @@@param defaultKey:mixed
            Optionally specify the preferred key to assign the value to if the attribute must
            be created. If the value is not specified, the first key in the keys list will be
            used instead.
        """

        if isinstance(keys, basestring):
            self._props[keys.lower()] = [value, None]
            return

        for k in keys:
            k = k.lower()
            if k in self._props:
                self._props[k] = [value, None]
                return

        self._props[keys[0] if defaultKey is None else defaultKey] = [value, None]

#___________________________________________________________________________________________________ remove
    def remove(self, keys, all =True):
        """Removes the specified key or keys from the attributes dictionary."""

        if not isinstance(keys, list):
            keys = [keys]

        success = False
        for k in keys:
            k = k.lower()
            if k in self._props:
                del self._props[k]
                if not all:
                    return True
                else:
                    success = True

        return success

#___________________________________________________________________________________________________ has
    def has(self, keys):
        """Specified whether or not the attribute exists."""
        return self.get(keys, None) is not None

#___________________________________________________________________________________________________ hasTrait
    def hasTrait(self, keys):
        """Determines whether or not the trait, specified by the single or list of trait keywords
        in keys, exists.

        @@@param keys:string,list
            A single or list of trait keywords to search for within the traits specified by the tag.

        @@@return bool
            Returns True if the trait is found, or False otherwise.
        """

        traits = self.get(['traits','trait'], [])
        for k in keys:
            if k in traits:
                return True

        return False

#___________________________________________________________________________________________________ get
    def get(self, keys, defaultValue =None, overrides =None, extract =False, returnKey =False):
        """Retrieves the attribute specified by the keys, or if the attribute was not specified in
        the tag the defaultValue.

        @@@param keys:string,list
            A single or list of key names for the key to retrieve.

        @@@param defaultValue:mixed
            The value to return if the key is not specified or is invalid.

        @@@return string,list,mixed
            Returns the string value of the attribute, or a list if the attribute string was a
            comma-delimited list, if the attribute exists. Otherwise returns the defaultValue.
        """

        if isinstance(keys, basestring):
            keys = [keys]

        if isinstance(overrides, dict):
            for k in keys:
                k = k.lower()
                if k in overrides:
                    v = overrides[k]
                    if extract:
                        del overrides[k]

                    if returnKey:
                        return v, [k, None]
                    return v

        if not self._props:
            if returnKey:
                return defaultValue, None
            return defaultValue

        if self.primaryAttribute and self.primaryAttribute in keys:
            searchKeys = ['value'] + keys
        else:
            searchKeys = keys

        for k in searchKeys:
            k = k.lower()
            if k in self._props:
                v = self._props[k]
                if extract:
                    del self._props[k]

                if returnKey:
                    try:
                        return v[0], [k, v[1]]
                    except Exception, err:
                        self._tag.log.writeError([
                            u'Failed to return key with data',
                            u'Key: ' + unicode(k),
                            u'Value: ' + unicode(v),
                            u'Type: ' + unicode(type(v)),
                            u'Attrs: ' + unicode(self._props)
                        ], err)

                return v[0]
            elif self._auxiliaryRenderData:
                if ListUtils.contains(self._auxiliaryRenderDataExtractions, keys):
                    continue

                null = NullPasser('null')
                for rd in self._auxiliaryRenderData:
                    v, keyData = rd.get(keys, null, returnKey=True)
                    if v == null:
                        continue

                    if extract:
                        self._auxiliaryRenderDataExtractions += keys

                    if returnKey:
                        return v, keyData
                    return v

        if returnKey:
            return defaultValue, None
        return defaultValue

#___________________________________________________________________________________________________ getAsEnumerated
    def getAsEnumerated(self, keys, enumerationClass, defaultValue =None, overrides =None,
                        allowFailure =False, extract =False, returnKey =False):
        """Retrieves the attribute specified by the keys, or if the attribute was not specified in
        the tag the defaultValue. The value is filtered by the enumerationClass, and the result
        returned the one specified within the enumerationClass as a convenience for using the
        value. If the raw value is not found within the enumerationClass, the defaultValue is
        returned in its place.

        @@@param keys:string,list
            A single or list of key names for the key to retrieve.

        @@@param enumerationClass:Class
            A class of enumeration values to retrieve by reflection and use to parse the
            appropriate enumerated return value.

        @@@param defaultValue:mixed
            The value to return if the key is not specified or is invalid.

        @@@return string,list,mixed
            Returns the enumerated value of the attribute. Otherwise returns the defaultValue.
        """

        out, keyData = self.getAsKeyword(
            keys=keys, defaultValue=None, overrides=overrides, extract=extract, returnKey=True,
            implode=False
        )
        if out is None:
            dv = defaultValue[0] if isinstance(defaultValue, list) else defaultValue
            if returnKey:
                return dv, keyData
            return dv

        choices = Reflection.getReflectionList(enumerationClass)
        if isinstance(out, list):
            outList = []
            for item in out:
                found = False
                for c in choices:
                    if item in c[1]:
                        outList.append(c[0])
                        found = True
                        break

                if not found and not allowFailure:
                    self.logAttributeError(
                        keyData=keyData,
                        keyGroup=keys,
                        rawValue=item,
                        code=MarkupAttributeError.BAD_ATTRIBUTE_VALUE
                    )
            if outList:
                if returnKey:
                    return outList, keyData
                return outList
        else:
            for c in choices:
                if out in c[1]:
                    if returnKey:
                        return c[0], keyData
                    return c[0]

        if not allowFailure:
            self.logAttributeError(
                keyData=keyData,
                keyGroup=keys,
                rawValue=out,
                code=MarkupAttributeError.BAD_ATTRIBUTE_VALUE
            )

        dv = defaultValue[0] if isinstance(defaultValue, list) else defaultValue
        if returnKey:
            return dv, keyData
        return dv

#___________________________________________________________________________________________________ getAsTShirtSize
    def getAsTShirtSize(self, keys, defaultValue =None, overrides =None, allowFailure =False,
                        extract =False, returnKey =False, values =None):
        raw, keyData = self.getAsEnumerated(
            keys=keys,
            enumerationClass=GeneralSizeEnum,
            defaultValue=None,
            overrides=overrides,
            extract=extract,
            returnKey=True,
            allowFailure=allowFailure
        )

        if raw is None:
            if returnKey:
                return defaultValue, keyData
            return defaultValue

        if values:
            if raw == GeneralSizeEnum.xxsmall[0]:
                out = values[0] if len(values) > 0 else raw
            elif raw == GeneralSizeEnum.xsmall[0]:
                out = values[1] if len(values) > 1 else raw
            elif raw == GeneralSizeEnum.small[0]:
                out = values[2] if len(values) > 2 else raw
            elif raw == GeneralSizeEnum.medium[0]:
                out = values[3] if len(values) > 3 else raw
            elif raw == GeneralSizeEnum.large[0]:
                out = values[4] if len(values) > 4 else raw
            elif raw == GeneralSizeEnum.xlarge[0]:
                out = values[5] if len(values) > 5 else raw
            elif raw == GeneralSizeEnum.xxlarge[0]:
                out = values[6] if len(values) > 6 else raw
            elif raw == GeneralSizeEnum.none[0]:
                out = values[7] if len(values) > 7 else raw
            else:
                out = raw
        else:
            out = raw

        if returnKey:
            return out, keyData
        return out

#___________________________________________________________________________________________________ getAsKeyword
    def getAsKeyword(self, keys, defaultValue =None, overrides =None, allowFailure =False,
                     extract =False, returnKey =False, implode =True):
        """Retrieves the attribute specified by the keys, or if the attribute was not specified in
        the tag the defaultValue. Prior to returning the value the value is formatted as a keyword,
        which means removing spaces and lowering the capitalization. Also, if the value was a list
        it will be returned as a colon delimited string.

        @@@param keys:string,list
            A single or list of key names for the key to retrieve.

        @@@param defaultValue:mixed
            The value to return if the key is not specified or is invalid.

        @@@return string,list,mixed
            Returns the string value of the attribute, or a colon delimited string if the value
            was a comma-delimited list, if the attribute exists. Otherwise returns the defaultValue.
        """

        raw, keyData = self.get(
            keys=keys, defaultValue=None, overrides=overrides, extract=extract, returnKey=True
        )
        if raw is None:
            if returnKey:
                return defaultValue, None
            return defaultValue

        try:
            if isinstance(raw, list):
                if implode:
                    out = u':'.join(raw)
                else:
                    out = []
                    for item in raw:
                        out.append(item.replace(u' ', u'').lower())
            else:
                out = raw.replace(' ','').lower()
            if returnKey:
                return out, keyData
            return out
        except Exception, err:
            if not allowFailure:
                self.logAttributeError(
                    keyData=keyData,
                    keyGroup=keys,
                    rawValue=raw,
                    code=MarkupAttributeError.BAD_ATTRIBUTE_VALUE
                )
            if returnKey:
                return defaultValue, None
            return defaultValue

#___________________________________________________________________________________________________ getAsColorClass
    def getAsColorClass(self, keys, defaultValue =None, background =False, overrides =None,
                        allowFailure =False, extract =None, returnKey =False):
        raw, keyData = self.get(
            keys=keys, defaultValue=None, overrides=overrides, extract=extract, returnKey=True
        )

        if raw is None:
            if returnKey:
                return defaultValue, keyData
            else:
                return defaultValue

        c = raw.rstrip('+-') if raw else raw
        c = AttributeData._REMOVE_WHITESPACE_RE.sub(u'', c).lower()

        if c in ThemeColorEnum.HIGHLIGHT[1]:
            vclass = 'v-S-hghback' if background else 'v-S-hgh'
        elif c in ThemeColorEnum.LINK[1]:
            vclass = 'v-S-lnkback' if background else 'v-S-lnk'
        elif c in ThemeColorEnum.SOFT[1]:
            vclass = 'v-S-sftback' if background else 'v-S-sft'
        elif c in ThemeColorEnum.BUTTON[1]:
            vclass = 'v-S-fbnback' if background else 'v-S-fbn'
        elif c in ThemeColorEnum.FOCAL[1]:
            vclass = 'v-S-fclback' if background else 'v-S-fcl'
        elif c in ThemeColorEnum.BACK[1]:
            vclass = 'v-S-bck' if background else 'v-S-bckfront'
        elif c in ThemeColorEnum.DODGE[1]:
            vclass = 'v-S-dod' if background else 'v-S-dodfront'
        elif c in ThemeColorEnum.BURN[1]:
            vclass = 'v-S-brn' if background else 'v-S-brnfront'
        elif c in ThemeColorEnum.BORDER[1]:
            vclass = 'v-S-bor' if background else 'v-S-borfront'
        elif c in ThemeColorEnum.BACK_BUTTON[1]:
            vclass = 'v-S-bbn' if background else 'v-S-bbnfront'
        else:
            if not allowFailure:
                self.logAttributeError(
                    keyData=keyData,
                    keyGroup=keys,
                    rawValue=raw,
                    code=MarkupAttributeError.BAD_ATTRIBUTE_VALUE
                )
                return

            vclass = None

        if vclass is not None:
            bendCount = ColorValue.getBendCount(raw)
            if bendCount:
                vclass += ('-d' if bendCount < 0 else '-u') + str(abs(bendCount))

            if returnKey:
                return vclass, keyData
            else:
                return vclass

        if returnKey:
            return defaultValue, keyData
        else:
            return defaultValue

#___________________________________________________________________________________________________ getAsColorValue
    def getAsColorValue(self, keys, defaultValue =None, overrides =None, extract =False,
                        returnKey =False):
        """Retrieves the attribute specified by the keys, or if the attribute was not specified in
        the tag the defaultValue. Prior to returning the value it is instantiated as a ColorValue
        object, which, if fails, returns the default value in its place.

        @@@param keys:string,list
            A single or list of key names for the key to retrieve.

        @@@param defaultValue:mixed
            The value to return if the key is not specified or is invalid. If the defaultValue is
            not a ColorValue, one will be created using the value.

        @@@return string,list,mixed
            Returns the ColorValue for the color specified by the attribute. Otherwise returns
            the defaultValue.
        """

        raw, keyData = self.get(
            keys=keys, defaultValue=None, overrides=overrides, extract=extract, returnKey=True
        )

        if raw:
            error = ErrorPasser('badColor')
            out   = self.convertToColorValue(raw, defaultValue, error)

            if out == error:
                self.logAttributeError(
                    keyData=keyData,
                    keyGroup=keys,
                    rawValue=raw,
                    code=MarkupAttributeError.BAD_ATTRIBUTE_VALUE
                )
            elif out:
                if returnKey:
                    return out, keyData
                return out

        dv = defaultValue if defaultValue is None else ColorValue(defaultValue)
        if returnKey:
            return dv, keyData
        return dv

#___________________________________________________________________________________________________ getAsUnit
    def getAsUnit(self, keys, defaultValue =None, defaultUnit =None, unitType =None,
                  overrides =None, allowFailure =False, extract =False, returnKey =False):
        """Retrieves the attribute specified by the keys, or if the attribute was not specified in
        the tag the defaultValue. Prior to returning the value is parsed for a number and unit,
        returning an instance of UnitAttribute representing the result.

        @@@param keys:string,list
            A single or list of key names for the key to retrieve.

        @@@param defaultValue:mixed
            The value to return if the key is not specified or is invalid. If the defaultValue is
            not a ColorValue, one will be created using the value.

        @@@return string,list,mixed
            Returns the ColorValue for the color specified by the attribute. Otherwise returns
            the defaultValue.
        """

        raw, keyData = self.get(
            keys=keys, defaultValue=None, overrides=overrides, extract=extract, returnKey=True
        )

        if raw is None:
            dv = UnitAttribute(value=defaultValue, unit=defaultUnit, unitType=unitType) \
                 if defaultValue else None
            if returnKey:
                return dv, keyData
            return dv

        try:
            if isinstance(raw, list):
                out = []
                for r in raw:
                    out.append(UnitAttribute.createIfValid(
                        r, defaultUnit=defaultUnit, unitType=unitType
                    ))
            else:
                out = UnitAttribute.createIfValid(raw, defaultUnit=defaultUnit, unitType=unitType)
            if out:
                if returnKey:
                    return out, keyData
                return out
            elif not allowFailure:
                self.logAttributeError(
                    keyData=keyData,
                    keyGroup=keys,
                    rawValue=raw,
                    code=MarkupAttributeError.BAD_ATTRIBUTE_VALUE
                )
        except Exception, err:
            if not allowFailure:
                self.logAttributeError(
                    keyData=keyData,
                    keyGroup=keys,
                    rawValue=raw,
                    code=MarkupAttributeError.BAD_ATTRIBUTE_VALUE
                )

        dv = UnitAttribute(value=defaultValue, unit=defaultUnit, unitType=unitType) \
             if defaultValue else None
        if returnKey:
            return dv, keyData
        return dv

#___________________________________________________________________________________________________ getAsFloat
    def getAsFloat(self, keys, defaultValue =None, overrides =None, allowFailure =False,
                   extract =False, returnKey =False):
        raw, keyData = self.get(
            keys=keys, defaultValue=None, overrides=overrides, extract=extract, returnKey=True
        )

        if raw is None:
            if returnKey:
                return defaultValue, keyData
            return defaultValue

        try:
            if returnKey:
                return float(raw)
            return float(raw)
        except Exception, err:
            if not allowFailure:
                self.logAttributeError(
                    keyData=keyData,
                    keyGroup=keys,
                    rawValue=raw,
                    code=MarkupAttributeError.BAD_ATTRIBUTE_VALUE
                )

            if returnKey:
                return defaultValue, keyData
            return defaultValue

#___________________________________________________________________________________________________ getAsInt
    def getAsInt(self, keys, defaultValue =None, overrides =None, allowFailure =False,
                 extract =False, returnKey =False):
        raw, keyData = self.get(
            keys=keys, defaultValue=None, overrides=overrides, extract=extract, returnKey=True
        )

        if raw is None:
            if returnKey:
                return defaultValue, keyData
            return defaultValue

        try:
            if returnKey:
                return int(raw), keyData
            return int(raw)
        except Exception, err:
            if not allowFailure:
                self.logAttributeError(
                    keyData=keyData,
                    keyGroup=keys,
                    rawValue=raw,
                    code=MarkupAttributeError.BAD_ATTRIBUTE_VALUE
                )

            if returnKey:
                return defaultValue, keyData
            return defaultValue

#___________________________________________________________________________________________________ getAsBool
    def getAsBool(self, keys, defaultValue =None, overrides =None, allowFailure =False,
                  extract =False, genericFalse =False, returnKey =False):
        raw, keyData = self.getAsKeyword(
            keys=keys, defaultValue=None, overrides=overrides, extract=extract, returnKey=True
        )

        if raw is None:
            if returnKey:
                return defaultValue, keyData
            return defaultValue

        out = None
        if raw in AttributeData._TRUE_BOOLEANS:
            out = True
        elif genericFalse:
            out = False

        if out is not None:
            if returnKey:
                return out, keyData
            return out

        if raw in AttributeData._FALSE_BOOLEANS:
            if returnKey:
                return False, keyData
            return False

        if not allowFailure:
            self.logAttributeError(
                keyData=keyData,
                keyGroup=keys,
                rawValue=raw,
                code=MarkupAttributeError.BAD_ATTRIBUTE_VALUE
            )

        if returnKey:
            return defaultValue, keyData
        return defaultValue

#___________________________________________________________________________________________________ getAsURL
    def getAsURL(self, keys, defaultValue =None, overrides =None, allowFailure =False,
                 extract =False, returnKey =False, allowPageID =False):

        raw, keyData = self.get(
            keys=keys, defaultValue=None, overrides=overrides, extract=extract, returnKey=True
        )

        if not raw:
            if returnKey:
                return defaultValue, keyData
            return defaultValue

        url = raw.replace(
            u'%{VIZME}%', URLParameters.getRootMainURL(True)
        ).replace(
            u'%{VIZMEDOCS}%', URLParameters.getRootDocURL(True)
        ).replace(
            u'%{DEV}%', u'dev' if CONFIG.DEV else u''
        )

        if AttributeData._ILLEGAL_ID_CHARS_RE.search(url):
            if returnKey:
                return url, keyData
            return url

        if allowPageID:
            url = self._processor.getPageURL(url)
            if url:
                if returnKey:
                    return url, keyData
                return url

        if not allowFailure:
            if raw.startswith(u'@'):
                self.logAttributeError(
                    keyData=keyData,
                    keyGroup=keys,
                    rawValue=url,
                    code=MarkupAttributeError.BAD_ATTRIBUTE_VALUE
                )

        if returnKey:
            return defaultValue, keyData
        return defaultValue

#___________________________________________________________________________________________________ convertToColorValue
    def convertToColorValue(self, value, defaultValue =None, onFailure =None):
        if isinstance(value, basestring):
            c = AttributeData._REMOVE_WHITESPACE_RE.sub(u'', value.rstrip(u'+-').lower())
        else:
            c = value

        front = self.focalColors
        back  = self.backColors
        out   = None
        if c in ThemeColorEnum.HIGHLIGHT[1]:
            out = front.highlightColor.clone()
        elif c in ThemeColorEnum.LINK[1]:
            out = front.linkColor.clone()
        elif c in ThemeColorEnum.SOFT[1]:
            out = front.softColor.clone()
        elif c in ThemeColorEnum.BUTTON[1]:
            out = front.buttonColor.clone()
        elif c in ThemeColorEnum.FOCAL[1]:
            out = front.baseColor.clone()
        elif c in ThemeColorEnum.BACK[1]:
            out = back.baseColor.clone()
        elif c in ThemeColorEnum.DODGE[1]:
            out = back.dodgeColor.clone()
        elif c in ThemeColorEnum.BURN[1]:
            out = back.burnColor.clone()
        elif c in ThemeColorEnum.BORDER[1]:
            out = back.borderColor.clone()
        elif c in ThemeColorEnum.BACK_BUTTON[1]:
            out = back.buttonColor.clone()
        elif c is not None:
            try:
                out = ColorValue(c)
            except Exception, err:
                if onFailure:
                    return onFailure
                out = None

        if out:
            if isinstance(value, basestring):
                out.bend(value)
            return out

        if isinstance(defaultValue, ColorValue):
            return defaultValue
        return ColorValue(defaultValue)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getInheritableProperty
    def _getInheritableProperty(self, prop, defaultValue =None, allowNone =False):
        Null   = namedtuple('Null', [])
        parent = self._tag.parent
        while parent:
            value  = getattr(parent.attrs, prop, Null())
            parent = parent.parent
            if isinstance(value, Null):
                continue

            if allowNone or not value is None:
                return value

        return defaultValue

#___________________________________________________________________________________________________ _getInheritableAttribute
    def _getInheritableAttribute(self, attr, defaultValue =None, allowNone =False):
        Null   = namedtuple('Null', [])
        parent = self._tag.parent
        while parent:
            value  = parent.attrs.get(attr, Null())
            parent = parent.parent
            if isinstance(value, Null):
                continue

            if not value is None or (value is None and allowNone):
                return value

        return defaultValue

#___________________________________________________________________________________________________ _getGlobalClass
    def _getGlobalClass(self, suffix =''):
        a = [AttributeData.GLOBAL_CLASS_PREFIX, self._tag.tagName]
        if len(suffix) > 0:
            a.append(suffix)

        return '-'.join(a)

#___________________________________________________________________________________________________ _parse
    def _parse(self):
        s = self._source
        if not s.strip():
            return dict()

        #-------------------------------------------------------------------------------------------
        # Analyze the attribute string using a TextAnalyzer
        ta = TextAnalyzer(s, False, AttributeData._PARSE_BLOCKS)
        ta.analyze()

        #-------------------------------------------------------------------------------------------
        # Break analyzed attribute string into attributes
        attrs  = []
        for b in ta.blocks:
            if b.blockType != BlockSyntaxEnum.VIZMEML_ATTR:
                if not AttributeData._PRIMARY_ATTR_QUOTED_RE.search(s[:b.start]):
                    continue

            attrs.append({'data':ta.getBlocksText(b), 'start':b.start, 'end':b.end})

        # If the attribute string doesn't split into multiple attributes assume the entire string
        # is a single attribute.
        if not attrs:
            attrs.append({'data':s, 'start':0, 'end':len(s)})

        res = dict()
        for attr in attrs:
            # Ignore empty/missing strings
            if not isinstance(attr['data'], basestring) or not attr['data'].strip():
                continue

            # Assign the data and remove the whitespace padding from the analyzed result
            araw  = attr['data']
            al    = araw.lstrip()
            start = attr['start'] + (len(araw) - len(al))
            a     = al.rstrip()
            end   = attr['end'] - (len(al) - len(a))

            attr['vstart'] = start
            index  = a.find(u':')

            # DEFAULT: NO COLON
            isDefault = index == -1

            # DEFAULT: COLON IN QUOTES
            if not isDefault:
                i         = a.find('"')
                isDefault = i != -1 and i < index

            # DEFAULT: COLON IN LITERAL
            if not isDefault:
                i         = a.find('\'')
                isDefault = i != -1 and i < index

            # DEFAULT: PART OF URL
            if not isDefault:
                isDefault = a[index+1:index+3] == '//'

            # Default properties are assigned to value
            quotes = ['\'', '"']
            value  = None
            name   = None
            try:
                if isDefault:
                    name  = 'value'
                    value = a[1:-1] if a[0] in quotes and a[-1] in quotes else a
                else:
                    attr['vstart'] += index + 1
                    name    = a[:index].lower()
                    name    = name[0] + name[1:].replace('-', '').replace('_', '')
                    value   = a[index+2:-1] if a[index+1] in quotes and a[-1] in quotes else a[index+1:]
            except Exception, err:
                MarkupTagError(
                    tag=self._tag,
                    code=MarkupTagError.CORRUPT_ATTRS
                ).log()
                self._tag.log.writeError([
                    'Attribute parsing error',
                    'Default: ' + str(isDefault),
                    'Attr: ' + str(a),
                    'Index: ' + str(index),
                    'Attr Data: ' + str(attr)
                ], err)

            if not value:
                continue

            # If the property is a comma-delimited list, convert the string into an array
            if value.find(',') != -1:
                value = AttributeData._COMMA_LIST_CLEANUP.sub(',',value)
                la    = TextAnalyzer(value, False, AttributeData._LIST_BLOCKS,
                                     initialBlock=AttributeData._LIST_BLOCKS[-1])
                la.analyze()
                value = []
                for b in la.blocks:
                    if b.blockType != BlockSyntaxEnum.LIST_ITEM:
                        continue
                    value.append(la.source[b.start:b.end].strip(',"\'').strip())

                if not value:
                    value = la.source
                elif len(value) == 1:
                    value = value[0].strip()

            res[name] = [value, attr]

        return res

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return u'<%s %s>' % (unicode(self.__class__.__name__), unicode(self._props))

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return str(self.__unicode__())

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__unicode__()

