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

        self.markupProcessor    = None

        self._site              = site
        self._definitionPath    = FileUtils.cleanupPath(definitionPath, isFile=True)
        self._sourcePath        = sourcePath
        self._inheritData       = []
        self._date              = None
        self._isProcessed       = False
        self._parentPage        = parentPage
        self._childPages        = []
        self._referencedPages   = []
        self._rssGenerator      = None
        self._rssOwners         = []
        self._thumbnail         = None
        self._pageVars          = None
        self._authorData        = None

        self._loadDefinitions()

        # If an RSS definition exists create an RSS generator
        if self.get('RSS'):
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
        if self._rssGenerator:
            return self._rssGenerator
        if self._rssOwners:
            return self._rssOwners[0]
        return None

#___________________________________________________________________________________________________ GS: renderPass
    @property
    def renderPass(self):
        return self.get('RENDER_PASS', 0)

#___________________________________________________________________________________________________ GS: author
    @property
    def author(self):
        if not self._authorData:
            self._authorData = AuthorData(self)
        return self._authorData

#___________________________________________________________________________________________________ GS: title
    @property
    def title(self):
        return self.get('title')

#___________________________________________________________________________________________________ GS: description
    @property
    def description(self):
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
        return self._pageVars

#___________________________________________________________________________________________________ GS: rssGenerator
    @property
    def rssGenerator(self):
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
        return self._definitionPath

#___________________________________________________________________________________________________ GS: sourcePath
    @property
    def sourcePath(self):
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

#___________________________________________________________________________________________________ GS: site
    @property
    def site(self):
        return self._site

#___________________________________________________________________________________________________ GS: isCompiled
    @property
    def isCompiled(self):
        path = self.sourcePath
        if not path:
            return True

        if self.markupProcessor or path.endswith('html'):
            return True
        return False

#___________________________________________________________________________________________________ GS: isProcessed
    @property
    def isProcessed(self):
        return self._isProcessed

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ addRssOwner
    def addRssOwner(self, rssGenerator):
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
        if not self.isCompiled:
            path   = self.sourcePath
            result = self._compileMarkup() if path and path.endswith('.sfml') else True
        else:
            result = True

        #--- THUMBNAIL
        #       Extract thumbnail property if it exists and create LocalImage in response
        thumbnail = self.get('THUMBNAIL')
        if thumbnail:
            self._thumbnail = LocalImage(self, thumbnail)
        else:
            self.site.writeWarningLog(u'No thumbnail image for Page "%s"' % self._definitionPath)

        return result

#___________________________________________________________________________________________________ process
    def process(self):
        """ Processes the previously compiled results and creates the final output html page with
            all the content and settings. """

        for child in self._childPages:
            child.process()

        if self.isProcessed:
            return True

        if self._createHtmlPage():
            self._isProcessed = True
        return self._isProcessed

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getSourceContent
    def _getSourceContent(self):
        if self.markupProcessor:
            return self.markupProcessor.get(page=self, site=self.site)
        elif not self.sourcePath:
            return u''
        return FileUtils.getContents(self.sourcePath)

#___________________________________________________________________________________________________ _loadDefinitions
    def _loadDefinitions(self):
        pageDefsPath = self._definitionPath
        directory   = FileUtils.getDirectoryOf(pageDefsPath)

        # Load page definitions
        if not pageDefsPath or not os.path.exists(pageDefsPath):
            return False
        self._data.data = JSON.fromFile(pageDefsPath)

        # Load folder level definitions
        folderDefPath = FileUtils.createPath(directory, '__folder__.def', isFile=True)
        if os.path.exists(folderDefPath):
            cd = ConfigsDict(JSON.fromFile(folderDefPath))
            test = SiteProcessUtils.testFileFilter(
                self.sourcePath,
                cd.get(('FOLDER', 'EXTENSION_FILTER')),
                cd.get(('FOLDER', 'NAME_FILTER')) )
            if test:
                self._inheritData.append(cd)

        steps = []
        while True:
            parentDirectory = FileUtils.createPath(directory, *steps, isDir=True)
            if parentDirectory == self.site.containerPath:
                break
            parentPath = parentDirectory + '__parent__.def'
            if os.path.exists(parentPath):
                self._inheritData.append(ConfigsDict(JSON.fromFile(parentPath)))
            steps.append('..')

        # Create a UID for the page definition if one does not already exist
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

        out = [
            self._formatPageVarInclude([
                'jquery',
                 '/js/ext/jquery/jquery.js',
                 '//ajax.googleapis.com/ajax/libs/jquery/2.0.3/jquery.min.js' ]),
            self._formatPageVarInclude(['staticFlow', '/js/engine.js']) ]
        for item in self._pageVars['SCRIPTS']:
            out.append(self._formatPageVarInclude(item))
        self._pageVars['SCRIPTS'] = out

        out = [self._formatPageVarInclude(['css-staticFlow', '/css/engine.css'])]
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
        out = [item[0]]
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

        self.markupProcessor = mp

        if mp.hasErrors:
            for renderError in mp.renderErrors:
                self._site.logger.write(
                    u'<hr />' + unicode(renderError.getHtmlLogDisplay()) + u'<br />')
            return False

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
        data = dict(
            site=self.site,
            loader=self.site.cdnRootUrl + u'/js/loader.js',
            pageVars=JSON.asString(self._pageVars),
            page=self,
            htmlSource=self._getSourceContent())

        mr = MakoRenderer(
            template=self.get('TEMPLATE'),
            rootPath=[
                self.site.htmlTemplatePath,
                StaticFlowEnvironment.rootPublicTemplatePath],
            data=data,
            minify=not self.site.isLocal )
        result = mr.render()

        if not mr.success:
            self._site.logger.write(u'HTML Page Creation Error: ' +  unicode(mr.errorMessage))
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


