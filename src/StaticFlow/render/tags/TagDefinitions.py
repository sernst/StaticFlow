# TagDefinitions.py
# (C)2012-2013
# Scott Ernst and Eric David Wills

from collections import namedtuple

TagDefinition = namedtuple('TagDefinition', ['name', 'tagClass', 'package', 'isBlock'])

#___________________________________________________________________________________________________ TagDefinitions
class TagDefinitions(object):
    """A class for..."""

#===================================================================================================
#                                                                                     P U B L I C

    BOLD            = TagDefinition('b', 'BoldTag', 'style', True)

    BORDER          = TagDefinition('border', 'BorderTag', 'box', True)

    BOX             = TagDefinition('box', 'BoxTag', 'box', True)

    BUTTON          = TagDefinition('button', 'ButtonTag', 'ui', False)

    CODE            = TagDefinition('code', 'CodeTag', 'terminal', True)

    COFFEECUP       = TagDefinition('coffeecup', 'CoffeecupTag', 'terminal', True)

    COFFEESCRIPT    = TagDefinition('coffeescript', 'CoffeeScriptTag', 'terminal', True)

    COLOR           = TagDefinition('color', 'ColorTag', 'style', True)

    COMMENT         = TagDefinition('comment', 'CommentTag', 'external', False)

    CONTAINER       = TagDefinition('container', 'ContainerTag', 'layout', True)

    CSS             = TagDefinition('css', 'CSSTag', 'terminal', True)

    DART            = TagDefinition('dart', 'DartTag', 'terminal', True)

    DEVBOX          = TagDefinition('devbox', 'DevBoxTag', 'internal', True)

    ELEMENT         = TagDefinition('element', 'ElementTag', 'entities', False)

    FONT            = TagDefinition('font', 'FontTag', 'style', True)

    FOOTER          = TagDefinition('footer', 'FooterTag', 'elements', True)

    GRADIENT        = TagDefinition('gradient', 'GradientBoxTag', 'box', True)

    GRAPH           = TagDefinition('graph', 'GraphTag', 'elements', True)

    GRID            = TagDefinition('grid', 'GridTag', 'layout', True)

    GROUP           = TagDefinition('group', 'GroupTag', 'definitions', False)

    HAML            = TagDefinition('haml', 'HamlTag', 'terminal', True)

    HANGER          = TagDefinition('hanger', 'HangerTag', 'layout', True)

    HEADER          = TagDefinition('header', 'HeaderTag', 'text', True)

    HTML            = TagDefinition('html', 'HTMLTag', 'terminal', True)

    HULU            = TagDefinition('hulu', 'HuluTag', 'external', False)

    ITALICS         = TagDefinition('i', 'ItalicsTag', 'style', True)

    ICON            = TagDefinition('icon', 'IconTag', 'text', False)

    IMAGE           = TagDefinition('image', 'ImageTag', 'image', False)

    IMAGE_URL       = TagDefinition('imageurl', 'ImageUrlTag', 'data', False)

    IMPLANT         = TagDefinition('implant', 'ImplantTag', 'generators', True)

    ITEM            = TagDefinition('item', 'ListItemTag', 'text', True)

    JADE            = TagDefinition('jade', 'JadeTag', 'terminal', True)

    JAVASCRIPT      = TagDefinition('javascript', 'JavaScriptTag', 'terminal', True)

    JUMP            = TagDefinition('jump', 'JumpTag', 'navigation', True)

    LESS            = TagDefinition('less', 'LessTag', 'terminal', True)

    LINE            = TagDefinition('line', 'LineTag', 'layout', False)

    LINK            = TagDefinition('link', 'LinkTag', 'text', True)

    LIST            = TagDefinition('list', 'ListTag', 'text', True)

    MARKDOWN        = TagDefinition('markdown', 'MarkdownTag', 'terminal', True)

    META_DATA       = TagDefinition('metadata', 'MetaDataTag', 'definitions', False)

    MEDIA           = TagDefinition('media', 'AssetTag', 'entities', False)

    NAVBAR          = TagDefinition('navbar', 'NavBarTag', 'elements', True)

    NOTE            = TagDefinition('note', 'NoteTag', 'insert', True)

    PAGE_URL        = TagDefinition('pageurl', 'PageUrlTag', 'data',  False)

    PARAGRAPH       = TagDefinition('p', 'ParagraphTag', 'text', True)

    PATTERN         = TagDefinition('pattern', 'PatternTag', 'generators', True)

    QUOTE           = TagDefinition('quote', 'QuoteTag', 'insert', True)

    RADIO           = TagDefinition('radio', 'RadioArrayTag', 'ui', True)

    RADIO_BUTTON    = TagDefinition('radiobutton', 'RadioButtonTag', 'ui', False)

    RAW             = TagDefinition('raw', 'RawTag', 'terminal', True)

    ROW             = TagDefinition('row', 'RowTag', 'layout', True)

    SASS            = TagDefinition('sass', 'SassTag', 'terminal', True)

    SCSS            = TagDefinition('scss', 'ScssTag', 'terminal', True)

    SIZE            = TagDefinition('size', 'SizeTag', 'style', True)

    SLIDER          = TagDefinition('slider', 'SliderTag', 'ui', False)

    SLIDESHARE      = TagDefinition('slideshare', 'SlideShareTag', 'external', False)

    SOUNDCLOUD      = TagDefinition('soundcloud', 'SoundCloudTag', 'external', False)

    SPACER          = TagDefinition('spacer', 'SpacerTag', 'layout', False)

    SQUEEZE         = TagDefinition('squeeze', 'SqueezeBoxTag', 'box', True)

    STYLUS          = TagDefinition('stylus', 'StylusTag', 'terminal', True)

    SYMBOL          = TagDefinition('symbol', 'SymbolTag', 'text', False)

    SUB             = TagDefinition('sub', 'SubscriptTag', 'text', True)

    SUMMARY         = TagDefinition('summary', 'SummaryTag', 'definitions', True)

    SUPER           = TagDefinition('sup', 'SuperscriptTag', 'text', True)

    THEME           = TagDefinition('theme', 'ThemeTag', 'style', True)

    TITLE           = TagDefinition('title', 'TitleTag', 'definitions', True)

    TWITTER         = TagDefinition('twitter', 'TwitterTag', 'external', False)

    TEXT            = TagDefinition('text', 'TextInputTag', 'ui', False)

    VIMEO           = TagDefinition('vimeo', 'VimeoTag', 'external', False)

    XDATA           = TagDefinition('xdata', 'XDataTag', 'data', True)

    YDATA           = TagDefinition('ydata', 'YDataTag', 'data', True)

    YOUTUBE         = TagDefinition('youtube', 'YouTubeTag', 'external', False)
