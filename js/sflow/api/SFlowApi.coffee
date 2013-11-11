# sflow.api.SFlowApi.coffee
# (C)2011-2013
# Scott Ernst

#___________________________________________________________________________________________________ SFlowApi
class SFlowApi
    ### Globally assigned (window.SFLOW) API class. Represents the complete public face of for the
        Static Flow API.
    ###

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ constructor
    constructor: () ->
        ### Creates the instance of the SFlowApi API class. ###

        # Store the source SFLOW object until preInit to prevent race conditions from asynchronous
        # actions.
        sf = SFLOW
        @_sf = sf

        # The actual API management class instance controlling the SFLOW object.
        @addEventListener    = sf.addEventListener
        @removeEventListener = sf.removeEventListener
        @dispatchEvent       = sf.dispatchEvent
        @_events             = sf._events
        @_eventCBs           = sf._eventCBs

        # The following are state variables that specify the current load/readiness state of the
        # SFLOW API.
        @CREATED = true
        @INIT    = false
        @READY   = false
        @SCRIPTS = false

        # Loaded/Initialized modules
        @mod = sf.mod

        # Class registry
        @r = sf.r

        window.SFLOW = this
        return

#___________________________________________________________________________________________________ loadComplete
    loadComplete: () ->
        sf = SFLOW

        # Hide page loading and show main content
        $('#mainContainer').show()
        $('#sf_footer').show()
        $('#loadBox').remove()

        sf.SCRIPTS = true
        sf.dispatchEvent({id:'SCRIPT:complete', oneShot:true})

        if PAGE.ASYNC.length
            loadItems(PAGE.ASYNC)

        if PAGE.HTML
            sf.addEventListener('DOM:dynamic', (event) ->
                sf.populateDom(event.data)
            )
        sf.dispatchEvent({id:'DOM:complete', oneShot:true})

        # Intialize the Zurb Foundation framework
        $(document).foundation()

        $(window).resize(() ->
            SFLOW.dispatchEvent({id:'DOM:resize', data:$('body')})
            SFLOW.resize()
        )

        sf.dispatchEvent({id:'LOAD:complete', oneShot:true})
        sf.refresh()

        if location.hash.length > 1
            sf.dispatchEvent({id:'PAGE:hashChange', data:location.hash})
        return

#___________________________________________________________________________________________________ resize
    resize: (dom) ->
        dom = if dom then $(dom) else $('body')
        SFLOW.dispatchEvent({id:'DOM:resize', data:dom})

        $('.sfml-aspect').each((index, element) ->
            e = $(element)
            aspect = e.data('aspect')
            e.height(Math.floor(e.width() / aspect))
        )

#___________________________________________________________________________________________________ refresh
    refresh: (dom) ->
        dom = if dom then $(dom) else $('body')

        # Force Zurb foundation elements to resize in the new DOM once initialized
        dom.find('.columns').resize()

        # Lazy load images
        dom.find('img[data-src!=""]').each((index, element) ->
            e   = $(element)
            src = e.attr('data-src')
            e.attr('data-src', null)

            # Skip empty data-src values
            if not src or src.length == 0
                return

            # Add CDN prefix to relative URLs
            if src.substr(0, 2) != '//' and src.substr(0, 4) != 'http'
                src = PAGE.CDN_URL + src

            e.attr('src', src)
        )

        # Update the sticky footer
        footerHeight = $('#sf_footer').height()
        $('#sf_footer_push').height(footerHeight)
        $('#sf_wrapper').css('margin-bottom', footerHeight + 'px')

        SFLOW.resize(dom)
        return
