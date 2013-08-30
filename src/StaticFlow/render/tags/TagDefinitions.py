# TagDefinitions.py
# (C)2012-2013
# Scott Ernst and Eric David Wills

from StaticFlow.render.tags.box.BoxTag import BoxTag
from StaticFlow.render.tags.box.BorderTag import BorderTag
from StaticFlow.render.tags.box.SqueezeBoxTag import SqueezeBoxTag
from StaticFlow.render.tags.definitions.GroupTag import GroupTag
from StaticFlow.render.tags.definitions.MetaDataTag import MetaDataTag
from StaticFlow.render.tags.definitions.SummaryTag import SummaryTag
from StaticFlow.render.tags.definitions.TitleTag import TitleTag
from StaticFlow.render.tags.external.HuluTag import HuluTag
from StaticFlow.render.tags.external.SlideShareTag import SlideShareTag
from StaticFlow.render.tags.external.SoundCloudTag import SoundCloudTag
from StaticFlow.render.tags.external.TwitterTag import TwitterTag
from StaticFlow.render.tags.external.VimeoTag import VimeoTag
from StaticFlow.render.tags.external.YouTubeTag import YouTubeTag
from StaticFlow.render.tags.image.ImageTag import ImageTag
from StaticFlow.render.tags.insert.NotesTag import NotesTag
from StaticFlow.render.tags.insert.QuoteTag import QuoteTag
from StaticFlow.render.tags.layout.ContainerTag import ContainerTag
from StaticFlow.render.tags.layout.GridTag import GridTag
from StaticFlow.render.tags.layout.HangerTag import HangerTag
from StaticFlow.render.tags.layout.LineTag import LineTag
from StaticFlow.render.tags.layout.RowTag import RowTag
from StaticFlow.render.tags.layout.SpacerTag import SpacerTag
from StaticFlow.render.tags.navigation.JumpTag import JumpTag
from StaticFlow.render.tags.style.BoldTag import BoldTag
from StaticFlow.render.tags.style.ColorTag import ColorTag
from StaticFlow.render.tags.style.FontTag import FontTag
from StaticFlow.render.tags.style.ItalicsTag import ItalicsTag
from StaticFlow.render.tags.style.SizeTag import SizeTag
from StaticFlow.render.tags.terminal.MarkdownTag import MarkdownTag
from StaticFlow.render.tags.terminal.RawTag import RawTag
from StaticFlow.render.tags.text.HeaderTag import HeaderTag
from StaticFlow.render.tags.text.LinkTag import LinkTag
from StaticFlow.render.tags.text.ListItemTag import ListItemTag
from StaticFlow.render.tags.text.ListTag import ListTag
from StaticFlow.render.tags.text.ParagraphTag import ParagraphTag
from StaticFlow.render.tags.text.SubscriptTag import SubscriptTag
from StaticFlow.render.tags.text.SuperscriptTag import SuperscriptTag
from StaticFlow.render.tags.text.SymbolTag import SymbolTag

#___________________________________________________________________________________________________ TagDefinitions
class TagDefinitions(object):
    """A class for..."""

#===================================================================================================
#                                                                                     P U B L I C

    BOLD            = BoldTag

    BORDER          = BorderTag

    BOX             = BoxTag

    COLOR           = ColorTag

    CONTAINER       = ContainerTag

    FONT            = FontTag

    GRID            = GridTag

    GROUP           = GroupTag

    HANGER          = HangerTag

    HEADER          = HeaderTag

    HULU            = HuluTag

    ITALICS         = ItalicsTag

    IMAGE           = ImageTag

    ITEM            = ListItemTag

    JUMP            = JumpTag

    LINE            = LineTag

    LINK            = LinkTag

    LIST            = ListTag

    MARKDOWN        = MarkdownTag

    META_DATA       = MetaDataTag

    NOTE            = NotesTag

    PARAGRAPH       = ParagraphTag

    QUOTE           = QuoteTag

    RAW             = RawTag

    ROW             = RowTag

    SIZE            = SizeTag

    SLIDESHARE      = SlideShareTag

    SOUNDCLOUD      = SoundCloudTag

    SPACER          = SpacerTag

    SQUEEZE         = SqueezeBoxTag

    SYMBOL          = SymbolTag

    SUB             = SubscriptTag

    SUMMARY         = SummaryTag

    SUPER           = SuperscriptTag

    TITLE           = TitleTag

    TWITTER         = TwitterTag

    VIMEO           = VimeoTag

    YOUTUBE         = YouTubeTag
