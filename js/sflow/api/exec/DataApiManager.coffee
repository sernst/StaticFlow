# sflow.api.exec.DataApiManager.coffee
# (C)2011-2013
# Scott Ernst

# import sflow.util.exec.ExecutionManager
# require sflow.api.io.APIRequest
# require sflow.util.ArrayUtils
# require sflow.util.ObjectUtils
# require sflow.util.Types

#___________________________________________________________________________________________________ DataApiManager
class DataApiManager extends ExecutionManager
    ### The DataApiManager class is the main executive class for managing the SFLOW API. The actual
        SFLOW API Class, VizmeAPI, is really just a lightwight public wrapper around the
        DataApiManager class. The API Manager class is responsible for initializing the API and
        handling all of the library and render functions within the page.
    ###

#===================================================================================================
#                                                                                       C L A S S

    @ID = 'api'

#___________________________________________________________________________________________________ constructor
    constructor: () ->
        ### Creates an DataApiManager module instance. ###

        super(DataApiManager.ID)

        @_oneShotEvents     = {}
        @_reqQueue          = {}
        @_pageLoading       = true
        @_eventCallbacks    = {}
        @_mousePos          = {x:0, y:0}

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ render
    render: () ->

#===================================================================================================
#                                                                               P R O T E C T E D


