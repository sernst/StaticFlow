# libraryLoader.coffee
# Vizme, Inc. (C)2012
# Scott Ernst

##MODULES##
SFLOW.exec.libraryReady('##LIBNAME##')
if typeof(libraryInit) == 'function'
    SFLOW.addEventListener('API:complete', libraryInit)
