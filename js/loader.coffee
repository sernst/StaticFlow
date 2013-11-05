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
    _events:{},
    _eventCBs:{},
    SCRIPTS:false
}
window.SFLOW = sflow

#___________________________________________________________________________________________________ resize
sflow.resize = (dom) ->
    dom = if dom then $(dom) else $('body')
    window.SFLOW.dispatchEvent({id:'DOM:resize', data:dom})

#___________________________________________________________________________________________________ refresh
sflow.refresh = (dom) ->
    dom = if dom then $(dom) else $('body')

    # Force Zurb foundation elements to resize in the new DOM once initialized
    dom.find('.columns').resize()

    # Lazy load images
    dom.find('img[data-src!=""]').each((index, element) ->
        e   = $(element)
        src = e.attr('data-src')
        if src and src.length > 0 and src.substr(1, 1) != '/'
            src = PAGE.CDN_URL + src
        e.attr('data-src', null)
        e.attr('src', src)
    )

    window.SFLOW.resize(dom)
    return

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
    v = window.SFLOW

    if v._events[id]
        cb(v._events[id], d)
        return

    e      = v._eventCBs
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
    v = window.SFLOW

    try
        id = e.id
    catch err
        id = e
        e  = {id:e}

    if e.oneShot
        v._events[id] = e

    cb = v._eventCBs
    if not cb[id]
        return false

    for x in cb[id]
        x.cb(e, x.data)
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
        # Intialize the Zurb Foundation framework
        $('#mainContainer').show()
        $('#loadBox').remove()

        SFLOW.SCRIPTS = true
        SFLOW.dispatchEvent({id:'SCRIPT:complete', oneShot:true})

        if PAGE.ASYNC.length
            loadItems(PAGE.ASYNC)

        if dyn
            SFLOW.addEventListener('DOM:dynamic', (event) ->
                SFLOW.populateDom(event.data)
            )
        SFLOW.dispatchEvent({id:'DOM:complete', oneShot:true})
        $(document).foundation()

        $(window).resize(() ->
            SFLOW.dispatchEvent({id:'DOM:resize', data:$('body')})
        )

        SFLOW.dispatchEvent({id:'LOAD:complete', oneShot:true})
        SFLOW.refresh()

        if location.hash.length > 1
            SFLOW.dispatchEvent({id:'PAGE:hashChange', data:location.hash})

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

