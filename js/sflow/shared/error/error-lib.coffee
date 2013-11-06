# sflow.shared.error.error-lib.coffee
# Vizme, Inc. (C)2012
# Scott Ernst

# targets sflow.api.VizmeAPI

# require sflow.shared.error.Error
# require sflow.util.exec.PageManager
# require sflow.util.display.Help
# require sflow.util.display.Response

#___________________________________________________________________________________________________ init
libraryInit = () ->
    pm = new PageManager('#container', 320, 3000, 0)
    pm.loadModule(Error,    false)
    pm.loadModule(Response, false)
    pm.loadModule(Help,     false)
    pm.initializeComplete()

    SFLOW.mod.error.show()
    pm.initializeComplete()
    $('#container').show()
    SFLOW.resize()
