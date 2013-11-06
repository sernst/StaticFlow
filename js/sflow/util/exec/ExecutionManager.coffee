# sflow.util.exec.ExecutionManager.coffee
# (C)2011-2013
# Scott Ernst

# import sflow.util.module.Module
# require sflow.util.Types

# ExecutionManager module that manages other modules.
class ExecutionManager extends Module

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ constructor
# Initializes the ExecutionManager module.
    constructor: (id) ->
        super(id)

        # Creates the global module access point if it doesn't already exist.
        SFLOW.mod ?= {}

        SFLOW.mod[id] = this

        # Applies this as the executive module.
        if not SFLOW.exec
            SFLOW.exec = this

