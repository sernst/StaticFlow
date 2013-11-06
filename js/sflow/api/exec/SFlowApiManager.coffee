# sflow.api.exec.SFlowApiManager.coffee
# (C)2011-2013
# Scott Ernst

# import sflow.api.exec.DataApiManager

# require sflow.api.data.DataManager
# require sflow.api.display.IconManager
# require sflow.api.display.StyleManager
# require sflow.api.enum.AttrEnum
# require sflow.api.io.APIRequest
# require sflow.api.render.StaticRenderer
# require sflow.util.ArrayUtils
# require sflow.util.ObjectUtils
# require sflow.util.Types
# require sflow.util.color.ColorMixer
# require sflow.util.debug.Logger
# require sflow.util.io.AJAXRequest
# require sflow.util.string.StringUtils
# require sflow.util.time.DataTimer
# require sflow.util.url.URLUtils

#___________________________________________________________________________________________________ SFlowApiManager
class SFlowApiManager extends DataApiManager
    ### The APIManager class is the main executive class for managing the SFLOW API. The actual
        SFLOW API Class, VizmeAPI, is really just a lightwight public wrapper around the APIManager
        class. The API Manager class is responsible for initializing the API and handling all of the
        library and render functions within the page.
    ###

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ constructor
    constructor: () ->
        ### Creates an APIManager module instance. ###
        super()

        @_renderLoopTimer = new DataTimer(200, 1, false, @_handleRenderLoop)
        @_mouseState      = null

        @_scroller   = $('.sf-scrollContainer')
        @styles      = new StyleManager()
        @data        = new DataManager()
        @vmlRender   = new StaticRenderer()
        @displayType = -1

        @_modules           = {}
        @_autoResizers      = []
        @_renderCallbacks   = {}
        @_pageLoading       = true
        @_resizeEnable      = true
        @requestCode        = null
        @args               = PAGE.apiArgs
        @_sessionCB         = null
        @_eventCallbacks    = {}
        @_mousePos          = {x:0, y:0}

        # Enable smart resizing of modules.
        win = $(window)
        win.resize(@_handleResize)

        cb  = @_handleMouseEvent
        doc = $(document)
        doc.mousedown(cb)
        doc.mouseup(cb)
        doc.mouseleave(cb)
        doc.mouseout(cb)

        $('body').mousemove(@_handleUpdateMousePosition)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ mouse
    mouse: () =>
        ### The APIManager stores the mouse position globally for the lifetime of the application
            as a centeral access point for the lastest position information for popup placement. ###
        return @_mousePos

#___________________________________________________________________________________________________ resizeEnable
    resizeEnable: (value) =>
        if Types.isSet(value)
            pre            = @_resizeEnable
            @_resizeEnable = if value then true else false
            if not pre and value
                @resize()

        return @_resizeEnable

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ render
    render: (rootDOM, callback) =>
        # Find any renderers and entities that are not loaded and load them

        @data.render(rootDOM)
        @vmlRender.render(rootDOM)


#___________________________________________________________________________________________________ resize
    resize: (rootDOM, force) =>
        ### Resizes all Vizme elements currently displayed on the page. This happens automatically
            when the window object is resized, but for changes to the page that do not cause a
            resize event this can be triggered manually at any time.
        ###

        if not @_resizeEnable
            return

        # Shrinks the imposed scrolling viewport to the size of the window.
        if @_scroller.length
            win = $(window)
            @_scroller.height(win.height())

        # Resizes fluid boxes that have a maximum allowed width
        dom = if rootDOM then rootDOM else $('body')

        @vmlRender.resize(dom, force)

        # If a rootDOM is specified only resize rendering within that DOM
        if not Types.isNone(rootDOM)
            @_resizeAutoMaxBoxes(dom)

        @_resizeAutoMaxBoxes(dom, true)

        if SFLOW.mod.page
            SFLOW.mod.page.resize()

        for name, module of @_modules
            if Types.isFunction(module.resize)
                module.resize()

        @_resizeAutoMaxBoxes(dom)

        for module in @_autoResizers
            module.resize()

#___________________________________________________________________________________________________ loadModule
    loadModule: (module) =>
        m   = new module()
        mfn = module.ID

        if not m.initialize()
            return null

        if Types.isFunction(m.autoResize) and m.autoResize()
            @_autoResizers.push(m)

        @_modules[m.id()] ?= m
        SFLOW.mod[m.id()] ?= m

        SFLOW.dispatchEvent({id:'API:module:' + m.id(), oneShot:true})

        return m

#___________________________________________________________________________________________________ updateSize
    updateSize: () =>
        if SFLOW.mod.page
            SFLOW.mod.page.updateSize()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _resizeAutoMaxBoxes
    _resizeAutoMaxBoxes: (dom, unlockOnly) =>
        dom.find("[#{AttrEnum.MAX_WIDE}]").each((index, element) ->
            me = $(this)
            v  = me.attr(AttrEnum.MAX_WIDE)
            if v.substr(0, 1) == '~'
                v = Math.round(10*parseInt(v.substr(1))) + 'px'
            else
                try
                    v = Math.round(parseInt(v)) + 'px'
                catch err

            me.css('max-width', v)
        )

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleUpdateMousePosition
    _handleUpdateMousePosition: (event) =>
        @_mousePos.x = event.clientX
        @_mousePos.y = event.clientY

#___________________________________________________________________________________________________ _onDomReady
    _onDomReady: () =>
        @_hidePageLoading()
        SFLOW.render()
        SFLOW.COMPLETE = true
        SFLOW.dispatchEvent({id:'API:complete', oneShot:true})
        return

#___________________________________________________________________________________________________ _handleResize
    _handleResize: (event) =>
        # Refresh the global font scale based on window aspect ratio
        @styles.setGlobalFontScale(null, false)
        @resize()

#___________________________________________________________________________________________________ _handleAutoResize
    _handleAutoResize: (event) =>
        if @_mouseState == 'down'
            return

        for module in @_autoResizers
            module.resize()

#___________________________________________________________________________________________________ _handleRenderLoop
    _handleRenderLoop: (dt) =>
        if @_mouseState != 'down'
            Renderer.renderQueuedItems()

            for module in @_autoResizers
                module.resize()

        dt.restart()

#___________________________________________________________________________________________________ _handleMouseEvent
    _handleMouseEvent: (event) =>
        if event.type == 'mousedown'
            @_renderLoopTimer.stop()
            @_mouseState = 'down'
            return

        if @_renderLoopTimer.data()
            @_renderLoopTimer.restart()

        @_mouseState = null
