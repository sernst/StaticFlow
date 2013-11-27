# loader.coffee
# (C)2013
# Scott Ernst

#---------------------------------------------------------------------------------------------------
# FUNCTION.BIND DEFINITION
#       This creates a bind method on functions if one does not exist, which is needed to bind
#       callback functions to a closure (scope) during the beach head loading process. This bind
#       definition was influenced heavily by the one available on the Mozilla developer network
#       function.bind documentation site.
if not Function.prototype.bind
    Function.prototype.bind = (oThis) ->
        aArgs   = Array.prototype.slice.call(arguments, 1)
        fToBind = this
        fNOP    = () ->
        fBound  = () ->
            return fToBind.apply(
                if (this instanceof fNOP && oThis) then this else oThis,
                aArgs.concat(Array.prototype.slice.call(arguments))
            )

        fNOP.prototype = this.prototype
        fBound.prototype = new fNOP()
        return fBound

#---------------------------------------------------------------------------------------------------
# STATIC FLOW BEACH HEAD
#       Creates temporary global SFlow access point.
sflow = {
    mod:{},
    r:{},
    _events:{},
    _eventCBs:{},
    CREATED:false
}
window.SFLOW = sflow

#___________________________________________________________________________________________________ addEventListener
sflow.addEventListener = (id, cb, d) ->
    ### Adds an event listener of the specified ID, which will execute the specified callback.

        @@@param id:string
            The event identifier on which to register the event callback.

        @@@param callback:function
            The callback function executed whenever the event is fired.

        @@@param data:mixed
            Any data to be passed to the callback function when called by the event.
    ###
    id = id.toLowerCase()
    sf = window.SFLOW

    if sf._events[id]
        cb.apply(window, [sf._events[id], d])
        return

    e      = sf._eventCBs
    e[id] ?= []

    # Do not add callbacks more than once
    for x in e[id]
        if x.cb == cb
            return

    e[id].push({cb:cb, data:d})
    return

#___________________________________________________________________________________________________ removeEventListener
sflow.removeEventListener = (id, cb) ->
    ### Removes an event listener of the specified ID.

        @@@param id:string
            The event identifier associated with the listener.

        @@@param callback:function
            The function to remove for the given id.
    ###
    id = id.toLowerCase()
    e = window.SFLOW._eventCBs
    if not e[id]
        return

    i = 0
    for x in e[id]
        if x.cb == cb
            e[id].splice(i, 1)
            return
        i++

    return

#___________________________________________________________________________________________________ dispatchEvent
sflow.dispatchEvent = (e) ->
    ### Dispatches an event. The event can either be a string object or an event object with an id
        atttribute.
    ###
    sf = window.SFLOW

    try
        id = e.id.toLowerCase()
    catch err
        id = e.toLowerCase()
        e  = {id:e}

    if e.oneShot
        sf._events[id] = e

    cb = sf._eventCBs
    if not cb[id]
        return false

    for x in cb[id]
        x.cb.apply(window, [e, x.data])
    return true

#___________________________________________________________________________________________________ populateDom
sflow.populateDom = (dom) ->
    $(dom).each((i, e) ->
        e  = $(e)
        id = e.attr('id')
        $('#' + id).replaceWith(e)
    )
    SFLOW.refresh()

#___________________________________________________________________________________________________ window.onhashchange
window.onhashchange = () ->
    SFLOW.dispatchEvent({id:'PAGE:hashChange', data:location.hash})

####################################################################################################
####################################################################################################

#___________________________________________________________________________________________________ window.onload
window.onload = () ->
    ### The beachhead loading script that asynchronously loads the javascript libraries needed to
        render the page.
    ###

    doc      = document
    head     = doc.getElementsByTagName('head')[0]
    progress = [1, 1]
    scripts  = PAGE.SCRIPTS
    delta    = 89.0/scripts.length
    css      = PAGE.CSS
    dyn      = PAGE.HTML
    count    = scripts.length

    #-----------------------------------------------------------------------------------------------
    # COMPLETE
    #   Executed when all script loading completed. Triggers the loading of the independent, i.e.
    #   truly asynchronous scripts, if any exist.
    complete = () ->
        new SFLOW.class()
        SFLOW.loadComplete()
        return

    #-----------------------------------------------------------------------------------------------
    # CALLBACK
    #   Executed when a script file has been loaded.
    callback = () ->
        SFLOW.dispatchEvent({id:'SCRIPT:loaded:' + this.i[0], data:this, oneShot:true})
        if not this.t
            return

        progress[0] += delta
        progress[1] = Math.max(progress[0], progress[1])

        if (this.t)
            count--
            if count <= 0
                complete()

        return

    #-----------------------------------------------------------------------------------------------
    # LOAD
    #   Loads script files asynchronously and on complete executes a callback. This function
    #   handles the actual load process, while load is used as a wrapper for standard includes.
    #   The independent (truly asynchronous) scripts are loaded using loadRow directly, which
    #   doesn't affect the counting toward completion of the script load process.
    loadItems = (items, sync) ->
        for item in items
            script         = doc.createElement('script')
            script.charset = 'utf-8'
            script.type    = 'text/javascript'
            script.id      = item[0]
            script.src     = item[1]
            script.onload = callback.bind({s:script, i:item, t:sync})
            head.appendChild(script)
        return

    #-----------------------------------------------------------------------------------------------
    # DISPLAY
    #   Animated display of the loading icon.
    lt = setInterval(() ->
        t = document.getElementById('loadProgress')
        if (!t)
            clearInterval(lt)
            lt = null
            return

        progress[1]++
        t.style.width = Math.min(100, progress[1]) + '%'
        return
    , 125)

    #-----------------------------------------------------------------------------------------------
    # CSS
    #   Begin loading of all of the linked CSS style sheets.
    if css and css.length > 0
        for cssItem in css
            link      = doc.createElement('link')
            link.rel  = 'stylesheet'
            link.type = 'text/css'
            link.id   = cssItem[0]
            link.href = cssItem[1]
            head.appendChild(link)

    #-----------------------------------------------------------------------------------------------
    # POST URL
    #   Dynamic AJAX post function.
    pUrl = (u, e, p, os) ->
        r = new XMLHttpRequest()
        r.onreadystatechange = () ->
            if r.readyState == 4 and r.status == 200
                SFLOW.dispatchEvent({id:e, data:r.responseText, oneShot:os})
            return
        pm = if p then 'POST' else 'GET'

        r.open(pm, u, true)
        if p
            r.setRequestHeader("Content-type","application/x-www-form-urlencoded; charset=UTF-8")
            r.send(p)
        else
            r.send()
        return
    SFLOW.get = pUrl

    # Load dynamic data if necessary
    if dyn
        pUrl(dyn, 'DOM:dynamic', null, true)

    # Begin the load process
    if scripts.length == 0
        complete()
    else
        loadItems(scripts, true)

    return

