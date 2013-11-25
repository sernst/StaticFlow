# Page.py
# (C)2013
# Scott Ernst

import os
import datetime

from pyaid.ArgsUtils import ArgsUtils
from pyaid.config.ConfigsDict import ConfigsDict
from pyaid.file.FileUtils import FileUtils
from pyaid.json.JSON import JSON
from pyaid.time.TimeUtils import TimeUtils
from pyaid.web.mako.MakoRenderer import MakoRenderer


from StaticFlow.components.ConfigsDataComponent import ConfigsDataComponent
from StaticFlow.StaticFlowEnvironment import StaticFlowEnvironment
from StaticFlow.components.LocalImage import LocalImage
from StaticFlow.render.MarkupProcessor import MarkupProcessor
from StaticFlow.process.AuthorData import AuthorData
from StaticFlow.process.PageProcessUtils import PageProcessUtils
from StaticFlow.process.SiteProcessUtils import SiteProcessUtils
from StaticFlow.process.rss.RssFileGenerator import RssFileGenerator

#___________________________________________________________________________________________________ Page
class Page(ConfigsDataComponent):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, site, definitionPath, sourcePath =None, parentPage =None):
        """Creates a new instance of Page"""
        super(Page, self).__init__()

        self.markupProcessor = None
        self.site            = site

        self._childPages        = []
        self._referencedPages   = []
        self._parentPage        = parentPage
        self._rssGenerator      = None
        self._rssOwners         = []

        self._definitionPath    = FileUtils.cleanupPath(definitionPath, isFile=True)
        self._sourcePath        = sourcePath
        self._inheritData       = []
        self._date              = None
        self._isCompiled        = False
        self._isProcessed       = False
        self._thumbnail         = None
        self._pageVars          = None
        self._authorData        = None

        self._loadDefinitions()

        # If an RSS definition exists create an RSS generator
        if self.get('RSS') is not None:
            self._rssGenerator = RssFileGenerator(self)

        self._date = FileUtils.getModifiedDatetime(self.sourcePath)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: thumbnail
    @property
    def thumbnail(self):
        """ LocalImage instance for the page thumbnail if one was specified. """
        return self._thumbnail

#___________________________________________________________________________________________________ GS: referencedPages
    @property
    def referencedPages(self):
        return self._referencedPages

#___________________________________________________________________________________________________ GS: rssLinkSource
    @property
    def rssLinkSource(self):
        """ The RSS generator that should be used to create the HTML link in the Page if such a
            generator exists for this page, otherwise None """
        if self._rssGenerator:
            return self._rssGenerator
        if self._rssOwners:
            return self._rssOwners[0]
        return None

#___________________________________________________________________________________________________ GS: renderPass
    @property
    def renderPass(self):
        """ The render pass integer for this page. The smaller the number, the earlier the page
            will be rendered during compilation and processing phases. The default value is 0 """
        return self.get('RENDER_PASS', 0)

#___________________________________________________________________________________________________ GS: author
    @property
    def author(self):
        """ The AuthorData for the Page if one exists """
        if not self._authorData:
            self._authorData = AuthorData(self)
        return self._authorData

#___________________________________________________________________________________________________ GS: title
    @property
    def title(self):
        """ The title for the Page """
        return self.get('title')

#___________________________________________________________________________________________________ GS: description
    @property
    def description(self):
        """ The description for the page """
        s = self.get('summary')
        if s:
            return s
        s = self.get('description')
        if s:
            return s
        return self.site.get('description')

#___________________________________________________________________________________________________ GS: footerDom
    @property
    def footerDom(self):
        """ The HTML for the footer of the Page, which is added to the page outside of the normal
            contents of the body to prevent issues with sticky footers It is generated by using
            the #footer SFML tag """
        if self.markupProcessor is None:
            return u''
        return self.markupProcessor.footerDom

#___________________________________________________________________________________________________ GS: cssTags
    @property
    def cssTags(self):
        if self.markupProcessor is None:
            return u''
        css = self.markupProcessor.cssStyles
        return css if css is not None else u''

#___________________________________________________________________________________________________ GS: pageVars
    @property
    def pageVars(self):
        """ A dictionary of variables that will be written to the html of the generated HTML for
            access by Javascript within the page during execution """
        return self._pageVars

#___________________________________________________________________________________________________ GS: rssGenerator
    @property
    def rssGenerator(self):
        """ The RSS generator owned by this page, if one exists, as defined by the RSS section of
            the Page definition file. Unlike RSS owners, that own pages, this is the RSS generator
            owned by this page. For example, a blog RSS feed is owned by the blog's home page """
        return self._rssGenerator

#___________________________________________________________________________________________________ GS: parentPage
    @property
    def parentPage(self):
        return self._parentPage

#___________________________________________________________________________________________________ GS: childPages
    @property
    def childPages(self):
        return self._childPages

#___________________________________________________________________________________________________ GS: filename
    @property
    def filename(self):
        filename = self.get('FILE_NAME')
        if filename is None:
            if self.sourcePath:
                filename = os.path.basename(self.sourcePath).rsplit('.', 1)[0]
            else:
                return None

        elif filename.endswith('.html'):
            filename = filename[:-5]

        if filename == '*':
            return None
        return filename

#___________________________________________________________________________________________________ GS: definitionPath
    @property
    def definitionPath(self):
        """ The path to the definition file that defines this Page """
        return self._definitionPath

#___________________________________________________________________________________________________ GS: sourcePath
    @property
    def sourcePath(self):
        """ The path to the content source file, if one exists, for this Page. It can be either an
            HTML or an SFML file """

        if self._sourcePath:
            return self._sourcePath

        fileNoExtension = self._definitionPath[:-3]
        if os.path.exists(fileNoExtension + 'sfml'):
            return fileNoExtension + 'sfml'
        if os.path.exists(fileNoExtension + 'html'):
            return fileNoExtension + 'html'
        return None

#___________________________________________________________________________________________________ GS: sourceFolder
    @property
    def sourceFolder(self):
        if self.sourcePath:
            return SiteProcessUtils.getFolderParts(
                self.sourcePath, self.site.sourceWebRootPath)
        return None

#___________________________________________________________________________________________________ GS: date
    @property
    def date(self):
        return self._date if self._date else datetime.datetime.now()

#___________________________________________________________________________________________________ GS: targetPath
    @property
    def targetPath(self):
        if not self.sourcePath:
            return None

        return FileUtils.createPath(
            self.site.targetWebRootPath,
            self.sourceFolder,
            self.filename + '.html',
            isFile=True)

#___________________________________________________________________________________________________ GS: targetUrl
    @property
    def targetUrl(self):
        path = self.targetPath
        if not path:
            return None
        return SiteProcessUtils.getUrlFromPath(self.site, self.get('DOMAIN'), path)

#___________________________________________________________________________________________________ GS: targetUrlLink
    @property
    def targetUrlLink(self):
        path = self.targetPath
        if not path:
            return None
        return u'/' + path[len(self.site.targetWebRootPath):].replace(u'\\', u'/')

#___________________________________________________________________________________________________ GS: dataSources
    @property
    def dataSources(self):
        return super(Page, self).dataSources + self._inheritData + self.site.dataSources

#___________________________________________________________________________________________________ GS: isCompiled
    @property
    def isCompiled(self):
        """ Whether or not this page has been compiled """
        return self._isCompiled

#___________________________________________________________________________________________________ GS: isProcessed
    @property
    def isProcessed(self):
        """ Whether or not this page has been processed """
        return self._isProcessed

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ addRssOwner
    def addRssOwner(self, rssGenerator):
        """ Adds the specified RSS generator to the list of RSS generators that has ownership of
            this page """

        if rssGenerator not in self._rssOwners:
            self._rssOwners.append(rssGenerator)
            return True
        return False

#___________________________________________________________________________________________________ compile
    def compile(self):
        """ The compile process links other pages to this page through the references, compiles any
            children pages, and then compiles the markup for this page if necessary. Once that is
            complete the settings affected by the compilation process, e.g. title, description,
            thumbnail image, etc. are updated in the page in preparation for processing. """

        if self.isCompiled:
            return True
        self._isCompiled = True

        #--- LINK REFERENCES
        #       Iterate through page references and add them to the list
        references = self.get('REFERENCES', [])
        for ref in references:
            refPath = FileUtils.createPath(self.site.sourceWebRootPath, ref.lstrip(u'/'))
            if not os.path.exists(refPath):
                self.site.writeLogError(u'Invalid References Path "%s"' % refPath)
                continue
            if os.path.isfile(refPath):
                pages = [self.site.pages.getPageBySourcePath(refPath)]
            else:
                pages = self.site.pages.getPagesInFolder(ref)
            if not pages:
                continue

            for page in pages:
                if page and page not in self._referencedPages:
                    self._referencedPages.append(page)

        self._referencedPages = PageProcessUtils.sortPagesByDate(
            pages=self._referencedPages,
            reverse=True)

        #--- CHILDREN
        #       Compile pages marked as children before compiling current page
        for child in self._childPages:
            child.compile()

        #--- COMPILE MARKUP
        #       If this is an SFML file, compile the markup and set the result to True or False
        #       depending on whether or not the markup compilation process was successful.
        path = self.sourcePath
        if path and path.endswith('.sfml'):
            result = self._compileMarkup()
        else:
            result = True

        #--- THUMBNAIL
        #       Extract thumbnail property if it exists and create LocalImage in response
        thumbnail = self.get('THUMBNAIL')
        if thumbnail:
            self._thumbnail = LocalImage(self, thumbnail)
        else:
            self.site.writeLogWarning(u'No thumbnail image for Page "%s"' % self._definitionPath)

        return result

#___________________________________________________________________________________________________ process
    def process(self):
        """ Processes the previously compiled results and creates the final output html page with
            all the content and settings. """

        if self.isProcessed:
            return True
        self._isProcessed = True

        for child in self._childPages:
            child.process()

        if not self.has('TITLE', localOnly=True):
            self.site.writeLogWarning(u'Missing Page Title', extras=[
                u'File: ' + self.sourcePath,
                u'Issue Generic page titles are bad for Search Engine Optimization (SEO)',
                u'Solution 1: Add a TITLE property to the definition file',
                u'Solution 2: Add a [#TITLE] block tag in your SFML file'])

        if not self.has('DESCRIPTION', localOnly=True) and not self.has('SUMMARY', localOnly=True):
            self.site.writeLogWarning(u'Missing Page Description', extras=[
                u'File: ' + self.sourcePath,
                u'Issue: Search Engine Optimization (SEO) requires a unique page description',
                u'Solution 1: Add a DESCRIPTION property to the definition file',
                u'Solution 2: Add a [#SUMMARY] block tag in your SFML file'])

        return self._createHtmlPage()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _loadDefinitions
    def _loadDefinitions(self):
        pageDefsPath = self._definitionPath
        directory   = FileUtils.getDirectoryOf(pageDefsPath)

        #--- PAGE DEFINITION --#
        if not pageDefsPath or not os.path.exists(pageDefsPath):
            return False
        try:
            data = JSON.fromFile(pageDefsPath, throwError=True)
            self._data.data = data
        except Exception, err:
            self.site.writeLogError(
                u'Unable to load definitions file for Page "%s"' % self.sourcePath, error=err)
            return

        #--- FOLDER DEFINITION ---#
        folderDefPath = FileUtils.createPath(directory, '__folder__.def', isFile=True)
        if os.path.exists(folderDefPath):
            try:
                data = JSON.fromFile(folderDefPath, throwError=True)
            except Exception, err:
                self.site.writeLogError(
                    u'Unable to load folder definitions file "%s"' % folderDefPath, error=err)
                return

            cd   = ConfigsDict(data)
            test = SiteProcessUtils.testFileFilter(
                self.sourcePath,
                cd.get(('FOLDER', 'EXTENSION_FILTER')),
                cd.get(('FOLDER', 'NAME_FILTER')) )
            if test:
                self._inheritData.append(cd)

        #--- PARENT DEFINITIONS ---#
        steps = []
        while True:
            parentDirectory = FileUtils.createPath(directory, *steps, isDir=True)
            if parentDirectory == self.site.containerPath:
                break
            parentPath = parentDirectory + '__parent__.def'
            if os.path.exists(parentPath):
                try:
                    data = JSON.fromFile(parentPath, throwError=True)
                except Exception, err:
                    self.site.writeLogError(
                        u'Unable to load parent definitions file "%s"' % parentPath, error=err)
                self._inheritData.append(ConfigsDict(data))
            steps.append('..')

        #--- PAGE UID
        #       Create a UID for the page definition if one does not already exist and save that
        #       change to the Page definition file
        if not self._data.get('UID'):
            uid       = []
            uidPrefix = self.get('UID_PREFIX')
            if uidPrefix:
                uid.append(uidPrefix)

            uid.append(TimeUtils.datetimeToTimecode(
                datetime.datetime.utcnow(), StaticFlowEnvironment.baseTime))

            pathParts = self.sourceFolder
            pathParts.append(self.filename)
            uid.append(u'-'.join(pathParts))

            self._data.add('UID', u'_'.join(uid))
            JSON.toFile(pageDefsPath, self._data.data, pretty=True)

        self._createPageVars()

#___________________________________________________________________________________________________ _createPageVars
    def _createPageVars(self):
        self._pageVars             = self.getMerged('PAGE_VARS', dict())
        self._pageVars['CDN_ROOT'] = self.site.cdnRootFolder
        self._pageVars['CDN_URL']  = self.site.cdnRootUrl

        #--- JS INCLUDE ---#
        out = [self._formatPageVarInclude(['staticflow', '/js/sflow/engine.js']) ]
        hasJQuery = False
        for item in self._pageVars['SCRIPTS']:
            scriptInclude = self._formatPageVarInclude(item)
            out.append(scriptInclude)
            hasJQuery = hasJQuery or scriptInclude[0] == 'jquery'

        if not hasJQuery:
            out.insert(0, self._formatPageVarInclude([
                'jquery',
                 '/js/sflow/jquery/jquery.js',
                 '//ajax.googleapis.com/ajax/libs/jquery/2.0.3/jquery.min.js' ]) )

        self._pageVars['SCRIPTS'] = out

        #--- CSS INCLUDES ---#
        out = [self._formatPageVarInclude(['css-staticFlow', '/css/sflow/engine.css'])]
        for item in self._pageVars['CSS']:
            out.append(self._formatPageVarInclude(item))
        self._pageVars['CSS'] = out

        out = []
        for item in self._pageVars['ASYNC']:
            out.append(self._formatPageVarInclude(item))
        self._pageVars['ASYNC'] = out

#___________________________________________________________________________________________________ _formatPageVarInclude
    def _formatPageVarInclude(self, item):
        isLocal = self.site.isLocal
        out = [item[0].lower()]
        url = item[2] if len(item) == 3 and not isLocal else item[1]
        if not isLocal and url[1] != u'/':
            url = self.site.cdnRootUrl + url
        out.append(url)
        return out

#___________________________________________________________________________________________________ _compileMarkup
    def _compileMarkup(self):
        source = FileUtils.getContents(self.sourcePath)
        if source is None:
            return False

        mp = MarkupProcessor(source, path=self.sourcePath)
        mp.get(page=self, site=self.site)
        if mp.hasErrors:
            raise Exception, u'Markup rendering failed "%s"' % self.sourcePath
        self.markupProcessor = mp

        self._date = self._parseDate(ArgsUtils.extract('date', None, mp.metadata))
        self.addItems(mp.metadata)
        return True

#___________________________________________________________________________________________________ _parseData
    def _parseDate(self, value):
        if not value:
            return None

        value = value.replace(u'/', u'-').strip().split(u'-')
        if len(value[-1]) < 4:
            value[-1] = u'20' + value[-1]

        return datetime.datetime(
            year=int(value[-1]),
            month=int(value[0]),
            day=int(value[1]) )

#___________________________________________________________________________________________________ _createHtmlPage
    def _createHtmlPage(self):
        if self.markupProcessor:
            sourceContent = self.markupProcessor.result
        elif self.sourcePath:
            sourceContent = FileUtils.getContents(self.sourcePath)
        else:
            sourceContent = u''

        mr = MakoRenderer(
            template=self.get('TEMPLATE'),
            minify=not self.site.isLocal,
            rootPath=[
                self.site.htmlTemplatePath,
                StaticFlowEnvironment.rootPublicTemplatePath],
            data=dict(
                site=self.site,
                loader=self.site.cdnRootUrl + u'/js/sflow/loader.js',
                pageVars=JSON.asString(self._pageVars),
                page=self,
                htmlSource=sourceContent if sourceContent else u''))
        result = mr.render()

        if not mr.success:
            self.site.writeLogError(u'Unable to create HTML Page', extras=[
                u'Page: ' + self.sourcePath,
                u'Error:' + unicode(mr.errorMessage).replace(u'\n', u'<br />') ])
            return False

        try:
            outDirectory = FileUtils.getDirectoryOf(self.targetPath)
            if not os.path.exists(outDirectory):
                os.makedirs(outDirectory)

            FileUtils.putContents(result, self.targetPath, raiseErrors=True)
            SiteProcessUtils.createHeaderFile(
                self.targetPath, [
                    FileUtils.getUTCModifiedDatetime(self._definitionPath),
                    FileUtils.getUTCModifiedDatetime(self.sourcePath)] )
            # Add the page to the sitemap
            self.site.sitemap.add(self)

            self.site.writeLogSuccess(
                u'CREATED', u'%s -&gt; %s' % (unicode(self.targetPath), self.targetUrl) )
        except Exception, err:
            self.site.writeLogError(u'HTML Page Creation Error', err)
            return False
        return True


