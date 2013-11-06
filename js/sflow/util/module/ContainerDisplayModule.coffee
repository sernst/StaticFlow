# sflow.util.module.ContainerDisplayModule.coffee
# Vizme, Inc. (C)2011
# Scott Ernst

# import sflow.util.module.DisplayModule
# require sflow.util.Types
# require sflow.util.dom.DOMUtils

# General Display module
class ContainerDisplayModule extends DisplayModule

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ constructor
# Creates a new ContainerDisplayModule module instance.
    constructor: (id, container) ->
        super(id, container)

#===================================================================================================
#                                                                                   G E T / S E T

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ resize
# Resizes the module.
    resize: () =>
        box = @me().find('.v-APIResponseBox')
        box.css('width', 'auto')
        box.each((index, element) ->
            me = $(this)
            if me.width() > 640
                me.width(640)
        )

        super()
