# sflow.util.module.Module.coffee
# Vizme, Inc. (C)2011-2013
# Scott Ernst

# require sflow.util.Types

# General Vizme Login (register) module.
class Module

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ constructor
# Creates a new Login module instance.
    constructor: (id) ->
        # Identifier for the module
        @_moduleID    = id
        @_initialized = false

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: id
# Module identifier.
    id: () =>
        return @_moduleID

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ initialize
# Intializes the module.
    initialize: () =>
        @_initialized = true
        return true
