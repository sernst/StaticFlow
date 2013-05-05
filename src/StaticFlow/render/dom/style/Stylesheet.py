# Stylesheet.py
# (C)2012-2013
# Scott Ernst

from StaticFlow.render.dom.organizer.KeyDataOrganizer import KeyDataOrganizer

#___________________________________________________________________________________________________ Stylesheet
class Stylesheet(KeyDataOrganizer):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, root, **kwargs):
        """Creates a new instance of Stylesheet."""
        KeyDataOrganizer.__init__(self, root, **kwargs)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ add
    def add(self, *args, **kwargs):
        """Adds a style or multiple styles to the Stylesheet.

        @@@param key:string
            If adding one style, the first argument is the name of the style to add. If adding
            multiple styles this argument is omitted.

        @@@param value:mixed,dict
            When adding a single style, this value can be any basic type that can be converted
            to a string. When adding multiple values this is the first argument and should be a
            dictionary of style name/value pairs.

        @@@param group:string
            Defaults to None, in which case the style(s) are added to the root group. Otherwise,
            specified the style group in which to add the style.
        """

        KeyDataOrganizer.add(self, *args, **kwargs)

#___________________________________________________________________________________________________ getTheme
    def getTheme(self, key, group =None):
        """Doc..."""
        return self.getKey(key, group)

#___________________________________________________________________________________________________ getStyles
    def getStyles(self, group =None):
        """Doc..."""
        return self.getKeyGroup(group)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _writeImpl
    def _writeImpl(self, value, params):
        res = []
        for n,v in value.iteritems():
            res.append(n + u':' + unicode(v))
        res = u';'.join(res)

        if params.get('wrap', True):
            return u'style=\'%s\'' % res
        else:
            return res
