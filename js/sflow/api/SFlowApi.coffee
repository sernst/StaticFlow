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

        @_loopInterval = null

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

        # Initialize the Zurb Foundation framework
        $(document).foundation()

        $(window).resize(() ->
            SFLOW.dispatchEvent({id:'DOM:resize', data:$('body')})
            SFLOW.resize()
        )

        sf.dispatchEvent({id:'LOAD:complete', oneShot:true})
        sf.refresh()

        if location.hash.length > 1
            sf.dispatchEvent({id:'PAGE:hashChange', data:location.hash})

        sf.dispatchEvent({id:'API:ready', oneShot:true})

        sf._loopInterval = setInterval(sf._handleRenderLoop, 100)
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

        #-------------------------------------------------------------------------------------------
        # LAZY LOAD ELEMENTS
        #       Elements like images and iframes with lazy load source attributes should be loaded
        #       during refresh to continue populating page
        lazyFunc = @_lazyReplacement
        dom.find('img[data-src!=""]').each((index, element) ->
            lazyFunc(element, 'data-src', 'src')
        )

        dom.find('iframe[data-src!=""]').each((index, element) ->
            lazyFunc(element, 'data-src', 'src')
        )

        @_loadDiscus()

        # Update the sticky footer
        #footerHeight = $('#sf_footer').height()
        #$('#sf_footer_push').height(footerHeight)
        #$('#sf_wrapper').css('margin-bottom', footerHeight + 'px')

        SFLOW.resize(dom)
        return

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _lazyReplacement
    _lazyReplacement: (element, sourceAttr, destAttr) ->
        e = $(element)
        src = e.attr(sourceAttr)
        e.attr(sourceAttr, null)

        # Skip empty data-src values
        if not src or src.length == 0
            return

        # Add CDN prefix to relative URLs
        if src.substr(0, 2) != '//' and src.substr(0, 4) != 'http'
            src = PAGE.CDN_URL + src

        e.attr(destAttr, src)
        return

#___________________________________________________________________________________________________ _loadDiscus
    _loadDiscus: () ->
        e = $("#disqus_thread")
        if e.attr('data-rendered')
            return

        prefix = 'data-discus-'
        e.attr('data-rendered', 1)

        sn = e.attr(prefix + 'shortname')
        url = e.attr(prefix + 'url')
        id = e.attr(prefix + 'id')
        local = e.attr(prefix + 'local')

        script = "<script type=\"text/javascript\">" \
            + "\nvar disqus_shortname = \"#{sn}\";" \
            + "\nvar disqus_url = \"#{url}\";" \
            + "\nvar disqus_identifier = \"#{id}\";" \
            + "\nvar disqus_developer = #{local};" \
            + "\n(function() {" \
            + "\nvar dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;" \
            + "\ndsq.src = '//' + \"#{sn}\" + '.disqus.com/embed.js';" \
            + "\n(document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq); })();" \
            + "\n</script>"

        e.append(script)
        return

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleRenderLoop
    _handleRenderLoop: () ->
        SFLOW.dispatchEvent('DOM:render')
