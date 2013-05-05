# DomRenderData.py
# (C)2012-2013
# Scott Ernst

from pyaid.ArgsUtils import ArgsUtils
from pyaid.debug.Logger import Logger

from StaticFlow.render.dom.organizer.AttributeDataOrganizer import AttributeDataOrganizer
from StaticFlow.render.dom.organizer.DomDataOrganizer import DomDataOrganizer
from StaticFlow.render.dom.organizer.SingleAttributeDataOrganizer import SingleAttributeDataOrganizer
from StaticFlow.render.dom.organizer.SingleValuedAttributeDataOrganizer import SingleValuedAttributeDataOrganizer
from StaticFlow.render.dom.style.Classes import Classes
from StaticFlow.render.dom.style.Stylesheet import Stylesheet

#___________________________________________________________________________________________________ DomRenderData
class DomRenderData(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _WRITES = ['id', 'renderID', 'dataID', 'themeID', 'classes', 'styles', 'attrs', 'dataState',
               'data', 'vdata', 'inits', 'events', 'settings', 'icons']

    _LOGGER = Logger('DomRenderData')

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        """Creates a new instance of ClassTemplate."""
        self._content  = ArgsUtils.get('content', '', kwargs)

        SVADO          = SingleValuedAttributeDataOrganizer
        self._id       = self._createOrganizer('id', kwargs, SVADO, name='id')
        self._renderID = self._createOrganizer(['renderID', 'rid'], kwargs, SVADO, name='data-v-rid')
        self._dataID   = self._createOrganizer(['dataID', 'did'], kwargs, SVADO, name='data-v-did')
        self._styleID  = self._createOrganizer(['themeID', 'sid'], kwargs, SVADO, name='data-v-sid')

        ADO            = AttributeDataOrganizer
        self._vdata    = self._createOrganizer('vdata', kwargs, ADO, prefix='data-v-')
        self._data     = self._createOrganizer('data', kwargs, ADO, prefix='data-')
        self._attrs    = self._createOrganizer('attrs', kwargs, ADO, prefix='')

        SADO            = SingleAttributeDataOrganizer
        self._dataState = self._createOrganizer('dataState', kwargs, SADO, name='data-v-data')
        self._inits     = self._createOrganizer('inits', kwargs, SADO, name='data-v-ini')
        self._events    = self._createOrganizer('events', kwargs, SADO, name='data-v-evt')
        self._settings  = self._createOrganizer('settings', kwargs, SADO, name='data-v-sets')
        self._icon      = self._createOrganizer('icons', kwargs, SADO, name='data-v-icon')

        self._styles   = self._createOrganizer('styles', kwargs, Stylesheet)
        self._classes  = self._createOrganizer('classes', kwargs, Classes)

        self._render   = ArgsUtils.get('render', {}, kwargs)
        self._doms     = ArgsUtils.get('doms', {}, kwargs)
        self._writes   = ArgsUtils.get('writes', [], kwargs)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: id
    @property
    def id(self):
        return self._id

#___________________________________________________________________________________________________ GS: renderID
    @property
    def renderID(self):
        return self._renderID

#___________________________________________________________________________________________________ GS: dataID
    @property
    def dataID(self):
        return self._dataID

#___________________________________________________________________________________________________ GS: themeID
    @property
    def themeID(self):
        return self._styleID

#___________________________________________________________________________________________________ GS: content
    @property
    def content(self):
        return self._content
    @content.setter
    def content(self, value):
        self._content = value

#___________________________________________________________________________________________________ GS: render
    @property
    def render(self):
        """Arbitrary render data properties."""
        return self._render

#___________________________________________________________________________________________________ GS: doms
    @property
    def doms(self):
        """Additional rendered doms to include in the template."""
        return self._doms

#___________________________________________________________________________________________________ GS: classes
    @property
    def classes(self):
        return self._classes

#___________________________________________________________________________________________________ GS: vdata
    @property
    def vdata(self):
        return self._vdata

#___________________________________________________________________________________________________ GS: dataState
    @property
    def dataState(self):
        return self._dataState

#___________________________________________________________________________________________________ GS: data
    @property
    def data(self):
        return self._data

#___________________________________________________________________________________________________ GS: events
    @property
    def events(self):
        return self._events

#___________________________________________________________________________________________________ GS: inits
    @property
    def inits(self):
        return self._inits

#___________________________________________________________________________________________________ GS: settings
    @property
    def settings(self):
        return self._settings

#___________________________________________________________________________________________________ GS: icons
    @property
    def icons(self):
        return self._icon

#___________________________________________________________________________________________________ GS: attrs
    @property
    def attrs(self):
        return self._attrs

#___________________________________________________________________________________________________ GS: styles
    @property
    def styles(self):
        return self._styles

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ join
    def join(self, sourceData):
        for w in DomRenderData._WRITES:
            target = getattr(self, w)
            if isinstance(target, DomDataOrganizer):
                target.join(getattr(sourceData, w))

#___________________________________________________________________________________________________ write
    def write(self, *args, **kwargs):
        group  = ArgsUtils.get('group', None, kwargs, args, 0)
        skipID = ArgsUtils.get('skipID', False, kwargs)
        items  = None if len(args) < 2 else args[1:]

        s   = []
        out = None
        if items and len(items):
            for a in items:
                out = a.write(group=group, **kwargs)
                if out and len(out) > 0:
                    s.append(out)
        else:
            writes = self._writes + DomRenderData._WRITES
            for w in writes:
                if skipID and w == 'id':
                    continue

                try:
                    out = getattr(self, w).write(group=group, **kwargs)
                    if out and len(out) > 0:
                        s.append(out)
                except Exception, err:
                    DomRenderData._LOGGER.writeError(['Organizer write failure',
                                                      'organizer: ' + str(out),
                                                      'renderData: ' + str(self)], err)
                    pass

        return u' '.join(s)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _createOrganizer
    def _createOrganizer(self, propertyName, kwargData, OrganizerClass, **kwargs):
        v = ArgsUtils.get(propertyName, None, kwargData)
        if isinstance(v, DomDataOrganizer):
            return v

        if v:
            return OrganizerClass(root=v, **kwargs)
        else:
            return OrganizerClass(root=v, **kwargs)


